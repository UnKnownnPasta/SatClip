"""Scan the whole archive for papers that may challenge SatClip's novelty claims (M8).

For every archive entry this script searches the full text for signals of the six
ingredients of the SatClip combination claim (NOVELTY.md section 5):

  C1 calibrated per-answer confidence
  C2 threshold abstention with a next step
  C3 scene provenance or reproducible receipts
  C4 SAR-first or automatic sensor choice under cloud
  C5 CPU, edge or offline deployment
  C6 plain-language questions for non-experts (and India)

Keyword hits only shortlist papers. A hit means the paper *mentions* the topic,
not that its system *has* the ingredient; every shortlisted paper is then judged
by hand in NOVELTY.md section 5. Writes docs/verification/archive_scan.csv and
prints the shortlist (papers with signals in three or more ingredients and a
category that builds question-answering systems).

    python tools/novelty_scan.py
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "archive" / "papers"
OUT = ROOT / "docs" / "verification" / "archive_scan.csv"

SIGNALS = {
    "C1_calibration": r"calibrat|expected calibration error|\bECE\b|temperature scaling|platt|isotonic|conformal",
    "C2_abstention": r"abstain|abstention|reject option|selective (prediction|classification)|refus|insufficient evidence|I don.t know",
    "C3_provenance": r"provenance|receipt|reproducib|replay|scene id|audit",
    "C4_sar_switch": r"sentinel-1|\bSAR\b|radar",
    "C4b_cloud": r"cloud",
    "C5_cpu_offline": r"\bCPU\b|offline|edge device|on-?board|on-?prem|laptop|quantiz",
    "C6_plain_language": r"natural[- ]language|plain[- ]language|non-?expert|question",
    "C6b_india": r"\bIndia|Assam|Kerala|Bihar|ISRO|NRSC|Bhuvan",
}
SYSTEM_CATEGORIES = {"rs-vlm", "eo-agents", "rs-benchmark", "upcoming", "trust-calibration", "change-detection"}


def front_matter(text: str) -> dict:
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    out = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line and not line.startswith(" "):
                k, v = line.split(":", 1)
                out[k.strip()] = v.strip().strip('"')
    return out


def main() -> None:
    rows = []
    for path in sorted(PAPERS.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        fm = front_matter(text)
        flags = {k: bool(re.search(p, text, re.I)) for k, p in SIGNALS.items()}
        c4 = flags["C4_sar_switch"] and flags["C4b_cloud"]
        c6 = flags["C6_plain_language"]
        dims = [flags["C1_calibration"], flags["C2_abstention"], flags["C3_provenance"], c4, flags["C5_cpu_offline"], c6]
        rows.append({
            "id": fm.get("id", path.stem[:3]),
            "title": fm.get("title", ""),
            "year": fm.get("year", ""),
            "category": fm.get("category", ""),
            "C1_calibration": int(dims[0]),
            "C2_abstention": int(dims[1]),
            "C3_provenance": int(dims[2]),
            "C4_sar_under_cloud": int(dims[3]),
            "C5_cpu_offline": int(dims[4]),
            "C6_plain_language": int(dims[5]),
            "india": int(flags["C6b_india"]),
            "signal_count": sum(dims),
        })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    shortlist = [r for r in rows if r["signal_count"] >= 3 and r["category"] in SYSTEM_CATEGORIES]
    print(f"{len(rows)} papers scanned; {len(shortlist)} shortlisted for manual review -> {OUT.relative_to(ROOT)}")
    for k in ["C1_calibration", "C2_abstention", "C3_provenance", "C4_sar_under_cloud", "C5_cpu_offline", "C6_plain_language"]:
        print(f"  {k}: mentioned in {sum(r[k] for r in rows)}")
    for r in sorted(shortlist, key=lambda r: -r["signal_count"]):
        print(f"  A{r['id']} [{r['category']}] {r['signal_count']}  {r['title'][:80]}")


if __name__ == "__main__":
    main()
