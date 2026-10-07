"""Fit the confidence calibration of `sar_water_otsu` on Sen1Floods11 hand-labelled chips.

What it does
  1. Downloads the 446 hand-labelled Sentinel-1 chips of Sen1Floods11 (archive A022) from the public
     Google Cloud bucket, one chip at a time, and keeps only a small per-chip result row.
  2. Puts each chip on SatClip's working grid: 10 m sigma0 dB -> 2 x 2 mean in linear power (20 m)
     -> dB, plus a sigma0-to-gamma0 shift (default +1.0 dB, ARCHITECTURE 6.7 "Radiometry").
  3. Runs the exact production code (`satclip.instruments.water.classify_sar_water`) to get the water
     mask and the raw quality score that the card confidence is built from.
  4. Marks a chip "correct" when the measured water area is within the card tolerance of the
     hand-labelled area: |pred - ref| <= 0.2 * max(ref, 0.05 * valid area). This is the event the
     confidence claims to predict (P(area within +/-20%)), so the fit is honest by construction.
  5. Chooses between an isotonic map (Zadrozny and Elkan, archive A127) and a Platt sigmoid (A126) by ECE
     on the valid split (fitted on train only), refits the winner on train + valid, and reports ECE and MCE (A128), risk-coverage at the 0.60 publication
     threshold (A027, A112) and a held-out-region check (A132): test split, Bolivia, and a leave-India-out
     fit evaluated on the 68 Indian chips.
  6. Writes config/calibration/sar_water_otsu.json (fitted: true, with the fit ledger) and a report with
     reliability and risk-coverage plots in training/calibration/reports/.

Instrument v1.1 (run 7) uses VV and VH; `--pols vv` reproduces v1.0 for comparison (v1.0 report kept as
reports/sar_water_otsu_v1.0.md).

Usage (from the repo root; needs the backend installed with the geo extra, plus matplotlib):
    python training/calibration/fit_water.py --from-cache    # after cache_sen1floods11.py, no streaming
    python training/calibration/fit_water.py                 # full run, about 1.4 GB streamed, not stored
    python training/calibration/fit_water.py --limit 40      # quick smoke run
    python training/calibration/fit_water.py --rows rows.csv # refit from a saved per-chip table, no download
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import io
import json
import math
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "backend"))

from satclip.calibration import fit_isotonic, Calibrator  # noqa: E402
from satclip.instruments.water import classify_sar_water  # noqa: E402

BUCKET = "https://storage.googleapis.com/sen1floods11/v1.1"
SPLITS = {"train": "flood_train_data.csv", "valid": "flood_valid_data.csv",
          "test": "flood_test_data.csv", "bolivia": "flood_bolivia_data.csv"}
OUT_DIR = ROOT / "training" / "calibration" / "reports"
CAL_PATH = ROOT / "config" / "calibration" / "sar_water_otsu.json"
TOL, FLOOR = 0.2, 0.05
THRESHOLD = 0.60


def _get(url: str, timeout: float = 120) -> bytes:
    import httpx
    for attempt in range(3):
        try:
            r = httpx.get(url, timeout=timeout, follow_redirects=True)
            r.raise_for_status()
            return r.content
        except Exception:  # noqa: BLE001
            if attempt == 2:
                raise
    raise RuntimeError("unreachable")


def list_chips() -> list[dict[str, str]]:
    chips = []
    for split, name in SPLITS.items():
        text = _get(f"{BUCKET}/splits/flood_handlabeled/{name}").decode()
        for line in text.strip().splitlines():
            s1, lab = [x.strip() for x in line.split(",")[:2]]
            chips.append({"split": split, "chip": s1.replace("_S1Hand.tif", ""), "event": s1.split("_")[0],
                          "s1": f"{BUCKET}/data/flood_events/HandLabeled/S1Hand/{s1}",
                          "label": f"{BUCKET}/data/flood_events/HandLabeled/LabelHand/{lab}"})
    return chips


def _read(blob: bytes) -> np.ndarray:
    from rasterio.io import MemoryFile
    with MemoryFile(blob) as mf, mf.open() as ds:
        return ds.read().astype("float32")


def to_working_grid(vv_db10: np.ndarray, label10: np.ndarray, shift_db: float) -> tuple[np.ndarray, np.ndarray]:
    """10 m sigma0 dB -> 20 m gamma0 dB (mean in linear power); label -> 20 m (water if >= half of the
    labelled sub-pixels are water; -1 where no sub-pixel is labelled)."""
    h, w = (vv_db10.shape[0] // 2) * 2, (vv_db10.shape[1] // 2) * 2
    lin = np.where(np.isfinite(vv_db10[:h, :w]), 10 ** (vv_db10[:h, :w] / 10), np.nan)
    blocks = lin.reshape(h // 2, 2, w // 2, 2)
    with np.errstate(invalid="ignore", divide="ignore"):
        mean = np.nanmean(blocks, axis=(1, 3))
        vv20 = 10 * np.log10(mean) + shift_db
    vv20[~np.isfinite(vv20)] = np.nan
    lab = label10[:h, :w].reshape(h // 2, 2, w // 2, 2)
    labelled = (lab >= 0).sum(axis=(1, 3))
    water = (lab == 1).sum(axis=(1, 3))
    lab20 = np.where(labelled == 0, -1, (water * 2 >= labelled).astype("int8"))
    return vv20, lab20


def measure_chip(chip: dict[str, str], shift_db: float, pols: str = "vvvh") -> dict[str, Any]:
    s1 = _read(_get(chip["s1"]))           # bands: VV, VH (sigma0 dB)
    lab = _read(_get(chip["label"]))[0]    # 1 water, 0 not water, -1 no data
    vv, lab20 = to_working_grid(s1[0], lab, shift_db)
    vh = to_working_grid(s1[1], lab, shift_db)[0] if pols == "vvvh" else None
    return measure_arrays({k: chip[k] for k in ("split", "chip", "event")}, vv, vh, lab20)


def measure_arrays(row: dict[str, Any], vv: np.ndarray, vh: Any, lab20: np.ndarray) -> dict[str, Any]:
    valid = np.isfinite(vv) & (lab20 >= 0)
    if vh is not None:
        valid &= np.isfinite(vh)
    if valid.sum() < 0.5 * valid.size:
        return {**row, "status": "skipped", "valid_share": round(float(valid.mean()), 3)}
    water, q = classify_sar_water(vv, valid, None, vh)
    px = 0.02 * 0.02  # km2 per 20 m pixel
    ref = float((lab20 == 1)[valid].sum()) * px
    pred = float(water[valid].sum()) * px
    measured = float(valid.sum()) * px
    inter = float((water & (lab20 == 1) & valid).sum())
    union = float(((water | (lab20 == 1)) & valid).sum())
    correct = abs(pred - ref) <= TOL * max(ref, FLOOR * measured)
    return {**row, "status": "ok", "valid_share": round(float(valid.mean()), 3), "measured_km2": round(measured, 4),
            "ref_km2": round(ref, 4), "pred_km2": round(pred, 4), "iou": round(inter / union, 4) if union else 1.0,
            "raw": q["raw_quality"], "p_area": q["p_area_within_tol"], "evidence_factor": q["evidence_factor"],
            "sigma_rel": q["sigma_rel"], "class_share": q["class_share"], "correct": int(correct),
            "inter_px": int(inter), "union_px": int(union)}


# ---------- metrics ----------

def ece_mce(p: np.ndarray, y: np.ndarray, bins: int = 10) -> tuple[float, float, list[dict[str, float]]]:
    edges = np.linspace(0, 1, bins + 1)
    ece, mce, table = 0.0, 0.0, []
    for i in range(bins):
        sel = (p >= edges[i]) & ((p < edges[i + 1]) if i < bins - 1 else (p <= 1))
        if not sel.any():
            continue
        conf, acc = float(p[sel].mean()), float(y[sel].mean())
        gap = abs(conf - acc)
        ece += sel.mean() * gap
        mce = max(mce, gap)
        table.append({"bin": f"{edges[i]:.1f}-{edges[i + 1]:.1f}", "n": int(sel.sum()), "conf": round(conf, 3),
                      "acc": round(acc, 3)})
    return round(float(ece), 4), round(float(mce), 4), table


def selective(p: np.ndarray, y: np.ndarray, t: float = THRESHOLD) -> dict[str, float]:
    keep = p >= t
    return {"coverage": round(float(keep.mean()), 3),
            "error_when_published": round(float(1 - y[keep].mean()), 3) if keep.any() else None,
            "error_if_always_published": round(float(1 - y.mean()), 3),
            "abstained_correct_share": round(float(y[~keep].mean()), 3) if (~keep).any() else None}


def aurc(p: np.ndarray, y: np.ndarray) -> tuple[float, list[tuple[float, float]]]:
    order = np.argsort(-p)
    err = 1 - y[order]
    n = len(err)
    risks = np.cumsum(err) / np.arange(1, n + 1)
    curve = [(float((k + 1) / n), float(risks[k])) for k in range(n)]
    return round(float(risks.mean()), 4), curve


def platt(raw: np.ndarray, y: np.ndarray, iters: int = 50) -> dict[str, Any]:
    """Platt sigmoid p = 1 / (1 + exp(-(a raw + b))) by Newton's method, with Platt's smoothed targets (A126)."""
    n1, n0 = float(y.sum()), float(len(y) - y.sum())
    t = np.where(y > 0, (n1 + 1) / (n1 + 2), 1 / (n0 + 2))
    X = np.stack([raw, np.ones_like(raw)], 1)
    w = np.zeros(2)
    for _ in range(iters):
        p = 1 / (1 + np.exp(-np.clip(X @ w, -30, 30)))
        g = X.T @ (p - t)
        H = X.T @ (X * (p * (1 - p))[:, None]) + 1e-6 * np.eye(2)
        step = np.linalg.solve(H, g)
        w -= step
        if np.abs(step).max() < 1e-8:
            break
    a, b = float(w[0]), float(w[1])
    return {"method": "logistic", "a": round(a, 4), "b": round(b, 4), "fitted": True}


def evaluate(cal: Calibrator, rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {"n": 0}
    raw = np.array([r["raw"] for r in rows], float)
    y = np.array([r["correct"] for r in rows], float)
    p = np.array([cal(x) for x in raw])
    e, m, table = ece_mce(p, y)
    e0, m0, _ = ece_mce(raw, y)
    a, _ = aurc(p, y)
    return {"n": len(rows), "accuracy": round(float(y.mean()), 3), "ece_uncalibrated": e0, "mce_uncalibrated": m0,
            "ece": e, "mce": m, "aurc": a, "at_0.60": selective(p, y), "uncalibrated_at_0.60": selective(raw, y),
            "reliability": table, "median_iou": round(float(np.median([r["iou"] for r in rows])), 3),
            "pooled_iou": _pooled_iou(rows)}


def _pooled_iou(rows: list[dict[str, Any]]) -> Any:
    if not all(r.get("union_px") not in (None, "") for r in rows):
        return None
    u = sum(float(r["union_px"]) for r in rows)
    return round(sum(float(r["inter_px"]) for r in rows) / u, 3) if u else None


def event_cards(cal: Calibrator, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Card-level check: treat all chips of one event in a split as one 'district' and rebuild the card
    confidence exactly as aggregate._area_confidence does (fully correlated tile sds)."""
    out = []
    by: dict[str, list[dict[str, Any]]] = {}
    for r in rows:
        by.setdefault(r["event"], []).append(r)
    for ev, rs in sorted(by.items()):
        pred = sum(r["pred_km2"] for r in rs)
        ref = sum(r["ref_km2"] for r in rs)
        meas = sum(r["measured_km2"] for r in rs)
        sd = sum(r["sigma_rel"] * max(r["class_share"], FLOOR) * r["measured_km2"] for r in rs)
        floor = FLOOR * meas
        rel = sd / max(pred, floor, 1e-9)
        p = 1.0 if rel == 0 else math.erf(TOL / (rel * math.sqrt(2)))
        w = [max(r["pred_km2"], 1e-6) for r in rs]
        factor = sum(wi * r["evidence_factor"] for wi, r in zip(w, rs)) / sum(w)
        conf = cal(p * factor)
        ok = abs(pred - ref) <= TOL * max(ref, floor)
        out.append({"event": ev, "chips": len(rs), "ref_km2": round(ref, 2), "pred_km2": round(pred, 2),
                    "confidence": round(conf, 3), "published": conf >= THRESHOLD, "within_20pct": bool(ok)})
    return out


# ---------- plots ----------

def plots(cal: Calibrator, india_cal: Calibrator, groups: dict[str, list[dict[str, Any]]], out_dir: Path) -> list[str]:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    files = []
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.4))
    ax = axes[0]
    ax.plot([0, 1], [0, 1], color="#94a3b8", lw=1, ls="--", label="perfect")
    colors = {"held-out test": "#2563eb", "Bolivia (unseen country)": "#ea580c", "India (leave-one-out)": "#059669"}
    for name, rows in groups.items():
        if not rows:
            continue
        raw = np.array([r["raw"] for r in rows])
        y = np.array([r["correct"] for r in rows], float)
        c = india_cal if name.startswith("India") else cal
        p = np.array([c(x) for x in raw])
        _, _, t = ece_mce(p, y)
        ax.plot([b["conf"] for b in t], [b["acc"] for b in t], marker="o", color=colors.get(name, "#334155"), label=name)
    ax.axvline(THRESHOLD, color="#e11d48", lw=1, ls=":")
    ax.set_xlabel("stated confidence (calibrated)")
    ax.set_ylabel("share of chips within +/-20% of the hand label")
    ax.set_title("Reliability")
    ax.legend(fontsize=8, loc="upper left")
    ax = axes[1]
    for name, rows in groups.items():
        if not rows:
            continue
        c = india_cal if name.startswith("India") else cal
        p = np.array([c(r["raw"]) for r in rows])
        y = np.array([r["correct"] for r in rows], float)
        _, curve = aurc(p, y)
        ax.plot([x for x, _ in curve], [r for _, r in curve], color=colors.get(name, "#334155"), label=name)
        keep = (p >= THRESHOLD).mean()
        ax.axvline(keep, color=colors.get(name, "#334155"), lw=0.8, ls=":")
    ax.set_xlabel("coverage (share of chips answered)")
    ax.set_ylabel("error among answered chips")
    ax.set_title("Risk-coverage (dotted: coverage at 0.60)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    f = out_dir / "sar_water_otsu_reliability.png"
    fig.savefig(f, dpi=130)
    files.append(f.name)
    return files


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--limit", type=int, default=0, help="use only the first N chips per split (smoke run)")
    ap.add_argument("--shift-db", type=float, default=1.0, help="sigma0 to gamma0 shift added to Sen1Floods11 VV")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--rows", type=Path, help="refit from a saved per-chip CSV instead of downloading")
    ap.add_argument("--from-cache", action="store_true",
                    help="measure from training/.cache/sen1floods11 (built by cache_sen1floods11.py) instead of streaming")
    ap.add_argument("--pols", choices=("vv", "vvvh"), default="vvvh",
                    help="vvvh = production v1.1 (VV or VH rule); vv = v1.0 behaviour, for comparison")
    ap.add_argument("--no-write", action="store_true", help="do not overwrite config/calibration")
    args = ap.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows_path = OUT_DIR / "sar_water_otsu_chips.csv"

    if args.rows:
        with open(args.rows) as f:
            rows = [{k: (float(v) if k not in ("split", "chip", "event", "status") and v not in ("",) else v)
                     for k, v in r.items()} for r in csv.DictReader(f)]
        for r in rows:
            if r["status"] == "ok":
                r["correct"] = int(r["correct"])
    elif args.from_cache:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from cache_sen1floods11 import load_cache
        rows = []
        for split in SPLITS:
            for c in load_cache(split):
                rows.append(measure_arrays({k: c[k] for k in ("split", "chip", "event")}, c["vv"],
                                           c["vh"] if args.pols == "vvvh" else None, c["label"]))
        _write_rows(rows, rows_path)
    else:
        chips = list_chips()
        if args.limit:
            seen: dict[str, int] = {}
            keep = []
            for c in chips:
                seen[c["split"]] = seen.get(c["split"], 0) + 1
                if seen[c["split"]] <= args.limit:
                    keep.append(c)
            chips = keep
        print(f"measuring {len(chips)} chips with {args.workers} workers ...", flush=True)
        rows = []
        with ThreadPoolExecutor(args.workers) as pool:
            for i, r in enumerate(pool.map(lambda c: _safe(measure_chip, c, args.shift_db, args.pols), chips), 1):
                rows.append(r)
                if i % 25 == 0:
                    print(f"  {i}/{len(chips)}", flush=True)
        _write_rows(rows, rows_path)

    ok = [r for r in rows if r["status"] == "ok"]
    fit_rows = [r for r in ok if r["split"] in ("train", "valid")]
    test = [r for r in ok if r["split"] == "test"]
    bolivia = [r for r in ok if r["split"] == "bolivia"]
    india = [r for r in ok if r["event"] == "India"]
    no_india_fit = [r for r in fit_rows if r["event"] != "India"]
    if len(fit_rows) < 10:
        raise SystemExit(f"only {len(fit_rows)} usable fitting chips; check downloads")

    # Method choice on the valid split (fit on train only), then refit the chosen method on train + valid.
    train = [r for r in fit_rows if r["split"] == "train"]
    valid_rows = [r for r in fit_rows if r["split"] == "valid"]
    fitters = {"isotonic": lambda rs: fit_isotonic([r["raw"] for r in rs], [r["correct"] for r in rs]),
               "logistic": lambda rs: platt(np.array([r["raw"] for r in rs]), np.array([r["correct"] for r in rs], float))}
    choice = {m: evaluate(Calibrator(f(train)), valid_rows)["ece"] for m, f in fitters.items()}
    method = min(choice, key=choice.get)
    spec = fitters[method](fit_rows)
    cal = Calibrator(spec, "sar_water_otsu")
    other = "logistic" if method == "isotonic" else "isotonic"
    other_cal = Calibrator(fitters[other](fit_rows))
    india_cal = Calibrator(fitters[method](no_india_fit))

    report = {
        "instrument": "sar_water_otsu", "dataset": "Sen1Floods11 v1.1 hand-labelled chips (archive A022)",
        "date": dt.date.today().isoformat(), "shift_db": args.shift_db,
        "instrument_version": "1.1" if args.pols == "vvvh" else "1.0", "polarisations": "VV or VH" if args.pols == "vvvh" else "VV", "tolerance": f"+/-{TOL:.0%} of max(ref, {FLOOR} x valid area)",
        "chips_total": len(rows), "chips_used": len(ok), "skipped": len(rows) - len(ok),
        "fit_on": f"train + valid splits ({len(fit_rows)} chips)",
        "held_out_test": evaluate(cal, test), "bolivia": evaluate(cal, bolivia),
        "india_leave_out": evaluate(india_cal, india),
        "method": method, "method_choice_valid_ece": choice,
        "other_method_on_test": {"method": other, **{k: v for k, v in evaluate(other_cal, test).items() if k in ("ece", "mce", "aurc", "at_0.60")}},
        "fit_in_sample": {k: v for k, v in evaluate(cal, fit_rows).items() if k in ("n", "accuracy", "ece", "mce")},
        "events_test": event_cards(cal, test + bolivia),
    }
    figs = plots(cal, india_cal, {"held-out test": test, "Bolivia (unseen country)": bolivia,
                                  "India (leave-one-out)": india}, OUT_DIR)
    (OUT_DIR / "sar_water_otsu_fit.json").write_text(json.dumps(report, indent=1))
    write_markdown(report, figs)

    if not args.no_write and not args.limit and args.pols == "vvvh":
        spec.update({"instrument": "sar_water_otsu", "fit": {"method_choice_valid_ece": choice,
            "n": len(fit_rows), "dataset": report["dataset"], "date": report["date"], "shift_db": args.shift_db, "instrument_version": "1.1",
            "event": "measured water area within +/-20% of the hand-labelled area",
            "test_ece": report["held_out_test"]["ece"], "test_coverage_at_0.60": report["held_out_test"]["at_0.60"]["coverage"],
            "test_error_when_published": report["held_out_test"]["at_0.60"]["error_when_published"],
            "report": "training/calibration/reports/sar_water_otsu.md"},
            "note": "Fitted on 5 km chips from 11 flood events worldwide, 68 of them in India. Applied at district scale "
                    "through the same formula; see the report for the event-level check and its limits."})
        CAL_PATH.write_text(json.dumps(spec, indent=1))
        print(f"wrote {CAL_PATH.relative_to(ROOT)}")
    print(json.dumps({k: report[k] for k in ("chips_used", "held_out_test")}, indent=1)[:1500])


def _write_rows(rows: list[dict[str, Any]], path: Path) -> None:
    keys = ["split", "chip", "event", "status", "valid_share", "measured_km2", "ref_km2", "pred_km2", "iou", "raw",
            "p_area", "evidence_factor", "sigma_rel", "class_share", "correct", "inter_px", "union_px", "error"]
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def _safe(fn, chip, shift, pols):
    try:
        return fn(chip, shift, pols)
    except Exception as exc:  # noqa: BLE001
        return {**{k: chip[k] for k in ("split", "chip", "event")}, "status": "error", "error": f"{type(exc).__name__}: {exc}"[:200]}


def write_markdown(r: dict[str, Any], figs: list[str]) -> None:
    def block(name: str, e: dict[str, Any]) -> str:
        if not e.get("n"):
            return f"| {name} | 0 | | | | | | |\n"
        s, u = e["at_0.60"], e["uncalibrated_at_0.60"]
        return (f"| {name} | {e['n']} | {e['accuracy']:.2f} | {e['ece_uncalibrated']:.3f} -> {e['ece']:.3f} | "
                f"{e['mce']:.3f} | {u['coverage']:.2f} / {u['error_when_published']} | {s['coverage']:.2f} / "
                f"{s['error_when_published']} | {e['median_iou']:.2f} |\n")
    lines = [
        "# Calibration report: sar_water_otsu", "",
        f"Generated by `training/calibration/fit_water.py` on {r['date']}. Dataset: {r['dataset']}.",
        f"Instrument version {r.get('instrument_version', '1.0')} ({r.get('polarisations', 'VV')}).",
        f"Chips used: {r['chips_used']} of {r['chips_total']} (skipped when under half the chip is valid and labelled).",
        f"Correct means: {r['tolerance']}. Fitted on the {r['fit_on']}; sigma0 to gamma0 shift {r['shift_db']} dB.", "",
        "| Evaluation set | Chips | Share correct | ECE before -> after | MCE after | Coverage / error at 0.60, before | "
        "Coverage / error at 0.60, after | Median IoU |", "|---|---|---|---|---|---|---|---|",
    ]
    lines[-1] += "\n" + block("Held-out test split", r["held_out_test"]) + block("Bolivia (country never seen)", r["bolivia"]) \
        + block("India, fit without India", r["india_leave_out"])
    p = r["other_method_on_test"]
    lines += ["", f"Chosen map: **{r['method']}** (lower ECE on the valid split when fitted on train only: "
              f"{r['method_choice_valid_ece']}). The other map ({p['method']}) on the same test split, for comparison: ECE {p['ece']:.3f}, MCE {p['mce']:.3f}, "
              f"AURC {p['aurc']:.3f}, coverage {p['at_0.60']['coverage']:.2f} with error {p['at_0.60']['error_when_published']} at 0.60.", "",
              "## Card-level check (all chips of an event summed, as the aggregator does for a district)", "",
              "| Event | Chips | Hand-labelled km2 | Measured km2 | Card confidence | Published | Within 20% |", "|---|---|---|---|---|---|---|"]
    for e in r["events_test"]:
        lines.append(f"| {e['event']} | {e['chips']} | {e['ref_km2']} | {e['pred_km2']} | {e['confidence']:.2f} | "
                     f"{'yes' if e['published'] else 'no'} | {'yes' if e['within_20pct'] else 'no'} |")
    prev = OUT_DIR / "sar_water_otsu_v1.0_fit.json"
    if r.get("instrument_version") == "1.1" and prev.exists():
        p0 = json.loads(prev.read_text())
        lines += ["", "## v1.0 (VV only, run 6) against v1.1 (VV or VH, run 7)", "",
                  "| Evaluation set | Share correct v1.0 -> v1.1 | ECE after | Coverage at 0.60 | Error when published | Median IoU |",
                  "|---|---|---|---|---|---|"]
        for key, name in (("held_out_test", "Held-out test split"), ("bolivia", "Bolivia"), ("india_leave_out", "India, fit without India")):
            a, b = p0[key], r[key]
            lines.append(f"| {name} | {a['accuracy']:.2f} -> {b['accuracy']:.2f} | {a['ece']:.3f} -> {b['ece']:.3f} | "
                         f"{a['at_0.60']['coverage']:.2f} -> {b['at_0.60']['coverage']:.2f} | {a['at_0.60']['error_when_published']} -> "
                         f"{b['at_0.60']['error_when_published']} | {a['median_iou']:.2f} -> {b['median_iou']:.2f} |")
        lines += ["", "VH bounds were chosen on the train split only (`reports/sar_water_vh_tuning.md`)."]
    lines += ["", *[f"![reliability and risk-coverage]({f})" for f in figs], "",
              "Per-chip rows: `sar_water_otsu_chips.csv`. Full numbers: `sar_water_otsu_fit.json`.", ""]
    (OUT_DIR / "sar_water_otsu.md").write_text("\n".join(lines))


if __name__ == "__main__":
    main()
