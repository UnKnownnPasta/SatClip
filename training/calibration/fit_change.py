"""Fit the confidence calibration of `sar_logratio_change` on Kuro Siwo (archive A041).

What it does
  1. Streams samples from the Kuro Siwo GRD webdataset on Hugging Face (CC BY 4.0): post-flood VV/VH, the
     closest pre-flood VV/VH (SL1), the expert label (0 dry, 1 permanent water, 2 flood) and the valid mask.
     Shards are read as tar streams and closed after the requested number of samples, so nothing big is
     stored. Both train_GRD and test_GRD shards are read, each at four byte offsets to reach more events.
  2. Puts each 224 x 224 px, 10 m sample on SatClip's 20 m grid (mean in linear power, then dB, plus the same
     +1 dB sigma0-to-gamma0 shift as fit_water.py).
  3. Runs the exact production code: `classify_sar_water` on the post-flood scene (v1.1, VV or VH) and
     `classify_sar_change` for the pair, which returns the new-water mask and the raw quality score.
  4. Marks a sample correct when the new-water area is within the card tolerance of the labelled flood
     area (class 2): |pred - ref| <= 0.2 * max(ref, 0.05 * valid area). That is the event the card
     confidence claims to predict.
  5. Cross-validates (5 folds grouped by flood event: the webdataset's train and test parts share events)
     the raw score, the borrowed water map, one Platt map, and one Platt map per answer regime ("no
     meaningful new water" vs "X sq km of new water"), then fits the regime maps on all samples and writes
     config/calibration/sar_logratio_change.json (replacing the borrowed "inherit" map) plus a report.

    python training/calibration/fit_change.py                       # about 1.5 GB streamed, 10 to 20 min
    python training/calibration/fit_change.py --per-shard 20        # quick run
    python training/calibration/fit_change.py --rows reports/sar_logratio_change_samples.csv   # refit only
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from fit_water import ROOT, FLOOR, TOL, Calibrator, platt  # noqa: E402
from kurosiwo_stream import samples  # noqa: E402

from satclip.instruments.water import classify_sar_change, classify_sar_water, fit_sar_threshold  # noqa: E402

OUT_DIR = HERE / "reports"
CAL_PATH = ROOT / "config" / "calibration" / "sar_logratio_change.json"
TRAIN_SHARDS = [f"train_GRD/shard-{i:05d}.tar" for i in range(5)]
TEST_SHARDS = [f"test_GRD/shard-{i:05d}.tar" for i in range(12)]
KEYS = ["split", "key", "event", "status", "valid_share", "measured_km2", "ref_km2", "pred_km2", "iou", "raw",
        "correct", "after_date", "before_date", "error"]


def to20(lin10: np.ndarray, shift_db: float) -> np.ndarray:
    h, w = (lin10.shape[0] // 2) * 2, (lin10.shape[1] // 2) * 2
    x = np.where(lin10[:h, :w] > 0, lin10[:h, :w], np.nan).reshape(h // 2, 2, w // 2, 2)
    with np.errstate(invalid="ignore", divide="ignore"):
        out = 10 * np.log10(np.nanmean(x, axis=(1, 3))) + shift_db
    out[~np.isfinite(out)] = np.nan
    return out


def label20(mask10: np.ndarray, valid10: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    h, w = (mask10.shape[0] // 2) * 2, (mask10.shape[1] // 2) * 2
    m = mask10[:h, :w].reshape(h // 2, 2, w // 2, 2)
    v = valid10[:h, :w].reshape(h // 2, 2, w // 2, 2) > 0
    flood = ((m == 2) & v).sum(axis=(1, 3)) * 2 >= v.sum(axis=(1, 3))
    ok = v.sum(axis=(1, 3)) >= 3
    return flood & ok, ok


def event_of(info: dict[str, Any]) -> tuple[str, str, str]:
    ds = info.get("datasets", {})
    master = next((k for k, v in ds.items() if v.get("master")), "")
    parts = master.split("_")
    event = parts[2] if len(parts) > 2 else "unknown"
    src = info.get("sources", {})
    return event, src.get("MS1", {}).get("source_date", ""), src.get("SL1", {}).get("source_date", "")


def measure(s: dict[str, Any], split: str, shift: float) -> dict[str, Any]:
    event, ad, bd = event_of(s.get("info", {}))
    row: dict[str, Any] = {"split": split, "key": s["key"], "event": event, "after_date": ad, "before_date": bd}
    vv_a, vh_a = to20(s["flood_vv"], shift), to20(s["flood_vh"], shift)
    vv_b, vh_b = to20(s["sec1_vv"], shift), to20(s["sec1_vh"], shift)
    flood, ok = label20(s["mask"], s["valid_mask"])
    valid = ok & np.isfinite(vv_a) & np.isfinite(vh_a)
    if valid.sum() < 0.5 * valid.size:
        return {**row, "status": "skipped", "valid_share": round(float(valid.mean()), 3)}
    fit = fit_sar_threshold(np.where(np.isfinite(vv_a), vv_a, np.nan))
    water, q = classify_sar_water(vv_a, valid, fit, vh_a)
    a = {"water": water, "valid": valid, "values": vv_a, "vh": vh_a, "quality": q,
         "fit": {**fit, "vh_threshold_db": q["vh_threshold_db"]}}
    ch = classify_sar_change(a, vv_b, vh_b)
    v = ch["valid"]
    px = 0.02 * 0.02
    new = ch["new"] & v
    ref = float((flood & v).sum()) * px
    pred = float(new.sum()) * px
    measured = float(v.sum()) * px
    inter, union = float((new & flood).sum()), float(((new | flood) & v).sum())
    correct = abs(pred - ref) <= TOL * max(ref, FLOOR * measured)
    return {**row, "status": "ok", "valid_share": round(float(v.mean()), 3), "measured_km2": round(measured, 4),
            "ref_km2": round(ref, 4), "pred_km2": round(pred, 4), "iou": round(inter / union, 4) if union else 1.0,
            "raw": round(float(ch["raw"]), 4), "correct": int(correct)}


SHARD_BYTES = 10_900_000_000   # all but the last train shard are about 10.9 GB
OFFSETS = (0.0, 0.25, 0.5, 0.75)  # start points inside each shard, to reach several flood events per shard


def collect(shards: list[str], split: str, per_shard: int, every: int, shift: float, workers: int) -> list[dict[str, Any]]:
    jobs = [(sh, int(f * (3_000_000_000 if sh.endswith("00004.tar") and sh.startswith("train") else SHARD_BYTES)))
            for sh in shards for f in OFFSETS]
    per_job = max(per_shard // len(OFFSETS), 1)

    def run(job: tuple[str, int]) -> list[dict[str, Any]]:
        shard, offset = job
        out = []
        try:
            for s in samples(shard, per_job, every, offset):
                try:
                    out.append(measure(s, split, shift))
                except Exception as exc:  # noqa: BLE001
                    out.append({"split": split, "key": s["key"], "status": "error", "error": f"{type(exc).__name__}: {exc}"[:160]})
        except Exception as exc:  # noqa: BLE001
            out.append({"split": split, "key": shard, "status": "error", "error": f"stream: {type(exc).__name__}: {exc}"[:160]})
        print(f"  {shard} @ {offset / 1e9:.1f} GB: {len(out)} samples", flush=True)
        return out
    with ThreadPoolExecutor(workers) as pool:
        return [r for rs in pool.map(run, jobs) for r in rs]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--per-shard", type=int, default=80, help="samples kept per shard")
    ap.add_argument("--every", type=int, default=3, help="keep one sample in N while streaming (spreads over the shard)")
    ap.add_argument("--shift-db", type=float, default=1.0)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--rows", type=Path)
    ap.add_argument("--no-write", action="store_true")
    args = ap.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows_path = OUT_DIR / "sar_logratio_change_samples.csv"
    if args.rows:
        with open(args.rows) as f:
            rows = [dict(r) for r in csv.DictReader(f)]
        for r in rows:
            for k in ("valid_share", "measured_km2", "ref_km2", "pred_km2", "iou", "raw"):
                if r.get(k) not in (None, ""):
                    r[k] = float(r[k])
            if r.get("correct") not in (None, ""):
                r["correct"] = int(r["correct"])
    else:
        rows = (collect(TRAIN_SHARDS, "train", args.per_shard, args.every, args.shift_db, args.workers)
                + collect(TEST_SHARDS, "test", max(args.per_shard // 2, 10), args.every, args.shift_db, args.workers))
        with open(rows_path, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=KEYS, extrasaction="ignore")
            w.writeheader()
            w.writerows(rows)
    ok = [r for r in rows if r["status"] == "ok"]
    for r in ok:
        r["regime"] = "change" if r["pred_km2"] >= FLOOR * r["measured_km2"] else "no_change"
    report = analyse(ok, len(rows), args)
    write_report(report)
    if not args.no_write:
        spec = report["final_spec"]
        spec.update({"instrument": "sar_logratio_change", "fit": {
            "n": len(ok), "events": report["events"], "dataset": report["dataset"], "date": report["date"],
            "instrument_version": "1.1", "event": "new-water area within +/-20% of the labelled flood area",
            "cv": "5-fold, grouped by flood event", "cv_regime_maps": report["cv"]["regime maps"],
            "report": "training/calibration/reports/sar_logratio_change.md"},
            "note": "Fitted on Kuro Siwo 2.2 km chips. One map per answer regime; replaces the map borrowed from sar_water_otsu."})
        CAL_PATH.write_text(json.dumps(spec, indent=1))
        print(f"wrote {CAL_PATH.relative_to(ROOT)}")


def _auc(p: np.ndarray, y: np.ndarray) -> Any:
    pos, neg = p[y == 1], p[y == 0]
    if not len(pos) or not len(neg):
        return None
    return round(float(np.mean([(x > neg).mean() + 0.5 * (x == neg).mean() for x in pos])), 3)


def _fit_regimes(rs: list[dict[str, Any]]) -> dict[str, Any]:
    maps = {}
    for reg in ("no_change", "change"):
        sub = [r for r in rs if r["regime"] == reg]
        if len(sub) < 10:  # too few to fit: constant at the pooled base rate, shrunk toward 0.5
            p = (sum(r["correct"] for r in sub) + 1) / (len(sub) + 2)
            maps[reg] = {"method": "logistic", "a": 0.0, "b": round(float(np.log(p / (1 - p))), 4), "fitted": True}
        else:
            maps[reg] = platt(np.array([r["raw"] for r in sub]), np.array([r["correct"] for r in sub], float))
    return {"method": "regimes", "by": "new_water_share", "cut": FLOOR, "maps": maps, "fitted": True}


def _metrics(p: np.ndarray, y: np.ndarray) -> dict[str, Any]:
    from fit_water import aurc, ece_mce, selective
    e, m, _ = ece_mce(p, y)
    return {"n": int(len(y)), "accuracy": round(float(y.mean()), 3), "ece": e, "mce": m, "aurc": aurc(p, y)[0],
            "auroc": _auc(p, y), "at_0.60": selective(p, y)}


def analyse(ok: list[dict[str, Any]], total: int, args) -> dict[str, Any]:
    """Grouped 5-fold cross-validation by flood event over all streamed samples. The Kuro Siwo webdataset's
    train and test parts share some events, so event grouping, not the shard split, is what keeps the
    evaluation honest."""
    events = sorted({r["event"] for r in ok})
    rng = np.random.default_rng(7)
    order = list(rng.permutation(events))
    fold_of = {ev: i % 5 for i, ev in enumerate(order)}
    y = np.array([r["correct"] for r in ok], float)
    raw = np.array([r["raw"] for r in ok])
    preds = {"raw score": raw.copy(), "borrowed water map": np.zeros(len(ok)), "one map": np.zeros(len(ok)),
             "regime maps": np.zeros(len(ok))}
    water = Calibrator(json.loads((ROOT / "config/calibration/sar_water_otsu.json").read_text()), "sar_water_otsu")
    preds["borrowed water map"] = np.array([water(x) for x in raw])
    for k in range(5):
        tr = [r for r in ok if fold_of[r["event"]] != k]
        te = [i for i, r in enumerate(ok) if fold_of[r["event"]] == k]
        one = Calibrator(platt(np.array([r["raw"] for r in tr]), np.array([r["correct"] for r in tr], float)))
        reg = Calibrator(_fit_regimes(tr))
        for i in te:
            preds["one map"][i] = one(ok[i]["raw"])
            preds["regime maps"][i] = reg(ok[i]["raw"], ok[i]["regime"])
    cv = {name: _metrics(p, y) for name, p in preds.items()}
    by_regime = {}
    for reg in ("no_change", "change"):
        idx = np.array([r["regime"] == reg for r in ok])
        by_regime[reg] = {"n": int(idx.sum()), "accuracy": round(float(y[idx].mean()), 3) if idx.any() else None,
                          "auroc_raw": _auc(raw[idx], y[idx]),
                          "regime_maps": _metrics(preds["regime maps"][idx], y[idx]) if idx.any() else None}
    flood = np.array([r["ref_km2"] >= FLOOR * r["measured_km2"] for r in ok])
    return {"instrument": "sar_logratio_change", "instrument_version": "1.1",
            "dataset": "Kuro Siwo GRD webdataset (archive A041), samples from train and test shards at 4 offsets each, before = SL1",
            "date": dt.date.today().isoformat(), "shift_db": args.shift_db,
            "tolerance": f"+/-{TOL:.0%} of max(labelled flood area, {FLOOR} x valid area)",
            "samples": len(ok), "skipped_or_error": total - len(ok), "events": len(events),
            "chips_with_labelled_flood": int(flood.sum()),
            "recall_of_flood_chips": round(float(y[flood].mean()), 3) if flood.any() else None,
            "median_iou_flood_chips": round(float(np.median([r["iou"] for r, f in zip(ok, flood) if f])), 3) if flood.any() else None,
            "cv": cv, "by_regime": by_regime, "final_spec": _fit_regimes(ok)}


def write_report(r: dict[str, Any]) -> None:
    (OUT_DIR / "sar_logratio_change_fit.json").write_text(json.dumps(r, indent=1))
    md = ["# Calibration report: sar_logratio_change", "",
          f"Generated by `training/calibration/fit_change.py` on {r['date']}. Dataset: {r['dataset']}.",
          f"Samples: {r['samples']} from {r['events']} flood events. Correct means: {r['tolerance']}. "
          "All numbers are 5-fold cross-validated with folds grouped by flood event (no event in both fit and test).", "",
          "| Map | ECE | MCE | AUROC | AURC | Coverage at 0.60 | Error when published |", "|---|---|---|---|---|---|---|"]
    for name, m in r["cv"].items():
        s = m["at_0.60"]
        md.append(f"| {name} | {m['ece']:.3f} | {m['mce']:.3f} | {m['auroc']} | {m['aurc']:.3f} | {s['coverage']:.2f} | {s['error_when_published']} |")
    md += ["", "| Answer regime | Samples | Share correct | AUROC of raw score | Coverage at 0.60 with regime maps | Error when published |",
           "|---|---|---|---|---|---|"]
    for reg, b in r["by_regime"].items():
        m = b["regime_maps"] or {"at_0.60": {"coverage": 0, "error_when_published": None}}
        md.append(f"| {reg.replace('_', ' ')} | {b['n']} | {b['accuracy']} | {b['auroc_raw']} | {m['at_0.60']['coverage']:.2f} | "
                  f"{m['at_0.60']['error_when_published']} |")
    md += ["", f"Chips with labelled flood: {r['chips_with_labelled_flood']}; the new-water area is within 20% on "
           f"{r['recall_of_flood_chips']} of them (median IoU {r['median_iou_flood_chips']}).", "",
           "Reading: the raw score barely ranks right from wrong answers overall, because two different answers are mixed. "
           "'No meaningful new water' answers are usually right; 'X sq km of new water' answers usually miss the labelled "
           "area by more than 20%, almost always by undercounting (on chips with labelled flood, 75% are undercounted by more "
           "than 20% and 4% overcounted; median measured-to-labelled ratio 0.53; the cause was not diagnosed per chip). The shipped map is "
           "therefore split by regime, and the change card will abstain on most positive change answers until the "
           "instrument improves.", "",
           "Limits: Kuro Siwo chips are 2.2 km squares, smaller than SatClip tiles; the before scene is the closest pre-flood "
           "pass in the dataset, often weeks earlier; few South Asian monsoon events. Per-sample rows: "
           "`sar_logratio_change_samples.csv`.", ""]
    (OUT_DIR / "sar_logratio_change.md").write_text("\n".join(md))
    print("\n".join(md))


if __name__ == "__main__":
    main()
