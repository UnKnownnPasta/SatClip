"""Scripted SatClip demo: six questions that show every kind of answer, run live, end to end.

    cd backend && python ../tools/demo.py            # live run, about 5 to 15 minutes
    cd backend && python ../tools/demo.py --quick    # small boxes instead of whole districts

What it shows
  1. a published flood extent (whole district, radar through monsoon cloud)
  2. "did the flood spread": the change card, and when it abstains, the two follow-up extent
     questions it offers (SOLUTION risk 17) are run too
  3. a crop change answer (optical, two dates)
  4. an ambiguous district name: SatClip asks which one, measures nothing
  5. an out-of-scope question: refused by design
  6. a Hindi question with a Latin-script district name
It writes docs/demo/cards.json (every card and receipt) and docs/demo/TRANSCRIPT.md.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from fastapi.testclient import TestClient  # noqa: E402

from satclip.api.main import create_app  # noqa: E402
from satclip.config import settings  # noqa: E402

FULL = [
    ("Flood extent, published", {"text": "How much of Barpeta was under water on 2024-07-11?"}),
    ("Did the flood spread", {"text": "Did the flood spread in Barpeta between 2024-06-05 and 2024-07-11?"}),
    ("Crop change", {"text": "Did the crop decline in Darbhanga between 2024-03-01 and 2024-04-25?"}),
    ("Ambiguous district", {"text": "How much of Aurangabad was under water on 2024-08-10?"}),
    ("Out of scope", {"text": "Count the boats in Ernakulam"}),
    ("Hindi question", {"text": "Barpeta में 11 जुलाई 2024 को कितना इलाका पानी में डूबा था?"}),
]
BOX_A, BOX_B = "bbox: 90.95, 26.25, 91.10, 26.40", "bbox: 85.90, 26.05, 86.05, 26.20"
QUICK = [
    ("Flood extent, published", {"text": f"How much was under water on 2024-07-11? {BOX_A}"}),
    ("Did the flood spread", {"text": f"Did the flood spread between 2024-06-05 and 2024-07-11? {BOX_A}"}),
    ("Crop change", {"text": f"Did the crop decline between 2024-03-01 and 2024-04-25? {BOX_B}"}),
    FULL[3], FULL[4],
    ("Hindi question", {"text": f"11 जुलाई 2024 को कितना इलाका पानी में डूबा था? {BOX_A}"}),
]


def ask(client: TestClient, body: dict, timeout_s: float = 1800) -> dict:
    t0 = time.time()
    r = client.post("/v1/queries", json=body)
    if r.status_code != 202:
        return {"request": body, "http": r.status_code, "error": r.text, "seconds": round(time.time() - t0, 2)}
    out = r.json()
    card = out.get("card")
    while card is None and time.time() - t0 < timeout_s:
        time.sleep(0.5)
        job = client.get(f"/v1/jobs/{out['job_id']}").json()
        card = job["card"] if job["state"] in ("done", "failed") else None
    receipt = client.get(f"/v1/receipts/{card['receipt_id']}").json() if card and card.get("receipt_id") else None
    return {"request": body, "parsed": out["parsed"], "n_tiles": out["n_tiles"], "seconds": round(time.time() - t0, 2),
            "card": card, "receipt": receipt}


def describe(step: str, res: dict) -> list[str]:
    lines = [f"### {step}", "", f"**Question:** {res['request']['text']}", ""]
    if res.get("error"):
        return lines + [f"HTTP {res['http']}: {res['error']}", ""]
    c, p = res["card"] or {}, res["parsed"]
    kind = "Answer" if not c.get("abstained") else ("Needs one detail" if not res["n_tiles"] else "Not enough evidence")
    lines += [f"- Understood as: {p['understood_as']}",
              f"- Result: **{kind}**. {c.get('answer_text', '(no card)')}",
              f"- Tiles: {c.get('tiles_answered', 0)} of {res['n_tiles']} measured, {res['seconds']} s"]
    if c.get("confidence") is not None:
        lines.append(f"- Confidence: {c['confidence']} ({c.get('confidence_band')}), calibration: {c.get('calibration')}")
    if c.get("abstained"):
        lines.append(f"- Why: {c.get('reason')}")
        lines.append(f"- What would help: {c.get('next_step')}")
    if c.get("details"):
        lines.append("- Details: " + ", ".join(f"{k} {v}" for k, v in c["details"].items()))
    sc = c.get("scenes") or []
    if sc:
        lines.append(f"- Scenes ({len(sc)}): " + "; ".join(f"{s['id']} ({s['date']})" for s in sc[:3])
                     + (" ..." if len(sc) > 3 else ""))
    if c.get("follow_ups"):
        lines.append("- Offered next: " + "; ".join(f["label"] for f in c["follow_ups"]))
    if c.get("receipt_id"):
        lines.append(f"- Receipt: `{c['receipt_id']}`")
    return lines + [""]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true", help="small boxes instead of whole districts")
    ap.add_argument("--out", default=str(ROOT / "docs" / "demo"))
    a = ap.parse_args()
    client = TestClient(create_app(settings()))
    runs: list[tuple[str, dict]] = []
    for step, body in (QUICK if a.quick else FULL):
        res = ask(client, body)
        runs.append((step, res))
        print(f"{step}: {res.get('seconds')} s -> {(res.get('card') or {}).get('answer_text')}", flush=True)
        for fu in (res.get("card") or {}).get("follow_ups") or []:
            sub = ask(client, fu["request"])
            runs.append((f"{step}, follow-up: {fu['label']}", sub))
            print(f"  {fu['label']}: {sub.get('seconds')} s -> {(sub.get('card') or {}).get('answer_text')}", flush=True)
    # Warm cache: the same first question again is served from the tile cache.
    warm = ask(client, (QUICK if a.quick else FULL)[0][1])
    runs.append(("Warm cache: question 1 again", warm))
    print(f"warm repeat: {warm['seconds']} s", flush=True)

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())
    (out / "cards.json").write_text(json.dumps({"generated": stamp, "mode": "quick" if a.quick else "full",
                                                "runs": [{"step": s, **r} for s, r in runs]}, indent=1, ensure_ascii=False))
    md = [f"# SatClip scripted demo ({'quick' if a.quick else 'full'} mode)", "",
          f"Generated {stamp} by `tools/demo.py` against the live public catalogues "
          "(Planetary Computer Sentinel-1 RTC, Earth Search Sentinel-2). Every number below was measured in this run.", ""]
    for s, r in runs:
        md += describe(s, r)
    (out / "TRANSCRIPT.md").write_text("\n".join(md), encoding="utf-8")
    print(f"wrote {out / 'TRANSCRIPT.md'}")


if __name__ == "__main__":
    main()
