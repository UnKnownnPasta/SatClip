"""M3 instrument tests. Offline: a fake DataProvider serves synthetic rasters on a real UTM grid,
so thresholds, areas, region clipping, overlays and abstention are all checked exactly."""
import copy
import time
from datetime import date

import numpy as np
import pytest

rasterio = pytest.importorskip("rasterio")
from rasterio.transform import from_bounds  # noqa: E402
from rasterio.warp import transform_bounds  # noqa: E402

from satclip import calibration, gazetteer  # noqa: E402
from satclip.config import load_settings  # noqa: E402
from satclip.data import provider as prov_mod  # noqa: E402
from satclip.data.cog import RasterWindow  # noqa: E402
from satclip.data.scene import Scene  # noqa: E402
from satclip.data.select import Selection  # noqa: E402
from satclip.instruments import get  # noqa: E402
from satclip.instruments import landcover  # noqa: E402
from satclip.models import DateWindow, Intent, QueryRequest, TileJob, TileStatus  # noqa: E402
from satclip.parser import parse  # noqa: E402
from satclip.tiling import tile_area_km2  # noqa: E402

TILE = (91.0, 26.3, 91.05, 26.35)
RNG = np.random.default_rng(7)
CFG = load_settings(environ={})


def W(a, b):
    return DateWindow(start=date.fromisoformat(a), end=date.fromisoformat(b))


def window(arr, bbox, res=20.0):
    l, b, r, t = transform_bounds("EPSG:4326", "EPSG:32646", *bbox, densify_pts=21)
    h, w = arr.shape
    return RasterWindow(data=arr.astype("float32"), crs="EPSG:32646", transform=from_bounds(l, b, r, t, w, h),
                        res_m=res, valid_fraction=float(np.isfinite(arr).mean()), bounds=(l, b, r, t))


def scene(sid, sensor, d, orbit="ascending"):
    bands = {"vv": "x"} if sensor == "S1" else {k: "x" for k in ("red", "green", "blue", "nir", "scl")}
    return Scene(id=sid, sensor=sensor, datetime=d + "T05:00:00Z", bbox=(90, 25, 92, 27), collection="c",
                 assets=bands, catalog="fake", cloud_cover=2.0, orbit_state=orbit if sensor == "S1" else None)


class FakeProvider:
    """Serves band arrays by (scene id, band). Arrays are generated at the tile shape for any bbox."""

    def __init__(self, selections, bands, cloud=None):
        self.cfg = copy.deepcopy(CFG)
        self.selections, self.bands, self.cloud = selections, bands, cloud or {}

    def for_tile(self, intent, windows, tile):
        return self.selections

    def read(self, sc, band, tile, res_m=20.0):
        arr = self.bands[(sc.id, band)]
        if res_m == 10.0 and arr.shape == SHAPE:
            arr = np.kron(arr, np.ones((2, 2)))
        return window(arr, tile, res_m)

    def tile_is_clear(self, sc, tile, res_m=20.0):
        if sc.sensor != "S2":
            return True, 0.0, None
        frac = self.cloud.get(sc.id, 0.0)
        return frac <= 0.3, frac, self.read(sc, "scl", tile, res_m)


SHAPE = (278, 250)  # about 5.5 x 5 km at 20 m


def flood_db(water_cols=0.4, water=-21.0, land=-10.0):
    a = RNG.normal(land, 1.5, SHAPE)
    a[:, : int(SHAPE[1] * water_cols)] = RNG.normal(water, 1.5, (SHAPE[0], int(SHAPE[1] * water_cols)))
    return 10 ** (a / 10)  # linear backscatter, as RTC assets store it


def job(instrument, intent, windows, region=None, bbox=TILE):
    return TileJob(job_id="j", tile_id="t", bbox=bbox, intent=intent, windows=windows, instrument=instrument, region=region)


@pytest.fixture(autouse=True)
def tmp_masks(tmp_path, monkeypatch):
    monkeypatch.setitem(CFG, "outputs", {"masks_dir": str(tmp_path / "masks"), "read_res_m": 20})
    yield
    prov_mod.set_provider(None)


def use(p):
    p.cfg["outputs"] = CFG["outputs"]
    prov_mod.set_provider(p)
    return p


# ---------- SAR water ----------

def test_sar_water_fits_threshold_and_measures_area(identity_calibration):
    s = scene("S1_after", "S1", "2024-07-11")
    use(FakeProvider([Selection(True, "S1", s, "monsoon month, radar first")], {("S1_after", "vv"): flood_db(0.4)}))
    _, fn = get("sar_water_otsu")
    r = fn(job("sar_water_otsu", Intent.water_extent, [W("2024-07-05", "2024-07-17")]))
    assert r.status == TileStatus.ok
    fit = r.params["fit"]
    assert fit["source"] == "fitted" and -18 < fit["threshold_db"] < -13 and fit["ashman_d"] > 4
    measured = r.params["measured_km2"]
    assert r.value == pytest.approx(0.4 * measured, rel=0.05)
    assert r.confidence >= 0.8 and r.scenes[0]["id"] == "S1_after"
    assert r.mask and r.mask["href"].startswith("/v1/masks/") and r.mask["bounds"] == list(TILE)


def test_sar_no_water_uses_default_threshold_and_stays_confident(identity_calibration):
    s = scene("S1_dry", "S1", "2024-07-11")
    use(FakeProvider([Selection(True, "S1", s, "r")], {("S1_dry", "vv"): flood_db(0.0)}))
    r = get("sar_water_otsu")[1](job("sar_water_otsu", Intent.water_extent, [W("2024-07-05", "2024-07-17")]))
    assert r.params["fit"]["source"] == "default" and r.params["fit"]["threshold_db"] == -17.0
    assert r.value < 0.05 and 0.6 <= r.confidence < 0.8


def test_sar_ambiguous_tile_gets_low_confidence():
    s = scene("S1_mush", "S1", "2024-07-11")
    use(FakeProvider([Selection(True, "S1", s, "r")], {("S1_mush", "vv"): 10 ** (RNG.normal(-18, 1.0, SHAPE) / 10)}))
    r = get("sar_water_otsu")[1](job("sar_water_otsu", Intent.water_extent, [W("2024-07-05", "2024-07-17")]))
    assert r.confidence < 0.5  # most pixels sit within 1 dB of the threshold


def test_selection_failure_becomes_abstention_reason():
    use(FakeProvider([Selection(False, reason="no S1 scene within 12 days of 2024-07-11")], {}))
    r = get("sar_water_otsu")[1](job("sar_water_otsu", Intent.water_extent, [W("2024-07-05", "2024-07-17")]))
    assert r.status == TileStatus.abstain and "no S1 scene" in r.reason


def test_logratio_change_finds_new_water():
    b, a = scene("S1_b", "S1", "2024-06-01"), scene("S1_a", "S1", "2024-07-11")
    use(FakeProvider([Selection(True, "S1", b, "same ascending orbit"), Selection(True, "S1", a, "monsoon")],
                     {("S1_b", "vv"): flood_db(0.1), ("S1_a", "vv"): flood_db(0.4)}))
    r = get("sar_logratio_change")[1](job("sar_logratio_change", Intent.water_change,
                                          [W("2024-05-26", "2024-06-07"), W("2024-07-05", "2024-07-17")]))
    m = r.params["measured_km2"]
    assert r.status == TileStatus.ok and r.value == pytest.approx(0.3 * m, rel=0.08)
    assert r.params["water_before_km2"] == pytest.approx(0.1 * m, rel=0.1) and r.params["receded_km2"] < 0.02 * m
    assert [s["role"] for s in r.scenes] == ["before", "after"]


# ---------- vegetation ----------

def s2_bands(sid, ndvi, water_cols=0.0):
    red = np.full(SHAPE, 0.05)
    nir = red * (1 + ndvi) / (1 - ndvi)
    green = np.full(SHAPE, 0.06)
    if water_cols:
        k = int(SHAPE[1] * water_cols)
        nir[:, :k], green[:, :k], red[:, :k] = 0.02, 0.08, 0.04
    scl = np.full(SHAPE, 4.0)
    return {(sid, "red"): red, (sid, "nir"): nir, (sid, "green"): green, (sid, "blue"): green * 0.8, (sid, "scl"): scl}


def test_ndvi_difference_measures_decline():
    b, a = scene("S2_b", "S2", "2024-08-01"), scene("S2_a", "S2", "2024-09-20")
    after = np.full(SHAPE, 0.7)
    after[:, : SHAPE[1] // 2] = 0.3
    bands = {**s2_bands("S2_b", np.full(SHAPE, 0.7)), **s2_bands("S2_a", after)}
    use(FakeProvider([Selection(True, "S2", b, "pair"), Selection(True, "S2", a, "closest")], bands))
    r = get("ndvi_difference")[1](job("ndvi_difference", Intent.vegetation_change,
                                      [W("2024-07-26", "2024-08-07"), W("2024-09-14", "2024-09-26")]))
    m = r.params["measured_km2"]
    assert r.status == TileStatus.ok and r.value == pytest.approx(0.5 * m, rel=0.03)
    assert r.params["mean_ndvi_before"] == pytest.approx(0.7, abs=0.01) and r.confidence > 0.7


def test_ndvi_abstains_on_cloudy_tile():
    b, a = scene("S2_b", "S2", "2024-08-01"), scene("S2_a", "S2", "2024-09-20")
    bands = {**s2_bands("S2_b", np.full(SHAPE, 0.7)), **s2_bands("S2_a", np.full(SHAPE, 0.7))}
    use(FakeProvider([Selection(True, "S2", b, "p"), Selection(True, "S2", a, "c")], bands, cloud={"S2_a": 0.8}))
    r = get("ndvi_difference")[1](job("ndvi_difference", Intent.vegetation_change,
                                      [W("2024-07-26", "2024-08-07"), W("2024-09-14", "2024-09-26")]))
    assert r.status == TileStatus.abstain and r.reason.startswith("cloud: 80%")


# ---------- description and land cover ----------

def test_index_caption_breakdown():
    s = scene("S2_x", "S2", "2024-11-11")
    use(FakeProvider([Selection(True, "S2", s, "closest")], s2_bands("S2_x", np.full(SHAPE, 0.7), water_cols=0.25)))
    r = get("index_caption")[1](job("index_caption", Intent.describe, [W("2024-11-05", "2024-11-17")]))
    bd = r.params["breakdown"]
    assert bd["water"] == pytest.approx(0.25, abs=0.01) and bd["dense vegetation"] == pytest.approx(0.75, abs=0.01)


def test_landcover_abstains_when_model_missing(monkeypatch):
    s = scene("S2_x", "S2", "2024-11-11")
    use(FakeProvider([Selection(True, "S2", s, "closest")], s2_bands("S2_x", np.full(SHAPE, 0.7))))

    def boom(cfg):
        raise ImportError("no torch")
    monkeypatch.setattr(landcover, "_load_clip", boom)
    r = get("zero_shot_landcover")[1](job("zero_shot_landcover", Intent.land_cover, [W("2024-11-05", "2024-11-17")]))
    assert r.status == TileStatus.abstain and "model unavailable" in r.reason


# ---------- region clipping ----------

def test_region_clipping_reduces_measured_area():
    from shapely.geometry import box
    from satclip.tiling import tiles_for_bbox
    outline = gazetteer.outline_lonlat("barpeta|assam")
    edge = next(tb for _, tb in tiles_for_bbox(outline.bounds, 0.05)
                if 0.3 < outline.intersection(box(*tb)).area / box(*tb).area < 0.7)  # straddles the boundary
    sc = scene("S1_a", "S1", "2024-07-11")
    use(FakeProvider([Selection(True, "S1", sc, "r")], {("S1_a", "vv"): flood_db(0.0)}))
    fn = get("sar_water_otsu")[1]
    full = fn(job("sar_water_otsu", Intent.water_extent, [W("2024-07-05", "2024-07-17")], bbox=edge))
    clipped = fn(job("sar_water_otsu", Intent.water_extent, [W("2024-07-05", "2024-07-17")], region="barpeta|assam", bbox=edge))
    assert clipped.params["measured_km2"] < 0.9 * full.params["measured_km2"]
    outside = fn(job("sar_water_otsu", Intent.water_extent, [W("2024-07-05", "2024-07-17")], region="barpeta|assam",
                     bbox=(88.0, 22.0, 88.05, 22.05)))
    assert outside.status == TileStatus.abstain and "outside" in outside.reason


# ---------- gazetteer and parser ----------

def test_gazetteer_and_parser_regions():
    p = parse(QueryRequest(text="How much of Barpeta was under water on 2024-07-11?"))
    assert p.region == "barpeta|assam" and p.place_name == "Barpeta, Assam" and p.problems == []
    amb = parse(QueryRequest(text="Did crops decline in Aurangabad between 2024-08-01 and 2024-09-20?"))
    assert amb.problems == ["ambiguous_area"] and len(amb.candidates) == 2
    ok = parse(QueryRequest(text="Did crops decline in Aurangabad, Bihar between 2024-08-01 and 2024-09-20?"))
    assert ok.region == "aurangabad|bihar"
    assert gazetteer.find("mon water levels")[0] is None  # short names need their capital letter
    assert gazetteer.meta()["license"] == "ODbL 1.0" and gazetteer.meta()["count"] > 700


# ---------- calibration ----------

def test_calibration_isotonic_and_fit():
    cal = calibration.Calibrator({"method": "isotonic", "points": [[0, 0.1], [1, 0.9]]})
    assert cal(0.5) == pytest.approx(0.5) and cal(2.0) == 0.9 and not cal.fitted
    spec = calibration.fit_isotonic([0.1, 0.2, 0.3, 0.6, 0.7, 0.9], [0, 1, 0, 1, 1, 1])
    ys = [p[1] for p in spec["points"]]
    assert ys == sorted(ys) and spec["fitted"]
    # tiny blocks are pooled, so a single chip cannot create a cliff
    spec = calibration.fit_isotonic([i / 20 for i in range(20)], [0, 1] * 10, min_block=5)
    assert all(b >= a for a, b in zip([p[1] for p in spec["points"]], [p[1] for p in spec["points"]][1:]))
    assert len(spec["points"]) <= 4


def test_calibration_files():
    """Shipped maps: water extent is fitted on Sen1Floods11 (M5) and carries its ledger; the others are
    still labelled placeholders, so the card can never claim a calibration that does not exist."""
    calibration.load.cache_clear()
    water = calibration.load("sar_water_otsu")
    assert water.fitted and water.status == "fitted"
    assert water.spec["fit"]["n"] >= 100 and "Sen1Floods11" in water.spec["fit"]["dataset"]
    xs = [i / 20 for i in range(21)]
    ys = [water(x) for x in xs]
    assert all(0 <= y <= 1 for y in ys) and ys == sorted(ys)
    for name in ("ndvi_difference", "index_caption"):
        assert calibration.load(name).status.startswith("placeholder")
    change = calibration.load("sar_logratio_change")
    assert change.status.startswith("borrowed from sar_water_otsu") and not change.fitted
    assert change(0.9) == pytest.approx(water(0.9))


# ---------- end to end through the API ----------

def test_api_end_to_end_district_card(tmp_path, identity_calibration):
    from fastapi.testclient import TestClient
    from satclip.api.main import create_app
    cfg = copy.deepcopy(CFG)
    cfg["intents"]["water_extent"] = "sar_water_otsu"
    s = scene("S1_after", "S1", "2024-07-11")
    use(FakeProvider([Selection(True, "S1", s, "monsoon month, so radar is used first")], {("S1_after", "vv"): flood_db(0.3)}))
    app = create_app(cfg)
    c = TestClient(app)
    r = c.post("/v1/queries", json={"text": "How much of Barpeta was under water on 2024-07-11?"}).json()
    n = r["n_tiles"]
    full = len(__import__("satclip.tiling", fromlist=["x"]).tiles_for_bbox(tuple(gazetteer.get("barpeta|assam")["bbox"]), 0.05))
    assert 0 < n < full  # tiles outside the outline are not queued
    for _ in range(200):
        job_ = c.get(f"/v1/jobs/{r['job_id']}").json()
        if job_["state"] == "done":
            break
        time.sleep(0.1)
    card = job_["card"]
    assert not card["abstained"] and card["region_name"] == "Barpeta, Assam"
    assert card["instrument"] == "sar_water_otsu" and card["calibration"].startswith("placeholder")
    assert card["caveats"] and card["selection_notes"] == ["monsoon month, so radar is used first"]
    assert card["value"] == pytest.approx(0.3 * card["details"]["measured_km2"], rel=0.06)
    assert len(card["masks"]) == card["tiles_answered"]
    png = c.get(card["masks"][0]["href"])
    assert png.status_code == 200 and png.content[:4] == b"\x89PNG"
    assert c.get("/v1/regions", params={"q": "barp"}).json()["regions"][0]["key"] == "barpeta|assam"
    assert c.get("/v1/regions/barpeta|assam").json()["geometry"]["type"] in ("Polygon", "MultiPolygon")
    assert c.get("/v1/masks/../../etc/passwd").status_code == 404
