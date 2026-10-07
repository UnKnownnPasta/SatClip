"""Run 7: water instrument v1.1 (VH), shared change core, multi-format dates, Indian Q&A labels, Kuro Siwo regrid."""
import sys
from datetime import date
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "training" / "lora"))
sys.path.insert(0, str(ROOT / "training" / "calibration"))

from satclip.instruments.water import classify_sar_change, classify_sar_water, fit_sar_threshold  # noqa: E402
from satclip.models import Intent, QueryRequest  # noqa: E402
from satclip.parser import classify_intent, dates_in_text, parse  # noqa: E402


def _scene(rng, vv_water, vh_water, shape=(120, 120)):
    vv = rng.normal(-8, 1.2, shape)
    vh = rng.normal(-15, 1.2, shape)
    vv[vv_water] = rng.normal(-22, 1.0, int(vv_water.sum()))
    vh[vh_water] = rng.normal(-27, 1.0, int(vh_water.sum()))
    return vv.astype("float32"), vh.astype("float32")


def test_vh_rule_catches_water_that_is_bright_in_vv():
    rng = np.random.default_rng(0)
    open_w = np.zeros((120, 120), bool)
    open_w[:, :40] = True
    rough = np.zeros((120, 120), bool)
    rough[:, 40:70] = True                       # rough water / flooded vegetation: VV stays bright, VH is dark
    vv, vh = _scene(rng, open_w, open_w | rough)
    valid = np.ones_like(open_w)
    w_vv, q_vv = classify_sar_water(vv, valid)
    w_both, q_both = classify_sar_water(vv, valid, None, vh)
    assert q_vv["polarisations"] == "VV" and q_both["polarisations"] == "VV+VH"
    assert abs(w_vv.mean() - 40 / 120) < 0.03
    assert abs(w_both.mean() - 70 / 120) < 0.03
    assert q_both["vh_threshold_db"] < -18


def test_vh_rule_adds_nothing_on_dry_land():
    rng = np.random.default_rng(1)
    water = np.zeros((120, 120), bool)
    water[:, :50] = True
    vv, vh = _scene(rng, water, water)
    valid = np.ones_like(water)
    assert abs(classify_sar_water(vv, valid, None, vh)[0].mean() - classify_sar_water(vv, valid)[0].mean()) < 0.01


def test_change_core_uses_either_polarisation():
    rng = np.random.default_rng(2)
    before_w = np.zeros((120, 120), bool)
    before_w[:, :30] = True
    after_w = np.zeros((120, 120), bool)
    after_w[:, :60] = True
    vv_b, vh_b = _scene(rng, before_w, before_w)
    vv_a, vh_a = _scene(rng, before_w, after_w)        # new water dark only in VH
    valid = np.ones_like(after_w)
    fit = fit_sar_threshold(vv_a)
    water, q = classify_sar_water(vv_a, valid, fit, vh_a)
    a = {"water": water, "valid": valid, "values": vv_a, "vh": vh_a, "quality": q,
         "fit": {**fit, "vh_threshold_db": q["vh_threshold_db"]}}
    ch = classify_sar_change(a, vv_b, vh_b)
    assert abs(ch["new"].mean() - 30 / 120) < 0.03
    assert ch["water_b"].mean() < 30 / 120 + 0.03
    assert 0 <= ch["raw"] <= 1


def test_dates_in_indian_formats():
    assert dates_in_text("11/07/2024 se 5-8-2024 tak") == [date(2024, 7, 11), date(2024, 8, 5)]
    assert dates_in_text("on 11th July, 2024 and Aug 3 2024") == [date(2024, 7, 11), date(2024, 8, 3)]
    assert dates_in_text("११ जुलाई २०२४ को") == [date(2024, 7, 11)]
    assert dates_in_text("31/02/2024") == []
    assert dates_in_text("bbox: 90.95, 26.25, 91.10, 26.40 on 2024-07-08") == [date(2024, 7, 8)]


def test_two_dates_make_a_water_question_a_change_question():
    assert classify_intent("Barpeta paani 2024-06-05 aur 2024-07-11", 2) == Intent.water_change
    p = parse(QueryRequest(text="बारपेटा Barpeta में 11 जुलाई 2024 को बाढ़ का क्षेत्र"))
    assert p.intent == Intent.water_extent and p.region == "barpeta|assam" and len(p.windows) == 1
    assert classify_intent("Barpeta me kitne ghar doobe?") == Intent.unsupported


def test_india_qa_only_writes_clear_cut_answers():
    import random
    from build_india_qa import chip_bbox, qa_from_shares, wc_tile
    assert wc_tile(90.97, 26.32) == "N24E090" and wc_tile(76.3, 9.9) == "N09E075"
    b = chip_bbox(91.0, 26.3)
    assert abs((b[3] - b[1]) * 111_320 - 2560) < 5
    qa = {k: a for _, a, k in qa_from_shares({"cropland": 0.7, "open water": 0.005, "built-up": 0.2, "tree cover": 0.095},
                                             random.Random(0))}
    assert qa["presence:cropland"] == "yes" and qa["presence:open water"] == "no"
    assert "presence:tree cover" not in qa          # 9.5% is neither clearly present nor clearly absent
    assert qa["dominant"] == "cropland" and "urban_rural" not in qa and qa["water_share"] == "almost none"


def test_kurosiwo_regrid_and_labels():
    from fit_change import label20, to20
    lin = np.full((4, 4), 0.01, "float32")
    assert np.allclose(to20(lin, 1.0), -19.0, atol=1e-4)
    mask = np.array([[2, 2, 0, 0], [2, 0, 0, 0], [1, 1, 0, 2], [1, 1, 0, 0]], "float32")
    flood, ok = label20(mask, np.ones_like(mask))
    assert flood.tolist() == [[True, False], [False, False]] and ok.all()
