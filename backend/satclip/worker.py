"""Worker: take a tile job, check the cache, run the instrument, return the result."""
from __future__ import annotations

from .cache import Cache, cache_key
from .instruments import get
from .models import TileJob, TileResult, TileStatus


def process(job: TileJob, cache: Cache) -> TileResult:
    version, fn = get(job.instrument)
    key = cache_key(job.tile_id, f"{job.instrument}@{version}", [w.model_dump(mode="json") for w in job.windows],
                    {"region": job.region} if job.region else None)
    hit = cache.get(key)
    if hit:
        res = TileResult(**hit)
        return res.model_copy(update={"job_id": job.job_id, "cache_hit": True})
    try:
        res = fn(job)
    except Exception as exc:  # a broken tile must never break the job
        return TileResult(job_id=job.job_id, tile_id=job.tile_id, status=TileStatus.error, reason=repr(exc)[:300])
    res.params = {**res.params, "instrument": job.instrument, "instrument_version": version}
    if res.status != TileStatus.error:
        cache.set(key, res.model_dump(mode="json"))
    return res


def run_redis_worker() -> None:  # pragma: no cover - needs a Redis server
    """Entry point for `python -m satclip.worker` in the worker container."""
    from .jobqueue import RedisQueue
    from .config import settings
    q = RedisQueue.from_settings(settings())
    q.work_forever()


if __name__ == "__main__":  # pragma: no cover
    run_redis_worker()
