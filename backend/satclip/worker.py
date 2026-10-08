"""Worker: take a tile job, check the cache, run the instrument, return the result."""
from __future__ import annotations

import time

from .cache import Cache, cache_key
from .instruments import get
from .models import TileJob, TileResult, TileStatus


# Run 8: transient read failures made the same question give different answers (a few tiles dropped
# out). A failed tile is retried once after a pause, outside the per-read retries in data/cog.py.
TILE_ATTEMPTS = 2
RETRY_DELAY_S = 3.0


def process(job: TileJob, cache: Cache) -> TileResult:
    version, fn = get(job.instrument)
    key = cache_key(job.tile_id, f"{job.instrument}@{version}", [w.model_dump(mode="json") for w in job.windows],
                    {"region": job.region} if job.region else None)
    hit = cache.get(key)
    if hit:
        res = TileResult(**hit)
        return res.model_copy(update={"job_id": job.job_id, "cache_hit": True})
    for attempt in range(TILE_ATTEMPTS):
        try:
            res = fn(job)
            break
        except Exception as exc:  # a broken tile must never break the job
            if attempt + 1 == TILE_ATTEMPTS:
                return TileResult(job_id=job.job_id, tile_id=job.tile_id, status=TileStatus.error, reason=repr(exc)[:300])
            time.sleep(RETRY_DELAY_S * (attempt + 1))
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
