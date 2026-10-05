"""Scene selection: which sensor and which scene answer this tile, and why (SOLUTION.md section 4).

Rules:
- Water questions in monsoon months go radar first (cloud over India is above 60% in June to September).
- Outside the monsoon, water questions go optical first and fall back to radar when optical is cloudy.
- Vegetation, land cover and description need optical; they abstain on cloud rather than swap sensor.
- A scene must cover the tile, be openly readable, have the bands the instrument needs, and fall
  within `max_days_from_request` of the window centre. The closest to the centre wins.
- Change pairs use the same sensor, and for radar the same orbit direction (and relative orbit if known).
Every decision becomes a plain-language reason that is printed on the card.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Any, Optional

from ..models import DateWindow, Intent
from .scene import Scene

WATER = {Intent.water_extent, Intent.water_change}
NEEDS = {
    ("S1", "water"): {"vv"},
    ("S2", "water"): {"green", "nir", "scl"},
    ("S2", "vegetation"): {"red", "nir", "scl"},
    ("S2", "optical"): {"red", "green", "blue", "nir", "scl"},
}
SENSOR_NAME = {"S1": "Sentinel-1 radar", "S2": "Sentinel-2 optical"}


@dataclass
class Selection:
    ok: bool
    sensor: Optional[str] = None
    scene: Optional[Scene] = None
    reason: str = ""
    fallback_used: bool = False
    considered: dict[str, Any] = field(default_factory=dict)


def _family(intent: Intent) -> str:
    if intent in WATER:
        return "water"
    if intent == Intent.vegetation_change:
        return "vegetation"
    return "optical"


def middle(w: DateWindow) -> date:
    return w.start + timedelta(days=(w.end - w.start).days // 2)


def sensor_order(intent: Intent, window: DateWindow, cfg: dict[str, Any]) -> list[str]:
    sc = cfg.get("scene", {})
    if intent not in WATER:
        return ["S2"]
    if middle(window).month in sc.get("monsoon_months", [6, 7, 8, 9]):
        return ["S1", "S2"]
    return ["S2", "S1"] if sc.get("sar_fallback", True) else ["S2"]


def _filter(sensor: str, intent: Intent, window: DateWindow, tile, cands: list[Scene], cfg) -> tuple[list[Scene], str]:
    """Return usable scenes, or an empty list and the reason the last filter stage removed them all."""
    sc = cfg.get("scene", {})
    mid, max_days = middle(window), int(sc.get("max_days_from_request", 12))
    stages = [
        (lambda s: s.sensor == sensor and abs((date.fromisoformat(s.date) - mid).days) <= max_days,
         lambda n: f"no {sensor} scene within {max_days} days of {mid}"),
        (lambda s: s.covers(tile), lambda n: f"{n} {sensor} scenes found but not covering this tile"),
        (lambda s: s.readable, lambda n: f"{n} {sensor} scenes not openly readable from the configured catalogues"),
        (lambda s: NEEDS[(sensor, _family(intent))] <= set(s.assets),
         lambda n: f"{n} {sensor} scenes missing bands {sorted(NEEDS[(sensor, _family(intent))])}"),
    ]
    if sensor == "S2":
        lim = float(sc.get("max_cloud_pct", 20))
        stages.append((lambda s: s.cloud_cover is not None and s.cloud_cover <= lim,
                       lambda n: f"cloud: {n} over {lim:g}% cloud"))
    pool = list(cands)
    for keep, why in stages:
        nxt = [s for s in pool if keep(s)]
        if not nxt:
            return [], why(len(pool))
        pool = nxt
    pool.sort(key=lambda s: (abs((date.fromisoformat(s.date) - mid).days), s.cloud_cover or 0, s.id))
    return pool, ""


def select_scenes(intent: Intent, window: DateWindow, tile, candidates: dict[str, list[Scene]],
                  cfg: dict[str, Any], sensors: Optional[list[str]] = None) -> Selection:
    order = sensors or sensor_order(intent, window, cfg)
    reasons: list[str] = []
    monsoon = intent in WATER and order[0] == "S1"
    for i, sensor in enumerate(order):
        usable, why = _filter(sensor, intent, window, tile, candidates.get(sensor, []), cfg)
        if usable:
            s = usable[0]
            if i == 0:
                base = ("monsoon month, so radar is used first because it sees through cloud" if monsoon
                        else f"{SENSOR_NAME[sensor]} scene closest to the requested date")
                reason = base
            else:
                reason = f"{SENSOR_NAME[order[0]]} unusable ({reasons[-1]}), so {SENSOR_NAME[sensor]} was used instead"
            return Selection(True, sensor, s, reason, fallback_used=i > 0,
                             considered={k: len(v) for k, v in candidates.items()})
        reasons.append(why)
    return Selection(False, reason="; ".join(reasons), considered={k: len(v) for k, v in candidates.items()})


def pair_for_change(intent: Intent, before: DateWindow, after: DateWindow, tile,
                    cands_before: dict[str, list[Scene]], cands_after: dict[str, list[Scene]],
                    cfg: dict[str, Any]) -> tuple[Selection, Selection]:
    """Pick the after scene first (the date the user cares about), then a matching before scene."""
    a = select_scenes(intent, after, tile, cands_after, cfg)
    if not a.ok:
        return Selection(False, reason="after date: " + a.reason), a
    pool = list(cands_before.get(a.sensor, []))
    note = f"same sensor ({SENSOR_NAME[a.sensor]}) as the after scene"
    if a.sensor == "S1" and a.scene.orbit_state:
        same = [s for s in pool if s.orbit_state == a.scene.orbit_state]
        if a.scene.relative_orbit is not None:
            rel = [s for s in same if s.relative_orbit == a.scene.relative_orbit]
            if rel:
                same, note = rel, f"same {a.scene.orbit_state} orbit and track ({a.scene.relative_orbit}) as the after scene"
            else:
                note = f"same {a.scene.orbit_state} orbit as the after scene"
        else:
            note = f"same {a.scene.orbit_state} orbit as the after scene"
        pool = same
    b = select_scenes(intent, before, tile, {a.sensor: pool}, cfg, sensors=[a.sensor])
    if b.ok:
        b.reason = note
    else:
        b.reason = "before date: " + b.reason
    return b, a
