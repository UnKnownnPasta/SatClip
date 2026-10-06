"""Rule-based question parser (M1, district gazetteer since M3). A LoRA-tuned VLM can replace the intent step in M5,
but the output contract (ParsedQuery) stays the same and is always echoed to the user.
"""
from __future__ import annotations

import re
from datetime import date, timedelta
from typing import Optional

from . import gazetteer
from .models import BBox, DateWindow, Intent, ParsedQuery, QueryRequest

# Order matters: change intents are checked before extent intents.
_RULES: list[tuple[Intent, tuple[str, ...]]] = [
    (Intent.unsupported, ("count", "how many cars", "how many houses", "forecast", "predict", "will it", "tomorrow", "who ")),
    (Intent.water_change, ("flood spread", "spread", "more water", "less water", "water change", "flooding change",
                           "newly flooded", "new flood", "flooded since", "flooded after", "compared")),
    (Intent.vegetation_change, ("crop", "vegetation", "ndvi", "greenness", "harvest", "sowing", "deforest", "forest loss")),
    (Intent.water_extent, ("flood", "water", "inundat", "submerged", "under water")),
    (Intent.land_cover, ("land cover", "land use", "what is this", "mostly", "classify", "type of area")),
    (Intent.describe, ("describe", "caption", "what does", "summary of the scene")),
]

_ISO = re.compile(r"\b(20\d{2})-(\d{2})-(\d{2})\b")
_BBOX = re.compile(r"bbox[:=\s]*\(?\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)")
_CHANGE = {Intent.water_change, Intent.vegetation_change}
WINDOW_HALF_DAYS = 6  # a date in the question becomes a +/- 6 day search window (Sentinel-1 revisit)


def classify_intent(text: str) -> Intent:
    t = " " + text.lower() + " "
    for intent, keys in _RULES:
        if any(k in t for k in keys):
            return intent
    return Intent.unsupported


def _windows_from_text(text: str) -> list[DateWindow]:
    out = []
    for y, m, d in _ISO.findall(text):
        try:
            day = date(int(y), int(m), int(d))
        except ValueError:
            continue
        out.append(DateWindow(start=day - timedelta(days=WINDOW_HALF_DAYS), end=day + timedelta(days=WINDOW_HALF_DAYS)))
    return out


def _bbox_from_text(text: str) -> tuple[Optional[BBox], Optional[str], Optional[str], list[str]]:
    """Return (bbox, place name, region key, ambiguous candidates)."""
    m = _BBOX.search(text)
    if m:
        return tuple(float(v) for v in m.groups()), None, None, []  # type: ignore[return-value]
    d, options = gazetteer.find(text)
    if d:
        return tuple(d["bbox"]), f"{d['name']}, {d['state']}", gazetteer.key(d), []  # type: ignore[return-value]
    return None, None, None, [(f"{o['name']}, {o['state']}", gazetteer.key(o)) for o in options]


def _valid_bbox(b: BBox) -> bool:
    return -180 <= b[0] < b[2] <= 180 and -90 <= b[1] < b[3] <= 90


def parse(req: QueryRequest) -> ParsedQuery:
    intent = classify_intent(req.text)
    picked = gazetteer.get(req.region) if req.region else None
    if picked:
        bbox, place, region, options = (tuple(picked["bbox"]), f"{picked['name']}, {picked['state']}",
                                        gazetteer.key(picked), [])
    elif req.bbox:
        bbox, place, region, options = tuple(req.bbox), None, None, []
    else:
        bbox, place, region, options = _bbox_from_text(req.text)
    windows = list(req.windows) if req.windows else _windows_from_text(req.text)
    problems: list[str] = []

    if intent == Intent.unsupported:
        problems.append("out_of_scope")
    if bbox is None:
        problems.append("ambiguous_area" if options else "missing_area")
    elif not _valid_bbox(bbox):  # type: ignore[arg-type]
        problems.append("invalid_area")
    need = 2 if intent in _CHANGE else 1
    if intent != Intent.unsupported and len(windows) < need:
        problems.append("missing_dates" if need == 1 else "need_two_dates")
    windows = sorted(windows, key=lambda w: w.start)[: max(need, 1)]

    where = place or (f"the box {bbox}" if bbox else "an unspecified area")
    when = " vs ".join(f"{w.start}..{w.end}" for w in windows) or "no dates"
    label = intent.value.replace("_", " ")
    understood = (f"{label} in {where}, {when}" if intent != Intent.unsupported
                  else "a question outside what SatClip can measure")
    return ParsedQuery(text=req.text, intent=intent, bbox=bbox, place_name=place, windows=windows,
                       region=region, candidates=[o[0] for o in options], candidate_keys=[o[1] for o in options],
                       understood_as=understood, problems=problems)
