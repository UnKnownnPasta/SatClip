"""The contract between the language model and SatClip's deterministic code.

The fine-tuned model only rewrites a free-text question (English, Hindi, Hinglish, typos, any date
format) into this small JSON object. It never resolves geography and never produces a number:
`resolve()` turns the JSON into the backend's ParsedQuery with the same gazetteer and date rules as
the rule parser, so a model mistake can only cost an "I understood ..." correction, never a wrong map.

Target JSON (keys always present, in this order):
  {"intent": "water_extent" | "water_change" | "vegetation_change" | "land_cover" | "describe" | "unsupported",
   "place": "<district name in standard English spelling, or null>",
   "state": "<state name if the user gave one, or null>",
   "dates": ["YYYY-MM-DD", ...],           # in the order the user meant them (before, after)
   "refuse_reason": null | "counting" | "forecast" | "identity" | "other"}
"""
from __future__ import annotations

import json
import re
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Optional

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))

INTENTS = ["water_extent", "water_change", "vegetation_change", "land_cover", "describe", "unsupported"]
REFUSE = [None, "counting", "forecast", "identity", "other"]
KEYS = ["intent", "place", "state", "dates", "refuse_reason"]

SYSTEM_PROMPT = (
    "You convert a question about Indian satellite imagery into JSON with keys intent, place, state, dates, "
    "refuse_reason. intent is one of water_extent, water_change, vegetation_change, land_cover, describe, "
    "unsupported. Write the district name in its standard English spelling. Write dates as YYYY-MM-DD in the order meant. "
    "Use unsupported with a refuse_reason for counting, forecasts, identifying people or anything else. "
    "Reply with JSON only.")

# JSON schema for constrained decoding (archive A150): output always parses and only allowed values appear.
JSON_SCHEMA: dict[str, Any] = {
    "type": "object", "additionalProperties": False, "required": KEYS,
    "properties": {
        "intent": {"enum": INTENTS},
        "place": {"type": ["string", "null"], "maxLength": 60},
        "state": {"type": ["string", "null"], "maxLength": 40},
        "dates": {"type": "array", "maxItems": 2, "items": {"type": "string", "pattern": r"^20\d\d-\d\d-\d\d$"}},
        "refuse_reason": {"enum": REFUSE},
    },
}


def dumps(obj: dict[str, Any]) -> str:
    return json.dumps({k: obj.get(k) for k in KEYS}, ensure_ascii=False, separators=(", ", ": "))


def parse_output(text: str) -> Optional[dict[str, Any]]:
    """Lenient parse of a model reply; returns None when it is not valid against the schema."""
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return None
    try:
        obj = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
    if not isinstance(obj, dict) or obj.get("intent") not in INTENTS or obj.get("refuse_reason") not in REFUSE:
        return None
    dates = obj.get("dates") or []
    if not isinstance(dates, list) or any(not isinstance(d, str) or not re.fullmatch(r"20\d\d-\d\d-\d\d", d) for d in dates):
        return None
    return {k: obj.get(k) for k in KEYS} | {"dates": dates}


def resolve(obj: dict[str, Any], text: str):
    """Model JSON -> backend ParsedQuery, through the same gazetteer and window rules as the rule parser."""
    from satclip import gazetteer
    from satclip.models import DateWindow, Intent, QueryRequest
    from satclip.parser import WINDOW_HALF_DAYS, parse

    windows = []
    for d in obj.get("dates") or []:
        try:
            day = date.fromisoformat(d)
        except ValueError:
            continue
        windows.append(DateWindow(start=day - timedelta(days=WINDOW_HALF_DAYS), end=day + timedelta(days=WINDOW_HALF_DAYS)))
    region = None
    if obj.get("place"):
        hit, options = gazetteer.find(" ".join(x for x in (obj["place"], obj.get("state") or "") if x))
        region = gazetteer.key(hit) if hit else None
    # Build the query through the normal parser so problems, candidates and the echo text are identical.
    # The model's place wins; the raw text is the fallback, exactly as in the rule parser.
    req = QueryRequest(text=text, region=region, windows=windows or None)
    return parse(req, intent=Intent(obj["intent"]))
