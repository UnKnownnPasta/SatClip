"""Turn BigEarthNet v2 (reBEN, archive A017) labels into optical and radar Q&A for LoRA fine-tuning.

Each BigEarthNet patch is a co-registered Sentinel-2 (1.2 km, 10 m bands) and Sentinel-1 (VV, VH) pair
with multi-labels from CORINE (19-class nomenclature). From the labels alone we generate, per patch
and per sensor:
  - "Which land cover classes are present?"  -> sorted label list
  - "Is there <class> in this image?"        -> yes (a true label) or no (a sampled absent label)
  - "Is any open water visible?"             -> from the water classes (the question SatClip cares most about)
The radar prompt says how the false colour was built, so the model learns what a VV/VH composite looks
like instead of mistaking it for an optical photo (the SAR gap reported for general VLMs, archive A021, A033).

Data: https://zenodo.org/records/10891137 (metadata.parquet 3.6 MB; BigEarthNet-S2.tar.zst 63 GB and
BigEarthNet-S1.tar.zst 54 GB). On Colab, extract a subset of tiles only, for example with
  tar --zstd -xf BigEarthNet-S2.tar.zst --wildcards '*T33UUP*'
The builder indexes whatever patch folders exist under --s2-root / --s1-root and skips the rest.

    python training/lora/build_bigearthnet.py --s2-root /content/BigEarthNet-S2 --s1-root /content/BigEarthNet-S1 --max 20000
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from images import s1_false_colour, s2_rgb, save_png  # noqa: E402
from schema import ROOT  # noqa: E402

CACHE = ROOT / "training" / ".cache" / "bigearthnet"
OUT = ROOT / "training" / "data" / "bigearthnet"
META_URL = "https://zenodo.org/records/10891137/files/metadata.parquet?download=1"
WATER = {"Inland waters", "Marine waters", "Inland wetlands", "Coastal wetlands"}
CLASSES = ["Urban fabric", "Industrial or commercial units", "Arable land", "Permanent crops", "Pastures",
           "Complex cultivation patterns", "Land principally occupied by agriculture, with significant areas of natural vegetation",
           "Agro-forestry areas", "Broad-leaved forest", "Coniferous forest", "Mixed forest",
           "Natural grassland and sparsely vegetated areas", "Moors, heathland and sclerophyllous vegetation",
           "Transitional woodland, shrub", "Beaches, dunes, sands", "Inland wetlands", "Coastal wetlands", "Inland waters",
           "Marine waters"]
SYSTEM = "You look at one satellite image and answer briefly and only from what the image shows."
S2_NOTE = "This is a Sentinel-2 true-colour image, 10 m pixels, about 1.2 km across."
S1_NOTE = ("This is a Sentinel-1 radar image, 10 m pixels, about 1.2 km across, shown as false colour: red = VV, "
           "green = VH, blue = VV minus VH. Calm water is very dark.")


def index_patches(root: Path, suffix: str) -> dict[str, Path]:
    """patch name -> folder, for every folder holding a file ending in `suffix` (layout-agnostic)."""
    if not root or not root.exists():
        return {}
    return {p.parent.name: p.parent for p in root.rglob(f"*{suffix}")}


def read_band(folder: Path, name: str, band: str) -> np.ndarray:
    import rasterio
    with rasterio.open(folder / f"{name}_{band}.tif") as ds:
        return ds.read(1).astype("float32")


def qa_for(labels: list[str], rng: random.Random) -> list[tuple[str, str]]:
    labels = sorted(labels)
    absent = [c for c in CLASSES if c not in labels]
    pos = rng.choice(labels)
    neg = rng.choice(absent) if absent else None
    out = [("Which land cover classes are present? List them.", "; ".join(labels)),
           (f"Is there {pos.lower()} in this image?", "yes"),
           ("Is any open water or wetland visible?", "yes" if WATER & set(labels) else "no")]
    if neg:
        out.append((f"Is there {neg.lower()} in this image?", "no"))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--s2-root", type=Path)
    ap.add_argument("--s1-root", type=Path)
    ap.add_argument("--split", default="train", choices=["train", "validation", "test"])
    ap.add_argument("--max", type=int, default=20000, help="max patches")
    ap.add_argument("--seed", type=int, default=11)
    args = ap.parse_args()
    import pandas as pd
    meta_path = CACHE / "metadata.parquet"
    if not meta_path.exists():
        import httpx
        CACHE.mkdir(parents=True, exist_ok=True)
        meta_path.write_bytes(httpx.get(META_URL, follow_redirects=True, timeout=300).content)
    meta = pd.read_parquet(meta_path)
    meta = meta[(meta.split == args.split) & ~meta.contains_cloud_or_shadow & ~meta.contains_seasonal_snow]
    s2 = index_patches(args.s2_root, "_B04.tif") if args.s2_root else {}
    s1 = index_patches(args.s1_root, "_VV.tif") if args.s1_root else {}
    meta = meta[meta.patch_id.isin(s2) | meta.s1_name.isin(s1)]
    rng = random.Random(args.seed)
    if len(meta) > args.max:
        meta = meta.sample(args.max, random_state=args.seed)
    OUT.mkdir(parents=True, exist_ok=True)
    n = 0
    with open(OUT / f"{args.split}.jsonl", "w", encoding="utf-8") as f:
        for row in meta.itertuples():
            labels = list(row.labels)
            for sensor, name, folder in (("S2", row.patch_id, s2.get(row.patch_id)), ("S1", row.s1_name, s1.get(row.s1_name))):
                if folder is None:
                    continue
                png = OUT / "images" / f"{name}.png"
                if not png.exists():
                    if sensor == "S2":
                        rgb = s2_rgb(*(read_band(folder, name, b) / 10000 for b in ("B04", "B03", "B02")))
                    else:
                        rgb = s1_false_colour(read_band(folder, name, "VV"), read_band(folder, name, "VH"))
                    save_png(rgb, png)
                note = S2_NOTE if sensor == "S2" else S1_NOTE
                for q, a in qa_for(labels, rng):
                    f.write(json.dumps({
                        "messages": [{"role": "system", "content": SYSTEM},
                                     {"role": "user", "content": [{"type": "image"}, {"type": "text", "text": f"{note} {q}"}]},
                                     {"role": "assistant", "content": a}],
                        "images": [str(png.relative_to(ROOT))],
                        "meta": {"sensor": sensor, "patch": row.patch_id, "country": row.country}}) + "\n")
                    n += 1
    print(f"{n} Q&A pairs from {len(meta)} patches -> {(OUT / f'{args.split}.jsonl').relative_to(ROOT)}")


if __name__ == "__main__":
    main()
