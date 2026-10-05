"""ndvi_difference (vegetation_change).

NDVI = (nir - red) / (nir + red) from Sentinel-2 L2A surface reflectance on two dates.
Only pixels that are clear (SCL vegetation, bare soil, water or unclassified) on both dates count.
Decline = NDVI fell by at least 0.15 on a pixel that was vegetated before (NDVI >= 0.3).
Gain is reported too. The instrument measures greenness change, not its cause: harvest,
flooding and crop damage can all lower NDVI, so the card says so.
Optical-only: under cloud the tile abstains rather than guessing from radar.
"""
from __future__ import annotations

import numpy as np

from ..calibration import load as load_cal
from ..data.provider import get_provider
from ..models import TileJob, TileResult, TileStatus
from . import register
from .common import abstain, threshold_confidence, drop_small, norm_diff, pixel_km2, region_mask, save_overlay, scene_ev

DROP = -0.15
VEGETATED = 0.3
CLEAR_SCL = (4, 5, 6, 7)
PALETTE = {1: (234, 88, 12, 175), 2: (22, 163, 74, 150)}


@register("ndvi_difference", "1.0")
def ndvi_difference(job: TileJob) -> TileResult:
    prov = get_provider()
    cfg = prov.cfg
    res = float(cfg.get("outputs", {}).get("read_res_m", 20))
    if len(job.windows) < 2:
        return abstain(job, "a change question needs two dates")
    before, after = prov.for_tile(job.intent, job.windows, job.bbox)
    for name, sel in (("after", after), ("before", before)):
        if not sel.ok:
            return abstain(job, sel.reason if sel.reason.startswith(name) else f"{name} date: {sel.reason}")
    ndvi, scls, clouds = [], [], []
    for s in (before.scene, after.scene):
        clear, frac, scl = prov.tile_is_clear(s, job.bbox, res)
        if not clear:
            return abstain(job, f"cloud: {frac:.0%} of the tile is cloud or shadow on {s.date}")
        red, nir = prov.read(s, "red", job.bbox, res), prov.read(s, "nir", job.bbox, res)
        ndvi.append(norm_diff(nir.data, red.data))
        scls.append(scl.data)
        clouds.append(frac)
    if ndvi[0].shape != ndvi[1].shape:
        return abstain(job, "before and after scenes are on different grids; cannot compare pixel by pixel")
    reg = region_mask(job, nir)
    valid = (np.isfinite(ndvi[0]) & np.isfinite(ndvi[1]) & np.isin(scls[0], CLEAR_SCL) & np.isin(scls[1], CLEAR_SCL)
             & (reg if reg is not None else True))
    inside = reg.mean() if reg is not None else 1.0
    if inside == 0:
        return abstain(job, "tile lies outside the named district")
    if valid.sum() < 0.5 * inside * valid.size:
        return abstain(job, f"only {valid.mean():.0%} of the tile is clear on both dates")
    d = ndvi[1] - ndvi[0]
    veg_before = valid & (ndvi[0] >= VEGETATED)
    decline = drop_small(veg_before & (d <= DROP), 10)
    gain = drop_small(valid & (d >= -DROP), 10)
    # P(decline area within +/-20%) if the 0.15 drop threshold is off by 0.05 NDVI, times 0.9 for
    # residual haze the scene classification misses, times the cloud-free share.
    tc = threshold_confidence(np.where(veg_before, d, np.nan), DROP, 0.05, below=True)
    amb = tc["near_share"]
    raw = tc["p_area_within_tol"] * 0.9 * (1 - max(clouds))
    cal = load_cal("ndvi_difference")
    px = pixel_km2(res)
    classes = np.zeros(d.shape, dtype="uint8")
    classes[decline] = 1
    classes[gain] = 2
    mask = save_overlay(job, nir, classes, PALETTE, {"1": "greenness fell", "2": "greenness rose"}, cfg)
    return TileResult(job_id=job.job_id, tile_id=job.tile_id, status=TileStatus.ok,
                      value=round(float(decline.sum()) * px, 4), unit="km2", confidence=round(cal(raw), 3), mask=mask,
                      scenes=[scene_ev(before.scene, "before"), scene_ev(after.scene, "after")],
                      params={"method": "Sentinel-2 NDVI difference on pixels clear on both dates", "sensor": "S2",
                              "selection": after.reason, "pairing": before.reason, "res_m": res,
                              "fit": {"drop": DROP, "vegetated_before": VEGETATED, "ambiguous_share": round(amb, 4)},
                              "mean_ndvi_before": round(float(np.nanmean(ndvi[0][valid])), 3),
                              "mean_ndvi_after": round(float(np.nanmean(ndvi[1][valid])), 3),
                              "vegetated_before_km2": round(float(veg_before.sum()) * px, 4),
                              "gain_km2": round(float(gain.sum()) * px, 4), "cloud_share": [round(c, 3) for c in clouds],
                              "raw_quality": round(raw, 4), "measured_km2": round(float(valid.sum()) * px, 4),
                              "sigma_abs_km2": round(tc["sigma_rel"] * max(tc["class_share"], 0.05) * float(veg_before.sum()) * px, 4),
                              "sigma_floor_km2": round(0.05 * float(veg_before.sum()) * px, 4),
                              "evidence_factor": round(0.9 * (1 - max(clouds)), 3),
                              "calibration": cal.status})
