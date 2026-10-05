"""District gazetteer: 735 Indian district outlines from geoBoundaries gbOpen IND ADM2
(ODbL 1.0, sourced from lgdirectory.gov.in; rebuilt with tools/build_gazetteer.py).

Replaces the three hand-typed demo boxes of M1. Duplicate names (for example Aurangabad in
Bihar and in Maharashtra) are resolved by a state name in the question, otherwise the user
is asked to choose. Names of four letters or fewer must match with their capitalisation,
so that common words do not trigger a district.
"""
from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any, Optional

PATH = Path(__file__).resolve().parent / "resources" / "districts.json"


def key(d: dict[str, Any]) -> str:
    return f"{d['name'].lower()}|{d['state'].lower()}"


@lru_cache(maxsize=1)
def _data() -> dict[str, Any]:
    raw = json.loads(PATH.read_text(encoding="utf-8"))
    by_key = {key(d): d for d in raw["districts"]}
    by_name: dict[str, list[dict]] = {}
    for d in raw["districts"]:
        by_name.setdefault(d["name"].lower(), []).append(d)
    states = sorted({d["state"] for d in raw["districts"]}, key=len, reverse=True)
    names = sorted(by_name, key=len, reverse=True)
    return {"meta": raw["meta"], "by_key": by_key, "by_name": by_name, "states": states, "names": names}


def get(region_key: str) -> Optional[dict[str, Any]]:
    return _data()["by_key"].get(region_key)


def meta() -> dict[str, Any]:
    return _data()["meta"]


def find(text: str) -> tuple[Optional[dict[str, Any]], list[dict[str, Any]]]:
    """Return (district, candidates). district is None when nothing matched or the name is ambiguous."""
    data = _data()
    low = text.lower()
    for name in data["names"]:
        if len(name) <= 4:  # short names must match with their capitalisation
            proper = data["by_name"][name][0]["name"]
            hit = re.search(r"(?<![A-Za-z])" + re.escape(proper) + r"(?![A-Za-z])", text)
        else:
            hit = re.search(r"(?<![a-z])" + re.escape(name) + r"(?![a-z])", low)
        if not hit:
            continue
        options = data["by_name"][name]
        if len(options) == 1:
            return options[0], options
        named = [d for d in options if d["state"].lower() in low]
        if len(named) == 1:
            return named[0], options
        return None, options
    return None, []


def outline_lonlat(region_key: str):
    """Shapely geometry of the district outline (lon/lat)."""
    from shapely.geometry import shape
    d = get(region_key)
    return shape(d["geometry"]) if d else None
