"""Combine tile results into one evidence card and decide abstention (SOLUTION.md section 6)."""
from __future__ import annotations

from collections import Counter
from math import erf, sqrt
from typing import Any

from .models import EvidenceCard, Intent, Job, SceneRef, TileStatus

MIN_TILE_COVERAGE = 0.5  # abstain if fewer than half the tiles could be measured

_NEXT_STEP = {
    "out_of_scope": "Try a supported question, for example: 'How much of Barpeta was under water on 2026-07-05?'",
    "missing_area": "Pick an area on the map, or name a district.",
    "invalid_area": "The area box is not valid. Draw it again on the map.",
    "missing_dates": "Add a date, for example 2026-07-05.",
    "need_two_dates": "A change question needs two dates, for example 2026-06-15 and 2026-07-05.",
    "ambiguous_area": "Several districts share this name. Add the state, for example 'Aurangabad, Bihar'.",
}


def band(conf: float, bands: list[dict[str, Any]]) -> str:
    for b in sorted(bands, key=lambda b: -b["min"]):
        if conf >= b["min"]:
            return b["label"]
    return "low"


CAVEATS = {
    "sar_water_otsu": ["Radar can miss water under dense vegetation or in narrow channels, and can mistake smooth surfaces "
                       "(tarmac, dry sand, radar shadow in hills) for water.",
                       "No terrain mask is applied yet, so steep slopes may add false water."],
    "sar_logratio_change": ["Change compares two passes on the same orbit; it shows where water appeared, not why.",
                            "Wind-roughened water and wet soil can hide or mimic change."],
    "ndvi_difference": ["NDVI measures greenness, not yield. Harvest, flooding, drought and crop damage can all lower it, "
                        "so the cause is not determined.",
                        "Compare dates in the same crop season; normal phenology also changes NDVI."],
    "zero_shot_landcover": ["Experimental: the land-cover model was trained mostly on sub-metre aerial imagery, and 10 m "
                            "Sentinel-2 is outside that range. Treat classes as indicative."],
    "index_caption": ["A description from spectral indices only: 'other' mixes built-up, bare and fallow land."],
}


def card_for_problems(job: Job) -> EvidenceCard:
    first = job.parsed.problems[0]
    nxt = _NEXT_STEP.get(first)
    if first == "ambiguous_area" and job.parsed.candidates:
        nxt = "Several districts share this name: " + "; ".join(job.parsed.candidates) + ". Add the state to your question."
    return EvidenceCard(job_id=job.job_id, abstained=True, understood_as=job.parsed.understood_as,
                        answer_text="I can't answer this yet.", reason=first, next_step=nxt,
                        region_name=job.parsed.place_name)


def _scenes(ok) -> list[SceneRef]:
    seen, out = set(), []
    for r in ok:
        for s in r.scenes:
            if s.get("id") not in seen:
                seen.add(s.get("id"))
                out.append(SceneRef(**{k: s.get(k) for k in ("id", "date", "sensor", "catalog")}))
    return sorted(out, key=lambda s: (s.date, s.id))


def _top_reasons(results, n: int = 3) -> str:
    counts = Counter(r.reason for r in results if r.reason)
    return "; ".join(f"{why} ({k} tiles)" if k > 1 else why for why, k in counts.most_common(n))


def _breakdown(ok) -> dict[str, float]:
    tot: dict[str, float] = {}
    area = 0.0
    for r in ok:
        a = float(r.params.get("measured_km2") or r.value or 0)
        area += a
        for k, v in (r.params.get("breakdown") or {}).items():
            tot[k] = tot.get(k, 0.0) + v * a
    return {k: round(v / area, 3) for k, v in sorted(tot.items(), key=lambda kv: -kv[1])} if area else {}


def _sum(ok, key: str) -> float:
    return round(sum(float(r.params.get(key) or 0) for r in ok), 2)


def _area_confidence(ok) -> float | None:
    """Confidence that the TOTAL area is within +/-20%. Tile errors share one scene and one method, so
    they are treated as fully correlated (the conservative case): total sd = sum of tile sds.
    P = erf(0.2 / (sd_rel * sqrt 2)), times the area-weighted evidence factor, then the instrument's
    calibration map (identity until M5 fits it)."""
    if not ok or any(r.params.get("sigma_abs_km2") is None for r in ok):
        return None
    from .calibration import load as load_cal
    sd = sum(float(r.params["sigma_abs_km2"]) for r in ok)
    total = sum(float(r.value or 0) for r in ok)
    floor = sum(float(r.params.get("sigma_floor_km2") or 0) for r in ok)
    rel = sd / max(total, floor, 1e-9)
    p = 1.0 if rel == 0 else erf(0.2 / (rel * sqrt(2)))
    w = [max(float(r.value or 0), 1e-6) for r in ok]
    factor = sum(wi * float(r.params.get("evidence_factor", 1.0)) for wi, r in zip(w, ok)) / sum(w)
    return load_cal(str(ok[0].params.get("instrument", ""))) (p * factor)


def aggregate(job: Job, trust: dict[str, Any]) -> EvidenceCard:
    ok = [r for r in job.results if r.status == TileStatus.ok and r.confidence is not None]
    total = max(job.tiles_total, 1)
    instrument = next((r.params.get("instrument") for r in job.results if r.params.get("instrument")), None)
    p0 = ok[0].params if ok else {}
    notes = sorted({r.params.get(k) for r in ok for k in ("selection", "pairing") if r.params.get(k)})
    base = dict(job_id=job.job_id, understood_as=job.parsed.understood_as, tiles_total=job.tiles_total,
                tiles_answered=len(ok), instrument=instrument, region_name=job.parsed.place_name,
                caveats=CAVEATS.get(instrument or "", []), selection_notes=notes,
                method=p0.get("method"), calibration=p0.get("calibration"))
    if len(ok) / total < MIN_TILE_COVERAGE:
        reason = _top_reasons(job.results)[:400] or "too few tiles could be measured"
        if "cloud" in reason and job.parsed.intent not in (Intent.water_extent, Intent.water_change):
            nxt = ("This question needs optical imagery, which clouds block. Try dates outside the monsoon, "
                   "or ask about water instead, which radar can measure through cloud.")
        else:
            nxt = "Widen the date window, or try again after the next Sentinel-1 pass (every 6 to 12 days)."
        return EvidenceCard(**base, abstained=True, answer_text="Insufficient evidence for this area and date.",
                            reason=reason, scenes=_scenes(ok), next_step=nxt)
    conf = _area_confidence(ok)
    if conf is None:  # instruments without an area-error model: area-weighted mean of tile confidences
        weights = [max(float(r.params.get("measured_km2") or 1.0), 1e-6) for r in ok]
        conf = sum(w * r.confidence for w, r in zip(weights, ok)) / sum(weights)
    if len(ok) < total:
        conf *= (len(ok) / total) ** 0.5  # tiles that could not be measured lower confidence
    value = round(sum(r.value or 0.0 for r in ok), 2)
    unit = ok[0].unit
    measured = _sum(ok, "measured_km2")
    synthetic = any(r.params.get("synthetic") for r in ok)
    label = band(conf, trust.get("bands", []))
    masks = [{"tile_id": r.tile_id, **r.mask} for r in ok if r.mask]
    intent = job.parsed.intent
    breakdown, details = None, {"measured_km2": measured}
    if intent == Intent.water_change:
        details.update(water_before_km2=_sum(ok, "water_before_km2"), water_after_km2=_sum(ok, "water_after_km2"),
                       receded_km2=_sum(ok, "receded_km2"))
    elif intent == Intent.vegetation_change:
        details.update(vegetated_before_km2=_sum(ok, "vegetated_before_km2"), gain_km2=_sum(ok, "gain_km2"))
    elif intent in (Intent.land_cover, Intent.describe):
        breakdown = _breakdown(ok)
    fallback = sum(1 for r in ok if r.params.get("fallback_used"))
    if fallback:
        details["tiles_on_fallback_sensor"] = fallback
    common = dict(**base, value=value, unit=unit, confidence=round(conf, 3), confidence_band=label, scenes=_scenes(ok),
                  masks=masks, breakdown=breakdown, details=details)
    if conf < float(trust.get("abstain_below", 0.6)):
        return EvidenceCard(**common, abstained=True,
                            answer_text="Insufficient evidence: confidence is below the publication threshold.",
                            reason="low_confidence", next_step="Try a narrower area or a date closer to a satellite pass.")
    where = f" of {job.parsed.place_name}" if job.parsed.place_name else ""
    def km(x: float) -> str:
        return f"{x:,.0f}" if x >= 100 else (f"{x:.1f}" if x >= 1 else f"{x:.2f}")
    pct = f", {value / measured:.0%} of the {km(measured)} sq km measured" if measured and unit == "km2" else ""
    if intent in (Intent.land_cover, Intent.describe) and breakdown:
        parts = [f"{k} {v:.0%}" for k, v in list(breakdown.items())[:4]]
        lead = "Mostly" if list(breakdown.values())[0] >= 0.5 else "Largest share:"
        text = f"{lead} {parts[0]}" + (f", then {', '.join(parts[1:])}" if len(parts) > 1 else "") + \
               f" across {km(measured)} sq km{where}"
    else:
        noun = {Intent.water_extent: "under water", Intent.water_change: "newly under water",
                Intent.vegetation_change: "with a clear fall in greenness"}.get(intent, "measured")
        text = f"About {km(value)} sq km{where} {noun}{pct}"
    text += f" ({label} confidence, {conf:.2f})."
    return EvidenceCard(**common, abstained=False, answer_text=text,
                        observed_vs_inferred="synthetic test data" if synthetic else "observed")
