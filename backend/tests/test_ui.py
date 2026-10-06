"""M4: API support for the web UI (district picker, ambiguity chooser, UI config) and the static UI itself."""
import re
from pathlib import Path

from fastapi.testclient import TestClient

from satclip.api.main import create_app
from satclip.models import QueryRequest
from satclip.parser import parse

FRONTEND = Path(__file__).resolve().parents[2] / "frontend"


def test_picked_region_wins_over_text():
    p = parse(QueryRequest(text="How much was under water on 2024-07-11?", region="barpeta|assam"))
    assert p.region == "barpeta|assam" and p.place_name == "Barpeta, Assam" and not p.problems


def test_unknown_picked_region_falls_back_to_text():
    p = parse(QueryRequest(text="How much of Barpeta was under water on 2024-07-11?", region="nowhere|x"))
    assert p.region == "barpeta|assam"


def test_ambiguous_name_returns_keys_for_chooser():
    p = parse(QueryRequest(text="How much of Aurangabad was under water on 2024-08-10?"))
    assert "ambiguous_area" in p.problems
    assert len(p.candidate_keys) == len(p.candidates) >= 2
    for label, key in zip(p.candidates, p.candidate_keys):
        assert key.split("|")[0] in label.lower()
    # each key resolves to that district when sent back as a pick
    again = parse(QueryRequest(text=p.text, region=p.candidate_keys[0]))
    assert not again.problems and again.place_name == p.candidates[0]


def test_ui_config_and_static_ui():
    c = TestClient(create_app())
    cfg = c.get("/v1/ui-config").json()
    assert 0 < cfg["abstain_below"] < 1 and cfg["bands"] and cfg["examples"]
    assert all("text" in e and "label" in e for e in cfg["examples"])
    html = c.get("/").text
    for landmark in ('id="q"', 'role="combobox"', 'role="progressbar"', 'id="card"', 'id="map"', "vendor/leaflet/leaflet.js"):
        assert landmark in html
    assert c.get("/vendor/leaflet/leaflet.js").status_code == 200


def test_frontend_has_no_em_dashes_and_no_external_scripts():
    for f in FRONTEND.glob("*.*"):
        text = f.read_text(encoding="utf-8")
        assert "\u2014" not in text, f.name
        if f.suffix == ".html":
            assert not re.search(r'<script[^>]+src="https?://', text), "scripts must be vendored for offline installs"
