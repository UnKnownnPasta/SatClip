import copy

import pytest

fakeredis = pytest.importorskip("fakeredis")

from satclip.config import load_settings
from satclip.jobqueue import RedisQueue, new_job_id
from satclip.models import Job, QueryRequest, TileJob
from satclip.parser import parse
from satclip.tiling import tiles_for_bbox


def test_redis_queue_roundtrip():
    cfg = copy.deepcopy(load_settings(environ={}))
    q = RedisQueue(fakeredis.FakeRedis(), cfg["trust"])
    parsed = parse(QueryRequest(text="water on 2026-07-05", bbox=(91.0, 26.2, 91.1, 26.3)))
    job = Job(job_id=new_job_id(), parsed=parsed)
    tiles = tiles_for_bbox(parsed.bbox, 0.05)
    q.submit(job, [TileJob(job_id=job.job_id, tile_id=t, bbox=b, intent=parsed.intent,
                           windows=parsed.windows, instrument="synthetic") for t, b in tiles])
    while q.work_once(block_s=1):
        pass
    done = q.get(job.job_id)
    assert done.state.value == "done" and len(done.results) == len(tiles)
    assert q.receipt(done.card.receipt_id)["output_hash"]
