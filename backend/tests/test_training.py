"""Tests for the M5 training and calibration code that runs without a GPU or network."""
import json
import random
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "training" / "lora"))
sys.path.insert(0, str(ROOT / "training" / "calibration"))

import schema  # noqa: E402


def test_parse_output_accepts_only_schema_json():
    good = '{"intent": "water_extent", "place": "Barpeta", "state": null, "dates": ["2024-07-11"], "refuse_reason": null}'
    assert schema.parse_output("Sure: " + good)["place"] == "Barpeta"
    assert schema.parse_output(good.replace("water_extent", "count_houses")) is None
    assert schema.parse_output(good.replace("2024-07-11", "11 July")) is None
    assert schema.parse_output("no json here") is None


def test_resolve_uses_gazetteer_and_window_rules():
    obj = {"intent": "water_change", "place": "Barpeta", "state": None, "dates": ["2024-06-05", "2024-07-11"],
           "refuse_reason": None}
    parsed = schema.resolve(obj, "barpeta me 5 june se 11 july tak baadh kitni badhi")
    assert parsed.intent.value == "water_change" and parsed.region == "barpeta|assam"
    assert len(parsed.windows) == 2 and parsed.problems == []
    amb = schema.resolve({**obj, "place": "Aurangabad"}, "Aurangabad flood 2024")
    assert amb.region is None and "ambiguous_area" in amb.problems and len(amb.candidates) == 2
    out = schema.resolve({**obj, "intent": "unsupported", "refuse_reason": "counting"}, "how many houses in Barpeta")
    assert "out_of_scope" in out.problems


def test_intent_builder_targets_are_consistent():
    import build_intent_data as B
    districts = json.loads((ROOT / "backend/satclip/resources/districts.json").read_text())["districts"]
    rng = random.Random(0)
    for _ in range(300):
        row = B.make(rng.choice(districts), rng, {"aurangabad"})
        t = row["target"]
        assert schema.parse_output(row["messages"][2]["content"]) == t
        if t["intent"] in ("water_change", "vegetation_change"):
            assert len(t["dates"]) in (0, 2)
        if t["intent"] == "unsupported":
            assert t["refuse_reason"] in ("counting", "forecast", "identity", "other")
        else:
            assert t["refuse_reason"] is None
    assert B.split_of("Barpeta|Assam") == B.split_of("Barpeta|Assam")


def test_sen1floods11_regrid_and_correctness_rule():
    pytest.importorskip("rasterio")
    import fit_water as F
    vv = np.full((4, 4), -10.0, dtype="float32")
    vv[:2, :2] = -20.0
    lab = np.zeros((4, 4), dtype="float32")
    lab[:2, :2] = 1
    lab[3, 3] = -1
    vv20, lab20 = F.to_working_grid(vv, lab, shift_db=1.0)
    assert vv20.shape == (2, 2) and vv20[0, 0] == pytest.approx(-19.0) and lab20[0, 0] == 1
    assert lab20[1, 1] == 0  # three labelled sub-pixels of land outvote one no-data pixel
    p = np.array([0.9, 0.9, 0.1, 0.1])
    y = np.array([1, 1, 0, 0], float)
    ece, mce, _ = F.ece_mce(p, y)
    assert ece == pytest.approx(0.1) and mce == pytest.approx(0.1)
    s = F.selective(p, y)
    assert s["coverage"] == 0.5 and s["error_when_published"] == 0.0
    spec = F.platt(np.array([0.1, 0.2, 0.8, 0.9] * 5), np.array([0, 0, 1, 1] * 5, float))
    assert spec["a"] > 0
