"""Run 8 (M6): follow-up extents for abstained change cards (SOLUTION risk 17), receipts, demo script."""
from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

from satclip.aggregate import aggregate, extent_follow_ups
from satclip.models import DateWindow, Intent, Job, ParsedQuery, QueryRequest, TileResult, TileStatus
from satclip.parser import parse
from satclip.receipt import build_receipt

TRUST = {"abstain_below": 0.6, "bands": [{"min": 0.8, "label": "high"}, {"min": 0.6, "label": "low"}]}
W = [DateWindow(start=date(2024, 5, 30), end=date(2024, 6, 11)), DateWindow(start=date(2024, 7, 5), end=date(2024, 7, 17))]


def _job(intent: Intent, conf: float, n: int = 4) -> Job:
    p = ParsedQuery(text="t", intent=intent, windows=W if intent == Intent.water_change else W[:1],
                    understood_as="x", region="barpeta|assam", place_name="Barpeta, Assam")
    job = Job(job_id="j1", parsed=p, tiles_total=n)
    job.results = [TileResult(job_id="j1", tile_id=f"t{i}", status=TileStatus.ok, value=1.0, unit="km2",
                              confidence=conf, params={"measured_km2": 30.0}) for i in range(n)]
    return job


def test_abstained_change_card_offers_extent_on_each_date():
    card = aggregate(_job(Intent.water_change, 0.2), TRUST)
    assert card.abstained and card.reason == "low_confidence"
    assert [f["label"] for f in card.follow_ups] == ["Water before: 2024-06-05", "Water after: 2024-07-11"]
    req = card.follow_ups[1]["request"]
    assert req["region"] == "barpeta|assam" and req["windows"] == [{"start": "2024-07-05", "end": "2024-07-17"}]
    # The follow-up request must parse into a runnable water-extent question on the same window and district.
    p = parse(QueryRequest(**req))
    assert p.intent == Intent.water_extent and not p.problems and p.region == "barpeta|assam"
    assert p.windows[0].start == date(2024, 7, 5) and p.windows[0].end == date(2024, 7, 17)
    assert "extent on each date" in card.next_step


def test_follow_ups_only_for_change_questions():
    assert extent_follow_ups(_job(Intent.water_extent, 0.2)) == []
    assert aggregate(_job(Intent.water_extent, 0.2), TRUST).follow_ups == []
    assert aggregate(_job(Intent.water_change, 0.95), TRUST).follow_ups == []  # published: nothing to offer


def test_follow_ups_keep_a_drawn_box():
    job = _job(Intent.water_change, 0.2)
    job.parsed.region, job.parsed.place_name, job.parsed.bbox = None, None, (90.95, 26.25, 91.1, 26.4)
    req = extent_follow_ups(job)[0]["request"]
    assert req["bbox"] == [90.95, 26.25, 91.1, 26.4] and "region" not in req
    assert not parse(QueryRequest(**req)).problems


def test_receipt_is_order_independent_and_sensitive_to_values():
    job = _job(Intent.water_extent, 0.9)
    res = [r.model_dump(mode="json") for r in job.results]
    card = aggregate(job, TRUST).model_dump(mode="json")
    a = build_receipt(job.parsed.model_dump(mode="json"), res, card)
    b = build_receipt(job.parsed.model_dump(mode="json"), list(reversed(res)), card)
    assert a["receipt_id"] == b["receipt_id"] and a["output_hash"] == b["output_hash"]
    res[0]["value"] = 2.0
    c = build_receipt(job.parsed.model_dump(mode="json"), res, card)
    assert c["output_hash"] != a["output_hash"]


def test_demo_script_covers_six_kinds_of_answer():
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
    import demo
    assert len(demo.FULL) == 6 and len(demo.QUICK) == 6
    kinds = {}
    for step, body in demo.FULL:
        p = parse(QueryRequest(**body))
        kinds[step] = (p.intent.value, p.problems[:1])
    assert kinds["Flood extent, published"] == ("water_extent", [])
    assert kinds["Did the flood spread"] == ("water_change", [])
    assert kinds["Crop change"] == ("vegetation_change", [])
    assert kinds["Ambiguous district"][1] == ["ambiguous_area"]
    assert kinds["Out of scope"][1] == ["out_of_scope"]
    assert kinds["Hindi question"] == ("water_extent", [])


def test_resize_is_deterministic_and_nan_aware():
    import numpy as np
    from satclip.data.cog import _average, _nearest
    a = np.arange(36, dtype="float32").reshape(6, 6)
    a[0, 0] = np.nan
    av = _average(a, 3, 3)
    assert av.shape == (3, 3) and np.isclose(av[0, 0], (1 + 6 + 7) / 3) and np.isclose(av[2, 2], (28 + 29 + 34 + 35) / 4)
    assert np.isnan(_average(np.full((4, 4), np.nan, "float32"), 2, 2)).all()
    assert np.array_equal(_nearest(a, 3, 3)[1:, 1:], a[[3, 5]][:, [3, 5]])


def test_read_window_decimates_in_numpy(tmp_path):
    import numpy as np
    import rasterio
    from rasterio.transform import from_origin
    from satclip.data.cog import read_window
    path = tmp_path / "t.tif"
    data = np.arange(200 * 200, dtype="uint16").reshape(200, 200) + 1
    with rasterio.open(path, "w", driver="GTiff", width=200, height=200, count=1, dtype="uint16", crs="EPSG:4326",
                       transform=from_origin(80.0, 21.0, 0.0001, 0.0001), nodata=0, tiled=True,
                       blockxsize=64, blockysize=64) as ds:
        ds.write(data, 1)
    box = (80.002, 20.988, 80.012, 20.998)
    a = read_window(str(path), box, res_m=0.0002, resampling="average")
    b = read_window(str(path), box, res_m=0.0002, resampling="average")
    assert a.data.shape == (50, 50) and np.array_equal(a.data, b.data)
    native = read_window(str(path), box)
    assert native.data.shape == (100, 100)
    assert np.isclose(a.data[0, 0], native.data[:2, :2].mean())
