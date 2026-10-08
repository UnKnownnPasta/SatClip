"""Receipt reproducibility check: re-run every question in a demo transcript from a cold start and
compare receipt hashes.

    cd backend && python ../tools/reproduce.py                    # uses docs/demo/cards.json
    cd backend && python ../tools/reproduce.py --cards other.json --limit 10

For each recorded run it builds a fresh API (empty tile cache), asks the same request, and compares
`output_hash` (tiles, scenes, values, confidences, the published answer) and `receipt_id` (the
above plus the parsed question). Writes docs/quality/reproducibility.json and prints a table.
A mismatch means the same question no longer gives the same evidence: a catalogue changed, a
scene was reprocessed, or the code is not deterministic. The report shows which field moved.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))
sys.path.insert(0, str(ROOT / "tools"))

from fastapi.testclient import TestClient  # noqa: E402

from demo import ask  # noqa: E402
from satclip.api.main import create_app  # noqa: E402
from satclip.config import settings  # noqa: E402


def first_difference(a: dict, b: dict) -> str:
    if not a or not b:
        return "missing receipt"
    if a["output"] != b["output"]:
        return f"output {a['output']} -> {b['output']}"
    ta, tb = {t["tile_id"]: t for t in a["tiles"]}, {t["tile_id"]: t for t in b["tiles"]}
    if ta.keys() != tb.keys():
        return f"tile set changed ({len(ta)} -> {len(tb)})"
    for k in sorted(ta):
        for f in ("status", "scenes", "value", "confidence", "params"):
            if ta[k].get(f) != tb[k].get(f):
                return f"tile {k} field {f}"
    return "parsed query changed" if a["parsed_query"] != b["parsed_query"] else "none"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cards", default=str(ROOT / "docs" / "demo" / "cards.json"))
    ap.add_argument("--limit", type=int, default=10)
    ap.add_argument("--out", default=str(ROOT / "docs" / "quality" / "reproducibility.json"))
    a = ap.parse_args()
    runs = [r for r in json.loads(Path(a.cards).read_text())["runs"]
            if r.get("receipt") and not r["step"].startswith("Warm cache")][: a.limit]
    rows = []
    for r in runs:
        client = TestClient(create_app(settings()))  # fresh queue and cache every time
        new = ask(client, r["request"])
        old_rec, new_rec = r["receipt"], new.get("receipt") or {}
        row = {"step": r["step"], "tiles": len(old_rec.get("tiles", [])),
               "receipt_id": old_rec.get("receipt_id"), "rerun_receipt_id": new_rec.get("receipt_id"),
               "output_hash_match": old_rec.get("output_hash") == new_rec.get("output_hash"),
               "receipt_match": old_rec.get("receipt_id") == new_rec.get("receipt_id"),
               "seconds": new.get("seconds")}
        row["difference"] = "none" if row["receipt_match"] else first_difference(old_rec, new_rec)
        rows.append(row)
        print(f"{row['step'][:50]:50s} tiles={row['tiles']:4d} output={'same' if row['output_hash_match'] else 'DIFF'} "
              f"receipt={'same' if row['receipt_match'] else 'DIFF'} ({row['difference']})", flush=True)
    rep = {"generated": time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime()), "source": Path(a.cards).name,
           "checked": len(rows), "output_hash_matches": sum(r["output_hash_match"] for r in rows),
           "receipt_matches": sum(r["receipt_match"] for r in rows), "rows": rows}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(rep, indent=1))
    print(f"{rep['receipt_matches']}/{rep['checked']} receipts reproduced exactly; wrote {a.out}")


if __name__ == "__main__":
    main()
