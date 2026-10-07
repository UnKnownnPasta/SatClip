"""Rule-based question parser (M1, district gazetteer since M3). A LoRA-tuned VLM can replace the intent step in M5,
but the output contract (ParsedQuery) stays the same and is always echoed to the user.
"""
from __future__ import annotations

import re
from datetime import date, timedelta
from typing import Optional

from . import gazetteer
from .models import BBox, DateWindow, Intent, ParsedQuery, QueryRequest

# Order matters: refusals first, then change intents before extent intents. English plus common Hindi and
# romanised Hindi (Hinglish) words, so the fallback parser serves the questions officials actually type;
# the learned parser (training/lora) handles anything freer than this.
_RULES: list[tuple[Intent, tuple[str, ...]]] = [
    (Intent.unsupported, ("count", "how many", "forecast", "predict", "will it", "tomorrow", "next week", "who ",
                          "which family", "population", "poem", "which party", "gdp", "hotel",
                          " kitne ", " agle ", "aayegi", " kiski ", "कितने", "आएगी", " कल ", "किसकी")),
    (Intent.water_change, ("flood spread", "spread", "more water", "less water", "water change", "flooding change",
                           "newly flooded", "new flood", "flooded since", "flooded after", "compared", "receded",
                           "naya paani", "badhi", "फैली", "नया जलभराव")),
    (Intent.vegetation_change, ("crop", "vegetation", "ndvi", "greenness", "harvest", "sowing", "deforest", "forest loss",
                                "fasal", "hariyali", "फसल", "फ़सल", "हरियाली")),
    (Intent.water_extent, ("flood", "water", "inundat", "submerged", "under water", "paani", "baadh", "doob",
                           "पानी", "बाढ़", "जलमग्न", "डूब", "जलभराव")),
    (Intent.land_cover, ("land cover", "land use", "what is this", "mostly", "classify", "type of area",
                         "kis type", "भूमि किस")),
    (Intent.describe, ("describe", "caption", "what does", "look like", "description", "summary of the scene",
                       "kaisa dikh", "वर्णन")),
]
_ISO = re.compile(r"\b(20\d{2})-(\d{1,2})-(\d{1,2})\b")
# Indian numeric order is day first: 11/07/2024, 11-07-2024, 11.07.2024.
_DMY = re.compile(r"\b(\d{1,2})[/.\-](\d{1,2})[/.\-](20\d{2})\b")
_EN_MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
_HI_MONTHS = {"जनवरी": 1, "फ़रवरी": 2, "फरवरी": 2, "मार्च": 3, "अप्रैल": 4, "मई": 5, "जून": 6, "जुलाई": 7, "अगस्त": 8,
              "सितंबर": 9, "सितम्बर": 9, "अक्टूबर": 10, "नवंबर": 11, "नवम्बर": 11, "दिसंबर": 12, "दिसम्बर": 12}
_MON = r"(jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june?|july?|aug(?:ust)?|sept?(?:ember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)"
_DAY_MON = re.compile(r"\b(\d{1,2})(?:st|nd|rd|th)?\s+(?:of\s+)?" + _MON + r"\.?,?\s+(20\d{2})\b", re.I)
_MON_DAY = re.compile(r"\b" + _MON + r"\.?\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(20\d{2})\b", re.I)
_HI_DATE = re.compile(r"(\d{1,2})\s+(" + "|".join(_HI_MONTHS) + r")\s+(20\d{2})")
_DEVANAGARI_DIGITS = str.maketrans("०१२३४५६७८९", "0123456789")


def _month(name: str) -> int:
    return _EN_MONTHS.index(name.lower()[:3]) + 1


def dates_in_text(text: str) -> list[date]:
    """Every calendar date in the question, in reading order. Accepts ISO (2024-07-11), Indian numeric
    day-first forms (11/07/2024, 11-07-2024, 11.07.2024), '11 July 2024', '11th Jul, 2024', 'July 11, 2024'
    and Hindi month names ('11 जुलाई 2024', Devanagari digits too). Impossible dates are skipped."""
    t = text.translate(_DEVANAGARI_DIGITS)
    found: list[tuple[int, date]] = []
    taken: list[tuple[int, int]] = []

    def add(m: re.Match, y: int, mo: int, d: int) -> None:
        if any(a < m.end() and m.start() < b for a, b in taken):
            return
        try:
            found.append((m.start(), date(y, mo, d)))
            taken.append((m.start(), m.end()))
        except ValueError:
            pass

    for m in _ISO.finditer(t):
        add(m, int(m[1]), int(m[2]), int(m[3]))
    for m in _DMY.finditer(t):
        add(m, int(m[3]), int(m[2]), int(m[1]))
    for m in _DAY_MON.finditer(t):
        add(m, int(m[3]), _month(m[2]), int(m[1]))
    for m in _MON_DAY.finditer(t):
        add(m, int(m[3]), _month(m[1]), int(m[2]))
    for m in _HI_DATE.finditer(t):
        add(m, int(m[3]), _HI_MONTHS[m[2]], int(m[1]))
    return [d for _, d in sorted(found, key=lambda x: x[0])]


_BBOX = re.compile(r"bbox[:=\s]*\(?\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)")
_CHANGE = {Intent.water_change, Intent.vegetation_change}
WINDOW_HALF_DAYS = 6  # a date in the question becomes a +/- 6 day search window (Sentinel-1 revisit)


def classify_intent(text: str, n_dates: int = 0) -> Intent:
    """First matching rule wins. A water question that names two dates is a change question."""
    t = " " + re.sub(r"[?!.,]", " ", text.lower()) + " "
    for intent, keys in _RULES:
        if any(k in t for k in keys):
            if intent == Intent.water_extent and n_dates >= 2:
                return Intent.water_change
            return intent
    return Intent.unsupported


def _windows_from_text(text: str) -> list[DateWindow]:
    return [DateWindow(start=d - timedelta(days=WINDOW_HALF_DAYS), end=d + timedelta(days=WINDOW_HALF_DAYS))
            for d in dates_in_text(text)]


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


def parse(req: QueryRequest, intent: Optional[Intent] = None) -> ParsedQuery:
    """`intent` lets a learned parser (training/lora/schema.py) supply the intent; everything else
    (gazetteer, windows, problems, echo text) stays deterministic."""
    intent = intent or classify_intent(req.text, len(dates_in_text(req.text)))
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
