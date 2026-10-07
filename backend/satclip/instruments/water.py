"""Water instruments.

sar_water_otsu (water_extent)
  Sentinel-1 RTC VV backscatter in dB. Open water is a specular reflector and appears dark.
  The threshold is fitted per tile, following the split-based approach of the DLR / Copernicus GFM
  chain (archive A083, A084, A086):
    1. split the tile into sub-blocks of about 1 km;
    2. keep blocks whose Otsu split is clearly bimodal (Ashman D >= 3 on class moments, class means
       at least 3 dB apart, minority class >= 10%, dark class mean below -15 dB);
    3. pool the kept blocks and fit a Kittler-Illingworth minimum-error threshold on the pool
       (Otsu is biased toward the more variable land class on real Sentinel-1 histograms).
  If no block in the tile is bimodal, the fit is repeated on the 3 x 3 tile neighbourhood at 40 m.
  If that also fails, or the fitted value is above -14 dB gamma0 (about -15 dB sigma0, implausible
  for water), a default of -17 dB gamma0 (about -18 dB sigma0) is used and the card says so.
  Blobs under 10 px are dropped.
  Outside the monsoon the data layer may choose Sentinel-2 instead: NDWI = (green - nir) / (green + nir)
  with water at NDWI > 0 (McFeeters), on SCL-clear pixels only.

sar_logratio_change (water_change)
  Two same-orbit Sentinel-1 scenes. New water = water after (threshold fitted on the after scene,
  applied to both dates) AND not water before AND a backscatter drop of at least 3 dB
  (log-ratio, archive A036). Optical pairs use NDWI crossing zero on pixels clear on both dates.
"""
from __future__ import annotations

from typing import Any, Optional

import numpy as np

from ..calibration import load as load_cal
from ..data.provider import get_provider
from ..models import TileJob, TileResult, TileStatus
from . import register
from .common import (abstain, kittler_illingworth, threshold_confidence, db, drop_small, norm_diff, otsu, pixel_km2, region_mask, save_overlay,
                     scene_ev, split_stats)

# Planetary Computer serves gamma0 (RTC), which reads about 0.6 to 1.5 dB above sigma0 at Sentinel-1
# incidence angles (gamma0 = sigma0 / cos(theta), theta 30 to 45 degrees). The sigma0 rules of archive
# A083 (fit above -15 dB is implausible; default -18 dB) are shifted by +1 dB accordingly.
DEFAULT_DB = -17.0
MAX_WATER_DB = -14.0
BLOCK_PX = 50              # about 1 km at 20 m
# Ashman D is computed from the moments of the two Otsu classes. Splitting a single Gaussian at its
# mean already gives D of about 2.65 that way, so we require D >= 3 plus a 3 dB gap between class
# means (stricter than the D > 2 used with fitted Gaussians in archive A086).
MIN_D = 3.0
MIN_GAP_DB = 3.0
MIN_BLOB_PX = 10
DROP_DB = -3.0
CLEAR_SCL = (4, 5, 6, 7, 11)
WATER_PALETTE = {1: (37, 99, 235, 170)}
CHANGE_PALETTE = {1: (37, 99, 235, 190), 2: (148, 163, 184, 110), 3: (234, 88, 12, 160)}


def fit_sar_threshold(vv_db: np.ndarray) -> dict[str, Any]:
    h, w = vv_db.shape
    kept = []
    n_blocks = 0
    step = BLOCK_PX // 2  # half-overlapping blocks, so an edge cannot hide on a block boundary
    for y in range(0, max(h - step, 1), step):
        for x in range(0, max(w - step, 1), step):
            blk = vv_db[y:y + BLOCK_PX, x:x + BLOCK_PX]
            if np.isfinite(blk).mean() < 0.8:
                continue
            n_blocks += 1
            t = otsu(blk)
            st = split_stats(blk, t)
            if (st["ashman_d"] >= MIN_D and st["minority"] >= 0.10 and st["mean_low"] < MAX_WATER_DB - 1
                    and st["mean_high"] - st["mean_low"] >= MIN_GAP_DB):
                kept.append(blk[np.isfinite(blk)])
    fit = {"blocks": n_blocks, "bimodal_blocks": len(kept)}
    if kept:
        pool = np.concatenate(kept)
        t = kittler_illingworth(pool)
        st = split_stats(pool, t)
        if t <= MAX_WATER_DB:
            return {**fit, "threshold_db": round(t, 2), "source": "fitted", **{k: round(v, 3) for k, v in st.items()}}
        fit["rejected_fit_db"] = round(t, 2)
    st = split_stats(vv_db, DEFAULT_DB)
    return {**fit, "threshold_db": DEFAULT_DB, "source": "default", **{k: round(v, 3) for k, v in st.items()}}


THRESH_SIGMA_DB = 1.0   # assumed threshold error (1 sd) for the confidence model


def water_quality(values: np.ndarray, t: float, fit: dict[str, Any], margin: float = THRESH_SIGMA_DB) -> dict[str, float]:
    """Raw confidence = P(area within +/-20% under a threshold error of `margin`) x evidence factor.
    The evidence factor is 0.8 to 1.0 for a fitted bimodal threshold (by Ashman D) and 0.75 for the
    default threshold, standing for the risk that the dark class is not water (calm tarmac, sand, shadow)."""
    tc = threshold_confidence(values, t, margin, below=True)
    if fit.get("source", "").startswith("fitted"):
        sep = min(max((fit["ashman_d"] - MIN_D) / 2, 0), 1)   # D 3 -> 0, D 5 -> 1
        factor = (0.8 + 0.2 * sep) * (0.95 if "neighbourhood" in fit["source"] else 1.0)
    else:
        factor = 0.75
    return {**tc, "evidence_factor": round(factor, 3), "raw_quality": round(tc["p_area_within_tol"] * factor, 4)}


def classify_sar_water(vv_db: np.ndarray, valid: np.ndarray, fit: Optional[dict[str, Any]] = None
                       ) -> tuple[np.ndarray, dict[str, float]]:
    """Core of sar_water_otsu on one tile of gamma0 VV in dB: threshold, speckle removal, raw quality.
    Shared with training/calibration/fit_water.py so the calibration is fitted on exactly this code."""
    if fit is None:
        fit = fit_sar_threshold(np.where(np.isfinite(vv_db), vv_db, np.nan))
    water = drop_small(valid & (vv_db < fit["threshold_db"]), MIN_BLOB_PX)
    q = water_quality(np.where(valid, vv_db, np.nan), fit["threshold_db"], fit)
    return water, q


def _sar_water(job: TileJob, prov, sel, res: float) -> tuple[Optional[dict], Optional[str]]:
    r = prov.read(sel.scene, "vv", job.bbox, res)
    vv = db(r.data)
    reg = region_mask(job, r)
    valid = np.isfinite(vv) & (reg if reg is not None else True)
    inside = reg.mean() if reg is not None else 1.0
    if inside == 0:
        return None, "tile lies outside the named district"
    if valid.sum() < 0.5 * inside * vv.size:
        return None, f"only {valid.mean():.0%} of the tile has valid radar pixels"
    fit = fit_sar_threshold(np.where(np.isfinite(vv), vv, np.nan))
    if fit["source"] == "default":
        # Not enough bimodal evidence inside the tile: refit on the 3 x 3 tile neighbourhood at 40 m,
        # like the AOI-wide tile selection of archive A083. Deterministic, so receipts reproduce.
        dx, dy = job.bbox[2] - job.bbox[0], job.bbox[3] - job.bbox[1]
        ctx = (job.bbox[0] - dx, job.bbox[1] - dy, job.bbox[2] + dx, job.bbox[3] + dy)
        try:
            ctx_db = db(prov.read(sel.scene, "vv", ctx, res * 2).data)
            cfit = fit_sar_threshold(ctx_db)
        except Exception as exc:  # noqa: BLE001  (context is a bonus; the tile result stands without it)
            cfit = {"source": "default", "context_error": type(exc).__name__}
        if cfit["source"] == "fitted":
            fit = {**cfit, "source": "fitted (3 x 3 tile neighbourhood)", "tile_fit": fit}
            fit["ashman_d"] = cfit["ashman_d"]
    water, q = classify_sar_water(vv, valid, fit)
    return {"raster": r, "water": water, "valid": valid, "fit": fit, "quality": q, "values": vv}, None


def _s2_water(job: TileJob, prov, sel, res: float) -> tuple[Optional[dict], Optional[str]]:
    clear, frac, scl = prov.tile_is_clear(sel.scene, job.bbox, res)
    if not clear:
        return None, f"cloud: {frac:.0%} of the tile is cloud or shadow on {sel.scene.date}"
    g = prov.read(sel.scene, "green", job.bbox, res)
    n = prov.read(sel.scene, "nir", job.bbox, res)
    ndwi = norm_diff(g.data, n.data)
    reg = region_mask(job, g)
    ok_px = np.isin(scl.data, CLEAR_SCL) if scl is not None and scl.data.shape == ndwi.shape else np.ones_like(ndwi, bool)
    valid = np.isfinite(ndwi) & ok_px & (reg if reg is not None else True)
    inside = reg.mean() if reg is not None else 1.0
    if inside == 0:
        return None, "tile lies outside the named district"
    if valid.sum() < 0.5 * inside * ndwi.size:
        return None, f"only {valid.mean():.0%} of the tile is clear and valid"
    water = drop_small(valid & (ndwi > 0.0), MIN_BLOB_PX)
    fit = {"threshold_ndwi": 0.0, "source": "fixed (McFeeters NDWI > 0)", "cloud_share": round(frac, 3)}
    tc = threshold_confidence(np.where(valid, -ndwi, np.nan), 0.0, 0.05, below=True)  # water is NDWI > 0
    q = {**tc, "evidence_factor": 0.85, "raw_quality": round(tc["p_area_within_tol"] * 0.85 * (1 - frac), 4)}
    return {"raster": g, "water": water, "valid": valid, "fit": fit, "quality": q, "values": ndwi}, None


def _measure(job, prov, sel, res):
    return (_sar_water if sel.sensor == "S1" else _s2_water)(job, prov, sel, res)


@register("sar_water_otsu", "1.0")
def sar_water_otsu(job: TileJob) -> TileResult:
    prov = get_provider()
    cfg = prov.cfg
    res = float(cfg.get("outputs", {}).get("read_res_m", 20))
    sel = prov.for_tile(job.intent, job.windows, job.bbox)[0]
    if not sel.ok:
        return abstain(job, sel.reason)
    m, why = _measure(job, prov, sel, res)
    if m is None:
        return abstain(job, why, scene=sel.scene.id)
    cal = load_cal("sar_water_otsu")
    conf = cal(m["quality"]["raw_quality"])
    area = float(m["water"].sum()) * pixel_km2(res)
    measured = float(m["valid"].sum()) * pixel_km2(res)
    q = m["quality"]
    sigma_abs = q["sigma_rel"] * max(q["class_share"], 0.05) * measured  # 1 sd of the area, km2
    mask = save_overlay(job, m["raster"], m["water"].astype("uint8"), WATER_PALETTE, {"1": "open water"}, cfg)
    method = ("Sentinel-1 VV backscatter, split-based Otsu threshold" if sel.sensor == "S1"
              else "Sentinel-2 NDWI > 0 on cloud-free pixels")
    return TileResult(job_id=job.job_id, tile_id=job.tile_id, status=TileStatus.ok, value=round(area, 4), unit="km2",
                      confidence=round(conf, 3), scenes=[scene_ev(sel.scene)], mask=mask,
                      params={"method": method, "sensor": sel.sensor, "selection": sel.reason,
                              "fallback_used": sel.fallback_used, "res_m": res, "fit": m["fit"], **m["quality"],
                              "measured_km2": round(measured, 4), "sigma_abs_km2": round(sigma_abs, 4),
                              "sigma_floor_km2": round(0.05 * measured, 4), "calibration": cal.status})


@register("sar_logratio_change", "1.0")
def sar_logratio_change(job: TileJob) -> TileResult:
    prov = get_provider()
    cfg = prov.cfg
    res = float(cfg.get("outputs", {}).get("read_res_m", 20))
    if len(job.windows) < 2:
        return abstain(job, "a change question needs two dates")
    before, after = prov.for_tile(job.intent, job.windows, job.bbox)
    if not after.ok:
        return abstain(job, after.reason)
    if not before.ok:
        return abstain(job, before.reason)
    if after.sensor == "S1":
        a, why = _sar_water(job, prov, after, res)
        if a is None:
            return abstain(job, "after date: " + why)
        rb = prov.read(before.scene, "vv", job.bbox, res)
        b_db = db(rb.data)
        if b_db.shape != a["values"].shape:
            return abstain(job, "before and after scenes are on different grids; cannot compare pixel by pixel")
        t = a["fit"]["threshold_db"]
        valid = a["valid"] & np.isfinite(b_db)
        water_b = valid & (b_db < t)
        ratio = a["values"] - b_db  # dB difference = 10 log10(after / before)
        new = drop_small(valid & a["water"] & ~water_b & (ratio <= DROP_DB), MIN_BLOB_PX)
        receded = drop_small(valid & water_b & ~a["water"] & (ratio >= -DROP_DB), MIN_BLOB_PX)
        cand = valid & a["water"] & ~water_b
        # how stable is the new-water area if the 3 dB drop rule were off by 1 dB?
        rc = (threshold_confidence(np.where(cand, ratio, np.nan), DROP_DB, 1.0, below=True) if cand.any()
              else {"p_area_within_tol": 1.0, "near_share": 0.0})
        amb = rc.get("near_share", 0.0)
        raw = a["quality"]["raw_quality"] * rc["p_area_within_tol"]
        px_ = pixel_km2(res)
        new_km2, after_km2 = float(new.sum()) * px_, float(a["water"].sum()) * px_
        cand_km2 = float(cand.sum()) * px_
        a_abs = a["quality"]["sigma_rel"] * max(a["quality"]["class_share"], 0.05) * float(a["valid"].sum()) * px_
        r_abs = rc.get("sigma_rel", 0.0) * max(rc.get("class_share", 0.0), 0.05) * cand_km2
        sigma = {"sigma_abs_km2": round(float(np.hypot(r_abs, a_abs * new_km2 / max(after_km2, 1e-6))), 4),
                 "sigma_floor_km2": round(0.05 * float(a["valid"].sum()) * px_, 4),
                 "evidence_factor": a["quality"]["evidence_factor"]}
        method = "Sentinel-1 same-orbit pair: water threshold fitted on the after scene, plus a 3 dB backscatter drop"
        fit = {**a["fit"], "drop_db": DROP_DB, "ratio_ambiguous_share": round(amb, 4)}
        raster = a["raster"]
    else:
        ok_b, fb, sclb = prov.tile_is_clear(before.scene, job.bbox, res)
        ok_a, fa, scla = prov.tile_is_clear(after.scene, job.bbox, res)
        if not (ok_a and ok_b):
            return abstain(job, f"cloud over the tile ({fb:.0%} before, {fa:.0%} after)")
        nd = []
        for s in (before.scene, after.scene):
            g, n = prov.read(s, "green", job.bbox, res), prov.read(s, "nir", job.bbox, res)
            nd.append(norm_diff(g.data, n.data))
        raster = g
        if nd[0].shape != nd[1].shape:
            return abstain(job, "before and after scenes are on different grids; cannot compare pixel by pixel")
        reg = region_mask(job, raster)
        valid = (np.isfinite(nd[0]) & np.isfinite(nd[1]) & np.isin(sclb.data, CLEAR_SCL) & np.isin(scla.data, CLEAR_SCL)
                 & (reg if reg is not None else True))
        if valid.sum() < 0.3 * valid.size:
            return abstain(job, "too few pixels are clear on both dates")
        water_b, water_a = valid & (nd[0] > 0), valid & (nd[1] > 0)
        new = drop_small(water_a & ~water_b, MIN_BLOB_PX)
        receded = drop_small(water_b & ~water_a, MIN_BLOB_PX)
        amb = float(((np.abs(nd[0]) < 0.05) | (np.abs(nd[1]) < 0.05))[valid].mean())
        raw = 0.85 * (1 - amb) * (1 - max(fa, fb))
        method = "Sentinel-2 pair: NDWI crossing zero on pixels clear on both dates"
        fit = {"threshold_ndwi": 0.0, "ambiguous_share": round(amb, 4)}
        a = {"water": water_a}
        sigma = {}
    cal = load_cal("sar_logratio_change")
    conf = cal(raw)
    px = pixel_km2(res)
    classes = np.zeros(new.shape, dtype="uint8")
    classes[water_b & a["water"]] = 2
    classes[new] = 1
    classes[receded] = 3
    mask = save_overlay(job, raster, classes, CHANGE_PALETTE,
                        {"1": "new water", "2": "water on both dates", "3": "water receded"}, cfg)
    return TileResult(job_id=job.job_id, tile_id=job.tile_id, status=TileStatus.ok, value=round(float(new.sum()) * px, 4),
                      unit="km2", confidence=round(conf, 3), mask=mask,
                      scenes=[scene_ev(before.scene, "before"), scene_ev(after.scene, "after")],
                      params={"method": method, "sensor": after.sensor, "selection": after.reason,
                              "pairing": before.reason, "fallback_used": after.fallback_used, "res_m": res, "fit": fit,
                              "water_before_km2": round(float(water_b.sum()) * px, 4),
                              "water_after_km2": round(float(a["water"].sum()) * px, 4),
                              "receded_km2": round(float(receded.sum()) * px, 4), "raw_quality": round(raw, 4), **sigma,
                              "measured_km2": round(float(valid.sum()) * px, 4), "calibration": cal.status})
