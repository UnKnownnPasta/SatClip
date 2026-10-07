"""Convert RSVQA (archive A011) into chat JSONL for LoRA fine-tuning and evaluation.

RSVQA-LR: Sentinel-2 RGB tiles of the Netherlands, 256 x 256 px at 10 m, questions of four types
(presence, comparison, rural_urban, count). Files on Zenodo record 6344334, layout:
  LR_split_{train,val,test}_{images,questions,answers}.json   (only entries with "active": true are used)
  Images_LR.zip -> Images_LR/{img_id}.tif

Why SatClip trains on it at all: the language layer has to *explain* an evidence card in plain words
and answer simple "is there water / is it urban" follow-ups about the shown image. Counting questions
are kept for evaluation only and are mapped to a refusal in training, because SatClip refuses counts
by design (SOLUTION.md non-goals): the model learns to say it cannot count from 10 m imagery.

    python training/lora/build_rsvqa.py --download            # fetch the ~110 MB LR release into training/.cache
    python training/lora/build_rsvqa.py --split test --max 2000
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from schema import ROOT  # noqa: E402

CACHE = ROOT / "training" / ".cache" / "rsvqa_lr"
OUT = ROOT / "training" / "data" / "rsvqa_lr"
ZENODO = "https://zenodo.org/records/6344334/files/{}?download=1"
SYSTEM = ("You look at one satellite image and answer briefly. Answer yes or no, rural or urban, or a short "
          "phrase. If a question asks for an exact count, say you cannot count objects reliably at this resolution.")
COUNT_REFUSAL = "I cannot count objects reliably at 10 m resolution."


def download() -> None:
    import httpx
    CACHE.mkdir(parents=True, exist_ok=True)
    names = [f"LR_split_{s}_{k}.json" for s in ("train", "val", "test") for k in ("images", "questions", "answers")]
    for name in names + ["Images_LR.zip"]:
        dst = CACHE / name
        if dst.exists():
            continue
        print("downloading", name, flush=True)
        with httpx.stream("GET", ZENODO.format(name), follow_redirects=True, timeout=600) as r:
            r.raise_for_status()
            with open(dst, "wb") as f:
                for chunk in r.iter_bytes(1 << 20):
                    f.write(chunk)
    if not (CACHE / "Images_LR").exists():
        zipfile.ZipFile(CACHE / "Images_LR.zip").extractall(CACHE)


def load_split(split: str) -> list[dict]:
    def active(name: str) -> list[dict]:
        d = json.loads((CACHE / f"LR_split_{split}_{name}.json").read_text())
        return [x for x in next(iter(d.values())) if x.get("active")]
    answers = {a["question_id"]: a["answer"] for a in active("answers")}
    rows = []
    for q in active("questions"):
        if q["id"] in answers:
            rows.append({"qid": q["id"], "img_id": q["img_id"], "type": q["type"], "question": q["question"].strip(),
                         "answer": str(answers[q["id"]]).strip()})
    return rows


def to_png(img_id: int) -> Path:
    """RSVQA-LR tiles are already 8-bit RGB GeoTIFFs; re-save as PNG so any processor can open them."""
    png = OUT / "images" / f"{img_id}.png"
    if not png.exists():
        import rasterio
        from images import save_png
        with rasterio.open(CACHE / "Images_LR" / f"{img_id}.tif") as ds:
            save_png(ds.read([1, 2, 3]).transpose(1, 2, 0), png)
    return png


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--download", action="store_true")
    ap.add_argument("--split", choices=["train", "val", "test"], default="train")
    ap.add_argument("--max", type=int, default=0, help="sample at most N questions (stratified by type)")
    ap.add_argument("--seed", type=int, default=3)
    args = ap.parse_args()
    if args.download:
        download()
    rows = load_split(args.split)
    if args.max and len(rows) > args.max:
        rng = random.Random(args.seed)
        by: dict[str, list[dict]] = {}
        for r in rows:
            by.setdefault(r["type"], []).append(r)
        per = max(1, args.max // len(by))
        rows = [x for v in by.values() for x in rng.sample(v, min(per, len(v)))]
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{args.split}.jsonl"
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            target = r["answer"]
            if r["type"] == "count" and args.split == "train":
                target = COUNT_REFUSAL
            img = to_png(r["img_id"])
            f.write(json.dumps({
                "messages": [{"role": "system", "content": SYSTEM},
                             {"role": "user", "content": [{"type": "image"}, {"type": "text", "text": r["question"]}]},
                             {"role": "assistant", "content": target}],
                "images": [str(img.relative_to(ROOT))], "meta": {"type": r["type"], "answer": r["answer"], "qid": r["qid"]},
            }) + "\n")
    from collections import Counter
    print(f"{len(rows)} questions -> {path.relative_to(ROOT)}", dict(Counter(r["type"] for r in rows)))


if __name__ == "__main__":
    main()
