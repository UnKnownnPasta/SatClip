"""SatClip load test: how fast do tiles move through the queue, and does it scale with workers?

    cd backend && python ../tools/loadtest.py                 # writes docs/quality/loadtest.json
    cd backend && python ../tools/loadtest.py --tiles 200 --io-ms 0,400

Every tile runs the real SAR water core (`classify_sar_water`, VV+VH, threshold fit, speckle
cleanup) on a synthetic 280 x 280 pixel tile (0.05 degrees at 20 m), plus a sleep that stands in
for the COG window reads (--io-ms; the live per-tile time is measured separately by tools/demo.py).
No network is used, so the numbers isolate SatClip's own compute and queue overhead.

Scenarios
  inline   in-process thread pool (the dev and single-laptop deployment), concurrency 1, 4, 8
  redis    a real redis-server and 1, 2, 4 worker processes (the docker-compose deployment);
           falls back to skipping if redis-server is not installed
  warm     the same job again: every tile is a cache hit
  api      POST /v1/queries for questions that need no measurement (parser and card path only)
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

import numpy as np  # noqa: E402
import psutil  # noqa: E402

from satclip.instruments import register  # noqa: E402
from satclip.instruments.water import classify_sar_water  # noqa: E402
from satclip.models import DateWindow, Intent, Job, JobState, ParsedQuery, TileJob, TileResult, TileStatus  # noqa: E402
from satclip.receipt import digest  # noqa: E402
from satclip.tiling import tile_area_km2, tiles_for_bbox  # noqa: E402

PX = 280
IO_MS = float(os.environ.get("SATCLIP_LOADTEST_IO_MS", "0"))


@register("loadtest", "1")
def loadtest_instrument(job: TileJob) -> TileResult:
    """Real water classification on a deterministic synthetic tile, plus simulated read latency."""
    seed = int(digest({"t": job.tile_id})[:8], 16)
    rng = np.random.default_rng(seed)
    frac = 0.1 + (seed % 300) / 1000
    water = rng.random((PX, PX)) < frac
    vv = np.where(water, rng.normal(-21, 1.5, (PX, PX)), rng.normal(-9, 2.0, (PX, PX)))
    vh = vv - 7 + rng.normal(0, 1.0, (PX, PX))
    if IO_MS:
        time.sleep(IO_MS / 1000)
    mask, q = classify_sar_water(vv, np.ones_like(water), vh_db=vh)
    area = tile_area_km2(job.bbox)
    return TileResult(job_id=job.job_id, tile_id=job.tile_id, status=TileStatus.ok,
                      value=round(float(mask.mean()) * area, 3), unit="km2",
                      confidence=round(float(q["raw_quality"]), 3),
                      scenes=[{"id": "LOADTEST", "date": "2024-07-11", "sensor": "synthetic"}],
                      params={"synthetic": True, "measured_km2": round(area, 3)})


def make_job(n_tiles: int, tag: str) -> tuple[Job, list[TileJob]]:
    side = int(np.ceil(np.sqrt(n_tiles)))
    bbox = (80.0, 20.0, 80.0 + side * 0.05, 20.0 + side * 0.05)
    tiles = tiles_for_bbox(bbox, 0.05)[:n_tiles]
    w = [DateWindow(start="2024-07-05", end="2024-07-17")]
    parsed = ParsedQuery(text=f"loadtest {tag}", intent=Intent.water_extent, bbox=bbox, windows=w,
                         understood_as="load test")
    job = Job(job_id=f"lt{tag}{int(time.time() * 1000) % 10**8}", parsed=parsed)
    return job, [TileJob(job_id=job.job_id, tile_id=tid, bbox=tb, intent=Intent.water_extent, windows=w,
                         instrument="loadtest") for tid, tb in tiles]


def rss_mb(pids: list[int]) -> float:
    tot = 0
    for p in pids:
        try:
            tot += psutil.Process(p).memory_info().rss
        except psutil.Error:
            pass
    return round(tot / 2**20, 1)


def run_inline(n: int, conc: int) -> dict:
    from satclip.jobqueue import InlineQueue
    q = InlineQueue({"abstain_below": 0.6, "bands": []}, concurrency=conc)
    out = {}
    for phase in ("cold", "warm"):
        job, tjs = make_job(n, f"i{conc}")  # same tile ids both phases, so "warm" is all cache hits
        t0 = time.perf_counter()
        q.submit(job, tjs)
        done = q.wait(job.job_id, timeout=3600)
        dt = time.perf_counter() - t0
        assert done and done.state == JobState.done
        out[phase] = {"seconds": round(dt, 3), "tiles_per_s": round(n / dt, 1),
                      "cache_hits": sum(r.cache_hit for r in done.results)}
    out["rss_mb"] = rss_mb([os.getpid()])
    return out


def free_port() -> int:
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def worker_main(url: str) -> None:
    import redis
    from satclip.jobqueue import RedisQueue
    q = RedisQueue(redis.Redis.from_url(url), {"abstain_below": 0.6, "bands": []})
    while not q.r.exists("satclip:loadtest:stop"):
        q.work_once(block_s=1)


def run_redis(n: int, workers_list: list[int], io_ms: float) -> dict:
    exe = shutil.which("redis-server")
    if not exe:
        return {"skipped": "redis-server not installed"}
    import redis
    from satclip.jobqueue import RedisQueue
    port = free_port()
    srv = subprocess.Popen([exe, "--port", str(port), "--save", "", "--appendonly", "no"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    url = f"redis://127.0.0.1:{port}/0"
    try:
        r = redis.Redis.from_url(url)
        for _ in range(50):
            try:
                r.ping()
                break
            except redis.ConnectionError:
                time.sleep(0.1)
        q = RedisQueue(r, {"abstain_below": 0.6, "bands": []})
        out = {}
        for k in workers_list:
            r.flushdb()
            env = {**os.environ, "SATCLIP_LOADTEST_IO_MS": str(io_ms), "PYTHONPATH": str(ROOT / "backend")}
            procs = [subprocess.Popen([sys.executable, __file__, "--worker", url], env=env, cwd=str(ROOT / "backend"))
                     for _ in range(k)]
            time.sleep(2.0)  # let workers import numpy and connect
            res = {}
            for phase in ("cold", "warm"):
                job, tjs = make_job(n, f"r{k}")
                t0 = time.perf_counter()
                q.submit(job, tjs)
                while True:
                    j = q.get(job.job_id)
                    if j.state == JobState.done:
                        break
                    time.sleep(0.02)
                dt = time.perf_counter() - t0
                res[phase] = {"seconds": round(dt, 3), "tiles_per_s": round(n / dt, 1),
                              "cache_hits": sum(x.cache_hit for x in j.results)}
            res["worker_rss_mb_total"] = rss_mb([p.pid for p in procs])
            res["redis_rss_mb"] = rss_mb([srv.pid])
            r.set("satclip:loadtest:stop", 1)
            for p in procs:
                p.wait(timeout=30)
            out[f"{k}_workers"] = res
            print(f"  redis {k} workers: {res}", flush=True)
        return out
    finally:
        srv.terminate()
        srv.wait(timeout=10)


def run_api(n: int) -> dict:
    from fastapi.testclient import TestClient
    from satclip.api.main import create_app
    from satclip.config import settings
    c = TestClient(create_app(settings()))
    qs = ["Count the boats in Ernakulam", "How much of Aurangabad was under water on 2024-08-10?",
          "How much was under water?", "Did the crop decline in Darbhanga?"]
    c.post("/v1/queries", json={"text": qs[0]})  # warm imports and the gazetteer
    lat = []
    t0 = time.perf_counter()
    for i in range(n):
        s = time.perf_counter()
        r = c.post("/v1/queries", json={"text": qs[i % len(qs)]})
        assert r.status_code == 202
        lat.append((time.perf_counter() - s) * 1000)
    dt = time.perf_counter() - t0
    lat.sort()
    return {"requests": n, "requests_per_s_single_client": round(n / dt, 1),
            "p50_ms": round(lat[len(lat) // 2], 2), "p95_ms": round(lat[int(len(lat) * 0.95)], 2)}


def main() -> None:
    global IO_MS
    if len(sys.argv) == 3 and sys.argv[1] == "--worker":
        worker_main(sys.argv[2])
        return
    ap = argparse.ArgumentParser()
    ap.add_argument("--tiles", type=int, default=144, help="tiles per job (Barpeta district is about 140)")
    ap.add_argument("--io-ms", default="0,400", help="simulated read latency per tile, comma separated")
    ap.add_argument("--out", default=str(ROOT / "docs" / "quality" / "loadtest.json"))
    a = ap.parse_args()
    report = {"generated": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()), "tiles_per_job": a.tiles,
              "tile_pixels": f"{PX}x{PX}", "cpu_count": os.cpu_count(),
              "cpu_model": next((l.split(":", 1)[1].strip() for l in open("/proc/cpuinfo") if l.startswith("model name")), "?")
              if os.path.exists("/proc/cpuinfo") else "?", "runs": {}}
    for io in [float(x) for x in a.io_ms.split(",")]:
        IO_MS = io
        os.environ["SATCLIP_LOADTEST_IO_MS"] = str(io)
        key = f"io_{int(io)}ms"
        report["runs"][key] = {"inline": {}, "redis": None}
        for conc in (1, 4, 8):
            report["runs"][key]["inline"][f"concurrency_{conc}"] = res = run_inline(a.tiles, conc)
            print(f"{key} inline x{conc}: {res}", flush=True)
        report["runs"][key]["redis"] = run_redis(a.tiles, [1, 2, 4], io)
    report["api"] = run_api(400)
    print("api:", report["api"])
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=1))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
