"""Confidence calibration (SOLUTION.md section 6, archive A026, A031).

Each instrument computes a raw quality score in [0, 1] from transparent signals (histogram
separability, ambiguous-pixel share, clear-sky share). A calibration file per instrument maps
that raw score to a probability that the tile answer is within tolerance of a reference map.

Files live in `config/calibration/<instrument>.json`:
  {"method": "isotonic", "points": [[raw, p], ...], "fitted": true, "fit": {...}}
  {"method": "logistic", "a": 4.0, "b": -2.0, "fitted": true}
  {"method": "temperature", "T": 1.7, "fitted": true}       (softmax models, used by zero-shot CLIP)
  {"method": "inherit", "from": "sar_water_otsu", "fitted": false}   (borrow a parent instrument's map)
  {"method": "regimes", "by": "new_water_share", "cut": 0.05, "maps": {"no_change": {...}, "change": {...}},
   "fitted": true}   (one map per answer regime; run 7, sar_logratio_change: "no meaningful new water" and
   "X sq km of new water" answers are right at very different rates, so one map cannot serve both)
Until M5 fits them on labelled data, the shipped files are marked `"fitted": false`, and every
card says the confidence is uncalibrated. No hidden claims.
"""
from __future__ import annotations

import bisect
import json
import math
from functools import lru_cache
from pathlib import Path
from typing import Any

CAL_DIR = Path(__file__).resolve().parents[2] / "config" / "calibration"


class Calibrator:
    def __init__(self, spec: dict[str, Any], name: str = ""):
        self.spec, self.name = spec, name
        self.method = spec.get("method", "identity")
        self.fitted = bool(spec.get("fitted", False))
        if self.method == "isotonic":
            pts = sorted(spec["points"])
            self.xs, self.ys = [p[0] for p in pts], [p[1] for p in pts]

    def __call__(self, raw: float, regime: str | None = None) -> float:
        raw = min(max(float(raw), 0.0), 1.0)
        if self.method == "regimes":
            maps = {k: Calibrator(v, f"{self.name}:{k}") for k, v in self.spec["maps"].items()}
            if regime in maps:
                return maps[regime](raw)
            return min(m(raw) for m in maps.values())  # regime unknown: take the more cautious map
        if self.method == "isotonic":
            i = bisect.bisect_left(self.xs, raw)
            if i <= 0:
                return self.ys[0]
            if i >= len(self.xs):
                return self.ys[-1]
            x0, x1, y0, y1 = self.xs[i - 1], self.xs[i], self.ys[i - 1], self.ys[i]
            return y0 + (y1 - y0) * (raw - x0) / ((x1 - x0) or 1)
        if self.method == "logistic":
            return 1 / (1 + math.exp(-(self.spec["a"] * raw + self.spec["b"])))
        if self.method == "inherit":  # borrow a fitted map from the instrument this one is built on
            return load(self.spec["from"])(raw)
        return raw

    def temperature(self) -> float:
        return float(self.spec.get("T", 1.0)) if self.method == "temperature" else 1.0

    @property
    def status(self) -> str:
        if self.method == "inherit":
            parent = load(self.spec["from"])
            if parent.fitted:
                return f"borrowed from {self.spec['from']} (this instrument is not yet fitted on its own labels)"
        return "fitted" if self.fitted else "placeholder (not yet fitted on labelled data)"


@lru_cache(maxsize=32)
def load(name: str, cal_dir: str | None = None) -> Calibrator:
    path = Path(cal_dir or CAL_DIR) / f"{name}.json"
    if not path.exists():
        return Calibrator({"method": "identity", "fitted": False}, name)
    return Calibrator(json.loads(path.read_text()), name)


def fit_isotonic(raw: list[float], correct: list[int], min_block: int = 5) -> dict[str, Any]:
    """Pool-adjacent-violators isotonic fit (archive A127), used by training/calibration.
    Blocks smaller than `min_block` samples are pooled with a neighbour first, so a handful of chips
    cannot create a cliff in the map. Returns a spec dict whose points are the block centres."""
    pairs = sorted(zip(raw, correct))
    blocks = [[float(x), float(y), 1] for x, y in pairs]  # [mean x, mean y, weight]

    def merge(i: int) -> None:
        x0, y0, w0 = blocks[i]
        x1, y1, w1 = blocks[i + 1]
        blocks[i] = [(x0 * w0 + x1 * w1) / (w0 + w1), (y0 * w0 + y1 * w1) / (w0 + w1), w0 + w1]
        del blocks[i + 1]

    i = 0
    while i < len(blocks) - 1:  # PAV
        if blocks[i][1] > blocks[i + 1][1]:
            merge(i)
            i = max(i - 1, 0)
        else:
            i += 1
    i = 0
    while len(blocks) > 1 and i < len(blocks):  # pool tiny blocks into the smaller neighbour (keeps monotonicity)
        if blocks[i][2] >= min_block:
            i += 1
            continue
        if i == len(blocks) - 1:
            merge(i - 1)
            i = max(i - 2, 0)
        elif i == 0 or blocks[i + 1][2] <= blocks[i - 1][2]:
            merge(i)
        else:
            merge(i - 1)
            i -= 1
    points = []
    for x, y, _ in blocks:
        pt = [round(x, 4), round(y, 4)]
        if points and pt[0] == points[-1][0]:
            points[-1] = pt
        else:
            points.append(pt)
    return {"method": "isotonic", "points": points, "fitted": True, "fit": {"n": len(raw), "blocks": len(blocks)}}
