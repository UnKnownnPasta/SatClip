"""Receipts: canonical JSON plus a SHA-256 hash, so a re-run can prove it reproduced the answer."""
from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)


def digest(obj: Any) -> str:
    return hashlib.sha256(canonical(obj).encode()).hexdigest()


def build_receipt(parsed: dict, results: list[dict], card: dict) -> dict:
    tiles = sorted(
        ({k: r.get(k) for k in ("tile_id", "status", "value", "unit", "confidence", "scenes", "params")} for r in results),
        key=lambda r: r["tile_id"],
    )
    output = {k: card.get(k) for k in ("value", "unit", "confidence", "abstained")}
    body = {"schema": "satclip.receipt/1", "parsed_query": parsed, "tiles": tiles,
            "output": output, "output_hash": digest({"tiles": tiles, "output": output})}
    body["receipt_id"] = digest(body)[:16]
    return body
