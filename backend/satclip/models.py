"""Core data model. See docs/ARCHITECTURE.md section 5."""
from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class Intent(str, Enum):
    water_extent = "water_extent"
    water_change = "water_change"
    vegetation_change = "vegetation_change"
    land_cover = "land_cover"
    describe = "describe"
    unsupported = "unsupported"


class DateWindow(BaseModel):
    start: date
    end: date


BBox = tuple[float, float, float, float]  # min_lon, min_lat, max_lon, max_lat


class QueryRequest(BaseModel):
    text: str = Field(min_length=3, max_length=500)
    bbox: Optional[BBox] = None
    windows: Optional[list[DateWindow]] = None


class ParsedQuery(BaseModel):
    text: str
    intent: Intent
    bbox: Optional[BBox] = None
    place_name: Optional[str] = None
    windows: list[DateWindow] = []
    understood_as: str
    problems: list[str] = []  # why the query cannot run yet (missing AOI, dates, out of scope)


class TileJob(BaseModel):
    job_id: str
    tile_id: str
    bbox: BBox
    intent: Intent
    windows: list[DateWindow]
    instrument: str


class TileStatus(str, Enum):
    ok = "ok"
    abstain = "abstain"
    error = "error"


class TileResult(BaseModel):
    job_id: str
    tile_id: str
    status: TileStatus
    value: Optional[float] = None       # e.g. water area in sq km for this tile
    unit: Optional[str] = None
    confidence: Optional[float] = None  # calibrated, 0..1
    scenes: list[dict[str, Any]] = []   # [{id, date, sensor, catalog, href}]
    params: dict[str, Any] = {}         # instrument parameters, incl. fitted thresholds
    reason: Optional[str] = None
    cache_hit: bool = False


class SceneRef(BaseModel):
    id: str
    date: str
    sensor: str
    catalog: Optional[str] = None


class EvidenceCard(BaseModel):
    job_id: str
    answer_text: str
    value: Optional[float] = None
    unit: Optional[str] = None
    confidence: Optional[float] = None
    confidence_band: Optional[str] = None
    abstained: bool
    reason: Optional[str] = None
    next_step: Optional[str] = None
    understood_as: str
    scenes: list[SceneRef] = []
    observed_vs_inferred: str = "observed"
    tiles_total: int = 0
    tiles_answered: int = 0
    receipt_id: Optional[str] = None


class JobState(str, Enum):
    queued = "queued"
    running = "running"
    done = "done"
    failed = "failed"


class Job(BaseModel):
    job_id: str
    parsed: ParsedQuery
    state: JobState = JobState.queued
    tiles_total: int = 0
    results: list[TileResult] = []
    card: Optional[EvidenceCard] = None
