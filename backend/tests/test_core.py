import copy
from datetime import date

import pytest
from fastapi.testclient import TestClient

from satclip.api.main import create_app
from satclip.config import load_settings
from satclip.models import Intent, QueryRequest
from satclip.parser import parse
from satclip.receipt import digest
from satclip.tiling import tile_area_km2, tiles_for_bbox


@pytest.fixture()
def cfg():
    c = copy.deepcopy(load_settings(environ={}))
    c["intents"] = {k: "synthetic" for k in c["intents"]}
    return c


def test_env_override():
    c = load_settings(environ={"SATCLIP_QUEUE__BACKEND": "redis", "SATCLIP_TRUST__ABSTAIN_BELOW": "0.7"})
    assert c["queue"]["backend"] == "redis" and c["trust"]["abstain_below"] == 0.7


def test_tiles_are_deterministic_and_cover_bbox():
    a = tiles_for_bbox((90.8, 26.15, 91.35, 26.8), 0.05)
    b = tiles_for_bbox((90.81, 26.16, 91.0, 26.3), 0.05)
    assert len(a) == 11 * 13
    assert {t for t, _ in b} <= {t for t, _ in a}  # overlapping AOIs share tile IDs
    assert 25 < tile_area_km2(a[0][1]) < 35  # about 5.5 km x 5 km at 26N


@pytest.mark.parametrize("text,intent", [
    ("How much of Barpeta is under water on 2026-07-05?", Intent.water_extent),
    ("Did the flood spread in Barpeta between 2026-06-15 and 2026-07-05?", Intent.water_change),
    ("Did the crop decline in Darbhanga between 2026-06-01 and 2026-09-01?", Intent.vegetation_change),
    ("Count the cars in Ernakulam", Intent.unsupported),
    ("Will it flood tomorrow in Barpeta?", Intent.unsupported),
])
def test_intents(text, intent):
    assert parse(QueryRequest(text=text)).intent == intent


def test_parser_problems():
    p = parse(QueryRequest(text="Did the flood spread in Barpeta since 2026-07-05?"))
    assert "need_two_dates" in p.problems
    p = parse(QueryRequest(text="How much water is there on 2026-07-05?"))
    assert "missing_area" in p.problems
    p = parse(QueryRequest(text="water extent bbox: 91.0, 26.2, 91.1, 26.3 on 2026-07-05"))
    assert p.problems == [] and p.bbox == (91.0, 26.2, 91.1, 26.3)
    assert p.windows[0].start == date(2026, 6, 29)


def test_end_to_end_inline(cfg):
    app = create_app(cfg)
    c = TestClient(app)
    assert c.get("/health").json()["status"] == "ok"
    r = c.post("/v1/queries", json={"text": "How much is under water on 2026-07-05?", "bbox": [91.0, 26.2, 91.2, 26.4]})
    assert r.status_code == 202
    body = r.json()
    assert body["n_tiles"] == 16 and "water extent" in body["parsed"]["understood_as"]
    job = app.state.queue.wait(body["job_id"])
    card = job.card
    assert card.tiles_total == 16 and card.receipt_id
    assert card.observed_vs_inferred == "synthetic test data" or card.abstained
    rec = c.get(f"/v1/receipts/{card.receipt_id}").json()
    assert rec["output_hash"] == digest({"tiles": rec["tiles"], "output": rec["output"]})
    # SSE stream replays all tiles then the card
    ev = c.get(f"/v1/jobs/{body['job_id']}/events").text
    assert ev.count("event: tile") == 16 and "event: card" in ev


def test_cache_and_reproducibility(cfg):
    app = create_app(cfg)
    c = TestClient(app)
    q = {"text": "water on 2026-07-05", "bbox": [91.0, 26.2, 91.1, 26.3]}
    j1 = app.state.queue.wait(c.post("/v1/queries", json=q).json()["job_id"])
    j2 = app.state.queue.wait(c.post("/v1/queries", json=q).json()["job_id"])
    assert all(r.cache_hit for r in j2.results)
    r1 = c.get(f"/v1/receipts/{j1.card.receipt_id}").json()
    r2 = c.get(f"/v1/receipts/{j2.card.receipt_id}").json()
    assert r1["output_hash"] == r2["output_hash"]


def test_out_of_scope_abstains_immediately(cfg):
    c = TestClient(create_app(cfg))
    body = c.post("/v1/queries", json={"text": "Count the cars in Ernakulam"}).json()
    assert body["n_tiles"] == 0 and body["card"]["abstained"] and body["card"]["reason"] == "out_of_scope"
    assert body["card"]["next_step"]


def test_not_implemented_instrument_abstains():
    cfg = load_settings(environ={})
    cfg["intents"] = {"water_extent": "nonexistent"}
    app = create_app(cfg)
    c = TestClient(app)
    jid = c.post("/v1/queries", json={"text": "water on 2026-07-05", "bbox": [91.0, 26.2, 91.1, 26.3]}).json()["job_id"]
    card = app.state.queue.wait(jid).card
    assert card.abstained and "not implemented" in card.reason


def test_area_limit(cfg):
    cfg["tiling"]["max_tiles_per_job"] = 10
    c = TestClient(create_app(cfg))
    r = c.post("/v1/queries", json={"text": "water on 2026-07-05", "bbox": [90.0, 26.0, 91.0, 27.0]})
    assert r.status_code == 413


def test_tiles_do_not_spill_over_float_edges():
    t = tiles_for_bbox((85.90, 26.05, 86.05, 26.20), 0.05)
    assert len(t) == 9 and min(b[0] for _, b in t) == pytest.approx(85.90)
