"""M2 data layer tests. Offline: STAC calls go through httpx.MockTransport with recorded
responses, COG reads use small GeoTIFFs written to a temp dir."""
import copy
import json
from datetime import date
from pathlib import Path

import httpx
import numpy as np
import pytest

from satclip.config import load_settings
from satclip.data.cog import read_window, scl_cloud_fraction, sign_href
from satclip.data.provider import DataProvider, search_cell
from satclip.data.scene import normalize_item
from satclip.data.select import pair_for_change, select_scenes, sensor_order
from satclip.data.stac import Endpoint, StacClient, StacError
from satclip.models import DateWindow, Intent

FIX = Path(__file__).parent / "fixtures" / "stac"
S2 = json.loads((FIX / "earth-search_s2_barpeta_2024-11.json").read_text())
S1 = json.loads((FIX / "planetary-computer_s1rtc_barpeta_2024-07.json").read_text())
TILE = (91.0, 26.3, 91.05, 26.35)
CFG = load_settings()


def W(a, b):
    return DateWindow(start=date.fromisoformat(a), end=date.fromisoformat(b))


class FakeClock:
    def __init__(self):
        self.t = 0.0

    def __call__(self):
        return self.t


def make_client(handler, **kw):
    eps = [Endpoint("es", "https://es.test/v1", "sentinel-2-l2a", "sentinel-1-grd", readable={"S1": False, "S2": True}),
           Endpoint("pc", "https://pc.test/v1", "sentinel-2-l2a", "sentinel-1-rtc", signing="planetary-computer")]
    return StacClient(eps, transport=httpx.MockTransport(handler), **kw)


# ---------- normalisation ----------

def test_normalize_earth_search_item():
    sc = normalize_item(S2["features"][0], catalog="earth-search")
    assert sc.sensor == "S2" and sc.epsg == 32646 and sc.date == "2024-11-16"
    assert set(sc.assets) >= {"green", "red", "nir", "scl"} and sc.covers(TILE)
    assert sc.evidence()["cloud_cover"] == 7.21


def test_normalize_planetary_computer_aliases_and_proj_code():
    item = copy.deepcopy(S2["features"][2])
    item["assets"] = {"B03": {"href": "g"}, "B08": {"href": "n"}, "SCL": {"href": "s"}}
    del item["properties"]["proj:epsg"]
    item["properties"]["proj:code"] = "EPSG:32646"
    sc = normalize_item(item)
    assert sc.assets == {"green": "g", "nir": "n", "scl": "s"} and sc.epsg == 32646


def test_normalize_s1_rtc():
    sc = normalize_item(S1["features"][0], catalog="planetary-computer", needs_signing="planetary-computer")
    assert sc.sensor == "S1" and sc.orbit_state == "ascending" and "vv" in sc.assets


# ---------- STAC client ----------

def test_search_posts_body_and_filters_cloud():
    seen = []

    def handler(req):
        seen.append(json.loads(req.content))
        return httpx.Response(200, json=S2)

    c = make_client(handler)
    out = c.search("S2", TILE, date(2024, 11, 5), date(2024, 11, 20), max_cloud=5)
    assert [s.id for s in out] == ["S2C_46RBQ_20241111_1_L2A"]  # 7% and 9% scenes dropped
    body = seen[0]
    assert body["collections"] == ["sentinel-2-l2a"] and body["query"]["eo:cloud_cover"]["lte"] == 5
    assert body["datetime"] == "2024-11-05T00:00:00Z/2024-11-20T23:59:59Z"


def test_failover_and_cooldown():
    clock, calls = FakeClock(), []

    def handler(req):
        calls.append(req.url.host)
        if req.url.host == "es.test":
            return httpx.Response(502)
        return httpx.Response(200, json=S2)

    c = make_client(handler, clock=clock, cooldown_s=60)
    assert c.search("S2", TILE, date(2024, 11, 5), date(2024, 11, 20))[0].catalog == "pc"
    assert c.health()["es"] == "cooldown"
    calls.clear()
    c.search("S2", (91.1, 26.3, 91.15, 26.35), date(2024, 11, 5), date(2024, 11, 20))
    assert calls == ["pc.test"]  # es skipped while cooling down
    clock.t = 61
    calls.clear()
    c.search("S2", (91.2, 26.3, 91.25, 26.35), date(2024, 11, 5), date(2024, 11, 20))
    assert calls[0] == "es.test"  # retried after cooldown


def test_all_fail_raises():
    c = make_client(lambda req: httpx.Response(500))
    with pytest.raises(StacError):
        c.search("S2", TILE, date(2024, 11, 5), date(2024, 11, 20))


def test_search_only_endpoint_skipped_for_s1():
    hosts = []

    def handler(req):
        hosts.append(req.url.host)
        return httpx.Response(200, json=S1)

    out = make_client(handler).search("S1", TILE, date(2024, 7, 1), date(2024, 7, 15))
    assert hosts == ["pc.test"] and out[0].needs_signing == "planetary-computer"


def test_search_cache_and_paging():
    n = {"calls": 0}
    page1 = {**S2, "features": S2["features"][:2],
             "links": [{"rel": "next", "href": "https://es.test/v1/search", "method": "POST", "body": {"token": "p2"}}]}
    page2 = {**S2, "features": S2["features"][2:], "links": []}

    def handler(req):
        n["calls"] += 1
        return httpx.Response(200, json=page2 if json.loads(req.content).get("token") == "p2" else page1)

    c = make_client(handler)
    assert len(c.search("S2", TILE, date(2024, 11, 5), date(2024, 11, 20))) == 3
    assert n["calls"] == 2
    c.search("S2", TILE, date(2024, 11, 5), date(2024, 11, 20))
    assert n["calls"] == 2 and c.log[-1]["cache_hit"]


# ---------- selection ----------

def scenes(fc, catalog="x", **kw):
    return [normalize_item(f, catalog=catalog, **kw) for f in fc["features"]]


def test_monsoon_water_prefers_sar():
    assert sensor_order(Intent.water_extent, W("2024-07-05", "2024-07-17"), CFG) == ["S1", "S2"]
    assert sensor_order(Intent.water_extent, W("2024-11-05", "2024-11-17"), CFG) == ["S2", "S1"]
    assert sensor_order(Intent.vegetation_change, W("2024-07-05", "2024-07-17"), CFG) == ["S2"]


def test_select_monsoon_sar_first():
    sel = select_scenes(Intent.water_extent, W("2024-07-05", "2024-07-17"), TILE,
                        {"S1": scenes(S1), "S2": scenes(S2)}, CFG)
    assert sel.sensor == "S1" and not sel.fallback_used and "monsoon" in sel.reason
    assert sel.scene.date == "2024-07-11"  # closest to window middle (07-11)


def test_select_optical_closest_then_sar_fallback_when_cloudy():
    sel = select_scenes(Intent.water_extent, W("2024-11-05", "2024-11-17"), TILE, {"S2": scenes(S2), "S1": scenes(S1)}, CFG)
    assert sel.sensor == "S2" and sel.scene.id == "S2C_46RBQ_20241111_1_L2A"
    cloudy = copy.deepcopy(S2)
    for f in cloudy["features"]:
        f["properties"]["eo:cloud_cover"] = 80
    s1_nov = copy.deepcopy(S1)
    s1_nov["features"][0]["properties"]["datetime"] = "2024-11-10T11:57:28Z"
    sel = select_scenes(Intent.water_extent, W("2024-11-05", "2024-11-17"), TILE,
                        {"S2": scenes(cloudy), "S1": scenes(s1_nov)}, CFG)
    assert sel.sensor == "S1" and sel.fallback_used and "3 over 20% cloud" in sel.reason


def test_vegetation_abstains_on_cloud_instead_of_swapping_sensor():
    cloudy = copy.deepcopy(S2)
    for f in cloudy["features"]:
        f["properties"]["eo:cloud_cover"] = 90
    sel = select_scenes(Intent.vegetation_change, W("2024-11-05", "2024-11-17"), TILE,
                        {"S2": scenes(cloudy), "S1": scenes(S1)}, CFG)
    assert not sel.ok and sel.reason.startswith("cloud")


def test_scene_must_cover_tile_and_be_readable():
    far = (95.0, 20.0, 95.05, 20.05)
    sel = select_scenes(Intent.water_extent, W("2024-11-05", "2024-11-17"), far, {"S2": scenes(S2), "S1": []}, CFG)
    assert not sel.ok and "not covering" in sel.reason
    sel = select_scenes(Intent.water_extent, W("2024-07-05", "2024-07-17"), TILE,
                        {"S1": scenes(S1, readable=False), "S2": []}, CFG)
    assert not sel.ok and "not openly readable" in sel.reason


def test_change_pair_same_sensor_and_orbit():
    before = copy.deepcopy(S1)
    for f, d in zip(before["features"], ["2024-05-30T11:57:00Z", "2024-05-28T00:12:00Z"]):
        f["properties"]["datetime"] = d
    before["features"][1]["properties"]["sat:orbit_state"] = "descending"
    before["features"][1]["bbox"] = S1["features"][0]["bbox"]
    b, a = pair_for_change(Intent.water_change, W("2024-05-24", "2024-06-05"), W("2024-07-05", "2024-07-17"), TILE,
                           {"S1": scenes(before), "S2": []}, {"S1": scenes(S1), "S2": []}, CFG)
    assert a.sensor == b.sensor == "S1"
    assert b.scene.orbit_state == a.scene.orbit_state == "ascending"
    assert "same ascending orbit" in b.reason


# ---------- provider ----------

def test_search_cell_shares_searches_across_tiles():
    assert search_cell((91.01, 26.31, 91.06, 26.36), 1.0) == (91.0, 26.0, 92.0, 27.0)
    n = {"calls": 0}

    def handler(req):
        n["calls"] += 1
        return httpx.Response(200, json=S2)

    p = DataProvider(make_client(handler), CFG)
    for i in range(5):  # five neighbouring tiles, one catalogue call
        t = (91.0 + i * 0.05, 26.3, 91.05 + i * 0.05, 26.35)
        p.for_tile(Intent.vegetation_change, [W("2024-11-05", "2024-11-17")], t)
    assert n["calls"] == 1


# ---------- COG reads ----------

@pytest.fixture
def utm_cog(tmp_path):
    rasterio = pytest.importorskip("rasterio")
    from rasterio.transform import from_origin
    from rasterio.warp import transform as wt
    xs, ys = wt("EPSG:4326", "EPSG:32646", [91.0], [26.35])
    x0, y0 = xs[0] - 1000, ys[0] + 1000
    arr = np.full((1000, 1000), 100, dtype="uint16")
    arr[:, 500:] = 200  # east half brighter
    path = tmp_path / "b.tif"
    with rasterio.open(path, "w", driver="GTiff", width=1000, height=1000, count=1, dtype="uint16",
                       crs="EPSG:32646", transform=from_origin(x0, y0, 10, 10), nodata=0,
                       tiled=True, blockxsize=256, blockysize=256, compress="deflate") as dst:
        dst.write(arr, 1)
    return path


def test_read_window_lonlat_bbox(utm_cog):
    r = read_window(str(utm_cog), (91.0, 26.3, 91.05, 26.35), res_m=20)
    assert r.crs == "EPSG:32646"
    assert 200 < r.data.shape[0] < 330 and 200 < r.data.shape[1] < 330  # ~5 km at 20 m
    assert r.valid_fraction > 0.95
    assert np.nanmin(r.data) == 100 and np.nanmax(r.data) == 200  # west 80% dark, east 20% bright
    assert np.nanmean(r.data[:, :20]) == 100 and np.nanmean(r.data[:, -20:]) == 200


def test_read_window_outside_is_nan(utm_cog):
    r = read_window(str(utm_cog), (91.3, 26.3, 91.35, 26.35), res_m=50)
    assert r.valid_fraction == 0.0


def test_scl_cloud_fraction():
    scl = np.array([[4, 4, 9, 9], [0, 0, 8, 5]], dtype="float32")  # 2 nodata ignored, 3 of 6 cloudy
    assert scl_cloud_fraction(scl) == pytest.approx(0.5)
    assert scl_cloud_fraction(np.array([[0, 0]], dtype="float32")) == 1.0


def test_sign_href_planetary_computer_only():
    fetch = lambda coll: ("st=1&sig=abc", 9e12)
    assert sign_href("https://x/a.tif", "planetary-computer", "sentinel-1-rtc", fetch) == "https://x/a.tif?st=1&sig=abc"
    assert sign_href("https://x/a.tif", None, "sentinel-2-l2a", fetch) == "https://x/a.tif"


# ---------- API ----------

def test_scenes_endpoint_validates_and_searches(monkeypatch):
    from fastapi.testclient import TestClient
    from satclip.api.main import create_app
    app = create_app(CFG)
    app.state.stac = make_client(lambda req: httpx.Response(200, json=S2))
    tc = TestClient(app)
    assert tc.get("/v1/scenes", params={"bbox": "1,2,3", "start": "2024-11-01", "end": "2024-11-20"}).status_code == 422
    r = tc.get("/v1/scenes", params={"bbox": "91.0,26.3,91.05,26.35", "start": "2024-11-05", "end": "2024-11-20"})
    assert r.status_code == 200 and r.json()["count"] == 3 and r.json()["scenes"][0]["covers_request"]
