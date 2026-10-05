"""Instrument registry. An instrument is a named, versioned, transparent measurement:
measure(job) -> TileResult with a confidence from the instrument's calibration file.

Registered here: `not_implemented` (abstains honestly) and `synthetic` (tests only).
Real instruments (M3) live in water.py (sar_water_otsu, sar_logratio_change), vegetation.py
(ndvi_difference) and landcover.py (zero_shot_landcover, index_caption)."""
from __future__ import annotations

from typing import Callable

from ..models import TileJob, TileResult, TileStatus
from ..receipt import digest
from ..tiling import tile_area_km2

Instrument = Callable[[TileJob], TileResult]
REGISTRY: dict[str, tuple[str, Instrument]] = {}  # name -> (version, fn)


def register(name: str, version: str):
    def deco(fn: Instrument) -> Instrument:
        REGISTRY[name] = (version, fn)
        return fn
    return deco


def get(name: str) -> tuple[str, Instrument]:
    if name in REGISTRY:
        return REGISTRY[name]
    return REGISTRY["not_implemented"]


@register("not_implemented", "0")
def not_implemented(job: TileJob) -> TileResult:
    return TileResult(job_id=job.job_id, tile_id=job.tile_id, status=TileStatus.abstain,
                      reason=f"instrument '{job.instrument}' is not implemented yet (planned for M3)")


@register("synthetic", "0")
def synthetic(job: TileJob) -> TileResult:
    """Deterministic fake measurement for pipeline tests. Never used for real answers."""
    h = int(digest({"t": job.tile_id, "w": [w.model_dump() for w in job.windows]})[:8], 16)
    frac = (h % 1000) / 1000 * 0.3
    conf = 0.55 + (h % 400) / 1000
    return TileResult(job_id=job.job_id, tile_id=job.tile_id, status=TileStatus.ok,
                      value=round(frac * tile_area_km2(job.bbox), 3), unit="km2", confidence=round(conf, 3),
                      scenes=[{"id": "SYNTHETIC", "date": str(job.windows[0].start), "sensor": "synthetic"}],
                      params={"synthetic": True})


# Real instruments (M3). Imported last so they can use `register`.
from . import landcover, vegetation, water  # noqa: E402,F401
