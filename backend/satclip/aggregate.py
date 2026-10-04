"""Combine tile results into one evidence card and decide abstention (SOLUTION.md section 6)."""
from __future__ import annotations

from typing import Any

from .models import EvidenceCard, Intent, Job, SceneRef, TileStatus

MIN_TILE_COVERAGE = 0.5  # abstain if fewer than half the tiles could be measured

_NEXT_STEP = {
    "out_of_scope": "Try a supported question, for example: 'How much of Barpeta was under water on 2026-07-05?'",
    "missing_area": "Pick an area on the map, or name a district.",
    "invalid_area": "The area box is not valid. Draw it again on the map.",
    "missing_dates": "Add a date, for example 2026-07-05.",
    "need_two_dates": "A change question needs two dates, for example 2026-06-15 and 2026-07-05.",
}


def band(conf: float, bands: list[dict[str, Any]]) -> str:
    for b in sorted(bands, key=lambda b: -b["min"]):
        if conf >= b["min"]:
            return b["label"]
    return "low"


def card_for_problems(job: Job) -> EvidenceCard:
    first = job.parsed.problems[0]
    return EvidenceCard(job_id=job.job_id, abstained=True, understood_as=job.parsed.understood_as,
                        answer_text="I can't answer this yet.", reason=first, next_step=_NEXT_STEP.get(first))


def aggregate(job: Job, trust: dict[str, Any]) -> EvidenceCard:
    ok = [r for r in job.results if r.status == TileStatus.ok and r.confidence is not None]
    total = max(job.tiles_total, 1)
    base = dict(job_id=job.job_id, understood_as=job.parsed.understood_as,
                tiles_total=job.tiles_total, tiles_answered=len(ok))
    if len(ok) / total < MIN_TILE_COVERAGE:
        reasons = sorted({r.reason for r in job.results if r.reason})
        return EvidenceCard(**base, abstained=True, answer_text="Insufficient evidence for this area and date.",
                            reason="; ".join(reasons)[:300] or "too few tiles could be measured",
                            next_step="Widen the date window, or try again after the next Sentinel-1 pass.")
    weights = [max(r.value or 0.0, 1e-6) for r in ok]
    conf = sum(w * r.confidence for w, r in zip(weights, ok)) / sum(weights)
    conf = conf * (len(ok) / total) ** 0.5 if len(ok) < total else conf  # missing tiles lower confidence
    value = round(sum(r.value or 0.0 for r in ok), 2)
    unit = ok[0].unit
    seen, scenes = set(), []
    for r in ok:
        for s in r.scenes:
            if s.get("id") not in seen:
                seen.add(s.get("id"))
                scenes.append(SceneRef(**{k: s.get(k) for k in ("id", "date", "sensor", "catalog")}))
    synthetic = any(r.params.get("synthetic") for r in ok)
    label = band(conf, trust.get("bands", []))
    if conf < float(trust.get("abstain_below", 0.6)):
        return EvidenceCard(**base, abstained=True, value=value, unit=unit, confidence=round(conf, 3),
                            confidence_band=label, scenes=scenes, answer_text="Insufficient evidence: confidence is below the publication threshold.",
                            reason="low_confidence", next_step="Try a narrower area or a date closer to a satellite pass.")
    noun = {Intent.water_extent: "under water", Intent.water_change: "newly under water",
            Intent.vegetation_change: "with vegetation decline"}.get(job.parsed.intent, "measured")
    text = f"About {value:g} {unit or ''} {noun} ({label} confidence, {conf:.2f})."
    return EvidenceCard(**base, abstained=False, value=value, unit=unit, confidence=round(conf, 3),
                        confidence_band=label, scenes=scenes, answer_text=text.replace("  ", " "),
                        observed_vs_inferred="synthetic test data" if synthetic else "observed")
