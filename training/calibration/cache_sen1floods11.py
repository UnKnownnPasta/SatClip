"""Download the Sen1Floods11 hand-labelled chips once and keep a compact 20 m copy for fast experiments.

Each chip is stored as float16 VV and VH (gamma0 dB, same grid and shift as fit_water.py) plus the
20 m label, in one compressed .npz per split under training/.cache/sen1floods11/ (gitignored).
About 1.4 GB is streamed; the cache is about 60 MB.

    python training/calibration/cache_sen1floods11.py [--workers 8] [--shift-db 1.0]
"""
from __future__ import annotations

import argparse
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fit_water import ROOT, _get, _read, list_chips, to_working_grid  # noqa: E402

CACHE = ROOT / "training" / ".cache" / "sen1floods11"


def fetch(chip: dict[str, str], shift: float):
    try:
        s1 = _read(_get(chip["s1"]))
        lab = _read(_get(chip["label"]))[0]
        vv, lab20 = to_working_grid(s1[0], lab, shift)
        vh, _ = to_working_grid(s1[1], lab, shift)
        return chip, vv.astype("float16"), vh.astype("float16"), lab20
    except Exception as exc:  # noqa: BLE001
        print(f"  failed {chip['chip']}: {type(exc).__name__}: {exc}"[:200], flush=True)
        return chip, None, None, None


def load_cache(split: str) -> list[dict]:
    z = np.load(CACHE / f"{split}.npz", allow_pickle=True)
    return [{"chip": c, "event": e, "split": split, "vv": vv.astype("float32"), "vh": vh.astype("float32"), "label": lb}
            for c, e, vv, vh, lb in zip(z["chip"], z["event"], z["vv"], z["vh"], z["label"])]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--shift-db", type=float, default=1.0)
    a = ap.parse_args()
    CACHE.mkdir(parents=True, exist_ok=True)
    chips = list_chips()
    by: dict[str, list] = {}
    with ThreadPoolExecutor(a.workers) as pool:
        for i, (c, vv, vh, lb) in enumerate(pool.map(lambda c: fetch(c, a.shift_db), chips), 1):
            if vv is not None:
                by.setdefault(c["split"], []).append((c["chip"], c["event"], vv, vh, lb))
            if i % 50 == 0:
                print(f"  {i}/{len(chips)}", flush=True)
    for split, rows in by.items():
        np.savez_compressed(CACHE / f"{split}.npz", chip=np.array([r[0] for r in rows]), event=np.array([r[1] for r in rows]),
                            vv=np.stack([r[2] for r in rows]), vh=np.stack([r[3] for r in rows]), label=np.stack([r[4] for r in rows]))
        print(f"{split}: {len(rows)} chips")


if __name__ == "__main__":
    main()
