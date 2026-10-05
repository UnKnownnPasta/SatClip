"""Run real questions end to end against the live public catalogues, in-process:
    python -m satclip.livecheck                 # default demo questions
    python -m satclip.livecheck "question" ...   # your own
Prints each evidence card (answer, confidence, scenes, timings) and writes them to
backend/runtime/livecheck.json for the demo and the deck.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from fastapi.testclient import TestClient

from .api.main import create_app
from .config import settings

QUESTIONS = [
    # Small boxes keep the default run quick; district-wide runs are in docs/VERIFICATION.md.
    "How much was under water on 2024-07-08? bbox: 90.95, 26.25, 91.10, 26.40",
    "Did the flood spread between 2024-06-05 and 2024-07-08? bbox: 90.95, 26.25, 91.10, 26.40",
    "Did the crop decline between 2024-10-01 and 2024-11-20? bbox: 85.90, 26.05, 86.05, 26.20",
    "Describe this area on 2025-03-15 bbox: 85.90, 26.05, 86.05, 26.20",
    "What is the land cover here on 2025-03-15? bbox: 85.90, 26.05, 86.05, 26.20",
    "Count the boats in Ernakulam",
]


def run(questions: list[str], timeout_s: float = 900) -> list[dict]:
    c = TestClient(create_app(settings()))
    out = []
    for q in questions:
        t0 = time.time()
        r = c.post("/v1/queries", json={"text": q})
        if r.status_code != 202:
            out.append({"question": q, "error": r.text})
            print(q, "->", r.status_code, r.text)
            continue
        body = r.json()
        card = body.get("card")
        while card is None and time.time() - t0 < timeout_s:
            time.sleep(1)
            job = c.get(f"/v1/jobs/{body['job_id']}").json()
            card = job["card"] if job["state"] == "done" else None
        secs = round(time.time() - t0, 1)
        out.append({"question": q, "seconds": secs, "n_tiles": body["n_tiles"], "card": card})
        print(f"\n## {q}\n  {secs}s, {body['n_tiles']} tiles")
        if card:
            print("  answer:", card["answer_text"])
            print("  reason:", card.get("reason"), "| next:", card.get("next_step"))
            print("  scenes:", [(s["id"], s["date"]) for s in card.get("scenes", [])][:4])
            print("  notes:", card.get("selection_notes"), "| details:", card.get("details"))
            print("  breakdown:", card.get("breakdown"), "| tiles:", card["tiles_answered"], "/", card["tiles_total"])
    path = Path(__file__).resolve().parents[1] / "runtime" / "livecheck.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=1))
    return out


if __name__ == "__main__":
    run(sys.argv[1:] or QUESTIONS)
