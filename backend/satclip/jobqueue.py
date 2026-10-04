"""Job queue backends (ARCHITECTURE.md 6.2).

InlineQueue: in-process thread pool, for development, demos and tests. No external services.
RedisQueue:  jobs in Redis, tile jobs on a list, workers in separate containers.
Both expose the same interface to the API: submit(job, tile_jobs), get(job_id), receipt(id).
"""
from __future__ import annotations

import json
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Optional

from .aggregate import aggregate
from .cache import MemoryCache, RedisCache
from .models import Job, JobState, TileJob, TileResult
from .receipt import build_receipt
from .worker import process


def new_job_id() -> str:
    return uuid.uuid4().hex[:12]


def _finalize(job: Job, trust: dict[str, Any]) -> dict:
    card = aggregate(job, trust)
    receipt = build_receipt(job.parsed.model_dump(mode="json"),
                            [r.model_dump(mode="json") for r in job.results], card.model_dump(mode="json"))
    card.receipt_id = receipt["receipt_id"]
    job.card, job.state = card, JobState.done
    return receipt


class InlineQueue:
    def __init__(self, trust: dict[str, Any], concurrency: int = 4) -> None:
        self.trust = trust
        self.cache = MemoryCache()
        self.jobs: dict[str, Job] = {}
        self.receipts: dict[str, dict] = {}
        self._lock = threading.Lock()
        self._pool = ThreadPoolExecutor(max_workers=concurrency, thread_name_prefix="satclip-tile")

    def submit(self, job: Job, tile_jobs: list[TileJob]) -> None:
        job.tiles_total = len(tile_jobs)
        job.state = JobState.running
        with self._lock:
            self.jobs[job.job_id] = job
        for tj in tile_jobs:
            self._pool.submit(self._run, tj)

    def store_done(self, job: Job, receipt: Optional[dict] = None) -> None:
        with self._lock:
            self.jobs[job.job_id] = job
            if receipt:
                self.receipts[receipt["receipt_id"]] = receipt

    def _run(self, tj: TileJob) -> None:
        res = process(tj, self.cache)
        with self._lock:
            job = self.jobs[tj.job_id]
            job.results.append(res)
            if len(job.results) == job.tiles_total:
                receipt = _finalize(job, self.trust)
                self.receipts[receipt["receipt_id"]] = receipt

    def get(self, job_id: str) -> Optional[Job]:
        with self._lock:
            job = self.jobs.get(job_id)
            return job.model_copy(deep=True) if job else None

    def receipt(self, receipt_id: str) -> Optional[dict]:
        return self.receipts.get(receipt_id)

    def wait(self, job_id: str, timeout: float = 30) -> Optional[Job]:
        end = time.time() + timeout
        while time.time() < end:
            job = self.get(job_id)
            if job and job.state in (JobState.done, JobState.failed):
                return job
            time.sleep(0.01)
        return self.get(job_id)


class RedisQueue:
    """Keys: satclip:job:{id} (Job JSON), satclip:results:{id} (list of TileResult JSON),
    satclip:tiles (pending TileJob JSON), satclip:processing (in-flight), satclip:receipt:{id}."""

    TILES, PROCESSING = "satclip:tiles", "satclip:processing"

    def __init__(self, client, trust: dict[str, Any], visibility_timeout_s: int = 300) -> None:
        self.r, self.trust, self.vt = client, trust, visibility_timeout_s
        self.cache = RedisCache(client)

    @classmethod
    def from_settings(cls, cfg: dict[str, Any]) -> "RedisQueue":
        import redis  # optional dependency
        q = cfg.get("queue", {})
        return cls(redis.Redis.from_url(q.get("redis_url", "redis://localhost:6379/0")),
                   cfg.get("trust", {}), int(q.get("visibility_timeout_s", 300)))

    def _save(self, job: Job) -> None:
        self.r.set(f"satclip:job:{job.job_id}", job.model_dump_json(exclude={"results"}), ex=7 * 86400)

    def submit(self, job: Job, tile_jobs: list[TileJob]) -> None:
        job.tiles_total, job.state = len(tile_jobs), JobState.running
        self._save(job)
        pipe = self.r.pipeline()
        for tj in tile_jobs:
            pipe.lpush(self.TILES, tj.model_dump_json())
        pipe.execute()

    def store_done(self, job: Job, receipt: Optional[dict] = None) -> None:
        self._save(job)
        if receipt:
            self.r.set(f"satclip:receipt:{receipt['receipt_id']}", json.dumps(receipt, default=str))

    def get(self, job_id: str) -> Optional[Job]:
        raw = self.r.get(f"satclip:job:{job_id}")
        if not raw:
            return None
        job = Job.model_validate_json(raw)
        job.results = [TileResult.model_validate_json(x) for x in self.r.lrange(f"satclip:results:{job_id}", 0, -1)]
        return job

    def receipt(self, receipt_id: str) -> Optional[dict]:
        raw = self.r.get(f"satclip:receipt:{receipt_id}")
        return json.loads(raw) if raw else None

    def work_once(self, block_s: int = 5) -> bool:
        raw = self.r.brpoplpush(self.TILES, self.PROCESSING, timeout=block_s)
        if raw is None:
            return False
        tj = TileJob.model_validate_json(raw)
        res = process(tj, self.cache)
        n = self.r.rpush(f"satclip:results:{tj.job_id}", res.model_dump_json())
        self.r.lrem(self.PROCESSING, 1, raw)
        job = self.get(tj.job_id)
        # Exactly one worker sees n == tiles_total, so exactly one finalizes.
        if job and n == job.tiles_total:
            receipt = _finalize(job, self.trust)
            self.store_done(job, receipt)
        return True

    def requeue_stale(self) -> int:  # pragma: no cover - simple janitor, run periodically
        """Move in-flight jobs back to pending (call after a worker crash; jobs are idempotent)."""
        moved = 0
        while self.r.rpoplpush(self.PROCESSING, self.TILES):
            moved += 1
        return moved

    def work_forever(self) -> None:  # pragma: no cover
        while True:
            self.work_once()


def make_queue(cfg: dict[str, Any]):
    q = cfg.get("queue", {})
    if q.get("backend", "inline") == "redis":
        return RedisQueue.from_settings(cfg)
    return InlineQueue(cfg.get("trust", {}), int(q.get("worker_concurrency", 4)))
