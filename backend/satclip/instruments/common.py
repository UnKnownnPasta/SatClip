"""Shared, transparent building blocks for instruments: histogram thresholding with a
bimodality test, region clipping, small-blob removal, map overlays and tile results."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Optional

import numpy as np

from ..models import TileJob, TileResult, TileStatus
from ..receipt import digest

ROOT = Path(__file__).resolve().parents[3]


def abstain(job: TileJob, reason: str, **params) -> TileResult:
    return TileResult(job_id=job.job_id, tile_id=job.tile_id, status=TileStatus.abstain, reason=reason, params=params)


def db(linear: np.ndarray) -> np.ndarray:
    with np.errstate(divide="ignore", invalid="ignore"):
        out = 10 * np.log10(linear)
    out[~np.isfinite(out)] = np.nan
    return out


def norm_diff(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    with np.errstate(divide="ignore", invalid="ignore"):
        out = (a - b) / (a + b)
    out[~np.isfinite(out)] = np.nan
    return out


def otsu(values: np.ndarray, bins: int = 256) -> float:
    v = values[np.isfinite(values)]
    hist, edges = np.histogram(v, bins=bins)
    centers = (edges[:-1] + edges[1:]) / 2
    w0 = np.cumsum(hist)
    w1 = w0[-1] - w0
    m = np.cumsum(hist * centers)
    with np.errstate(divide="ignore", invalid="ignore"):
        mu0 = m / w0
        mu1 = (m[-1] - m) / w1
        between = w0 * w1 * (mu0 - mu1) ** 2
    between[~np.isfinite(between)] = -1
    return float(centers[int(np.argmax(between))])


def kittler_illingworth(values: np.ndarray, bins: int = 256) -> float:
    """Minimum-error threshold (Kittler and Illingworth 1986). Unlike Otsu it allows the two classes
    different spreads, which matters for SAR where land is much more variable than calm water."""
    v = values[np.isfinite(values)]
    hist, edges = np.histogram(v, bins=bins)
    c = (edges[:-1] + edges[1:]) / 2
    p = hist / max(hist.sum(), 1)
    P1 = np.cumsum(p)
    P2 = 1 - P1
    m1c = np.cumsum(p * c)
    m2c = m1c[-1] - m1c
    s1c = np.cumsum(p * c * c)
    s2c = s1c[-1] - s1c
    with np.errstate(divide="ignore", invalid="ignore"):
        mu1, mu2 = m1c / P1, m2c / P2
        var1, var2 = s1c / P1 - mu1 ** 2, s2c / P2 - mu2 ** 2
        J = 1 + 2 * (P1 * np.log(np.sqrt(var1)) + P2 * np.log(np.sqrt(var2))) - 2 * (P1 * np.log(P1) + P2 * np.log(P2))
    ok = (P1 > 0.02) & (P2 > 0.02) & (var1 > 1e-6) & (var2 > 1e-6) & np.isfinite(J)
    if not ok.any():
        return otsu(values, bins)
    J[~ok] = np.inf
    return float(c[int(np.argmin(J))])


def threshold_confidence(values: np.ndarray, t: float, sigma: float, below: bool = True,
                         tol: float = 0.2, floor: float = 0.05) -> dict[str, float]:
    """Probability that the class area is within +/- tol (relative) if the threshold is off by a
    Gaussian error of standard deviation `sigma`. Area sensitivity is the histogram density at the
    threshold, estimated from the share of pixels within +/- sigma:
        sigma_rel = near / (2 * max(class share, floor));  P = erf(tol / (sigma_rel * sqrt 2)).
    `floor` stops tiny classes (a tile with almost no water) from looking infinitely uncertain."""
    from math import erf, sqrt
    v = values[np.isfinite(values)]
    if not v.size:
        return {"near_share": 1.0, "class_share": 0.0, "sigma_rel": 1.0, "p_area_within_tol": 0.0}
    near = float((np.abs(v - t) < sigma).mean())
    share = float((v < t).mean() if below else (v > t).mean())
    s_rel = near / (2 * max(share, floor))
    p = 1.0 if s_rel == 0 else erf(tol / (s_rel * sqrt(2)))
    return {"near_share": round(near, 4), "class_share": round(share, 4), "sigma_rel": round(s_rel, 4),
            "p_area_within_tol": round(p, 4)}


def split_stats(values: np.ndarray, t: float) -> dict[str, float]:
    """Ashman D separability and minority share of a two-class split (archive A086)."""
    v = values[np.isfinite(values)]
    lo, hi = v[v < t], v[v >= t]
    if lo.size < 2 or hi.size < 2:
        return {"ashman_d": 0.0, "minority": 0.0, "mean_low": float("nan"), "mean_high": float("nan")}
    d = np.sqrt(2) * abs(lo.mean() - hi.mean()) / np.sqrt(lo.var() + hi.var() + 1e-9)
    return {"ashman_d": float(d), "minority": float(min(lo.size, hi.size) / v.size),
            "mean_low": float(lo.mean()), "mean_high": float(hi.mean())}


def region_mask(job: TileJob, raster) -> Optional[np.ndarray]:
    """True inside the named district (in the raster's own grid). None when no region was named."""
    if not job.region:
        return None
    from rasterio.features import geometry_mask
    from rasterio.warp import transform_geom
    from shapely.geometry import box, mapping

    from ..gazetteer import outline_lonlat
    geom = outline_lonlat(job.region)
    if geom is None:
        return None
    clip = geom.intersection(box(*job.bbox))
    if clip.is_empty:
        return np.zeros(raster.data.shape, dtype=bool)
    native = transform_geom("EPSG:4326", raster.crs, mapping(clip))
    return geometry_mask([native], out_shape=raster.data.shape, transform=raster.transform, invert=True)


def drop_small(mask: np.ndarray, min_px: int) -> np.ndarray:
    """Remove connected blobs smaller than min_px (speckle), archive A083."""
    if min_px <= 1 or not mask.any():
        return mask
    from scipy import ndimage
    lab, n = ndimage.label(mask)
    if n == 0:
        return mask
    sizes = ndimage.sum(mask, lab, index=np.arange(1, n + 1))
    keep = np.zeros(n + 1, dtype=bool)
    keep[1:] = sizes >= min_px
    return keep[lab]


def pixel_km2(res_m: float) -> float:
    return (res_m * res_m) / 1e6


def save_overlay(job: TileJob, raster, classes: np.ndarray, palette: dict[int, tuple[int, int, int, int]],
                 legend: dict[str, str], cfg: dict[str, Any]) -> Optional[dict[str, Any]]:
    """Reproject a class map to the tile's lon/lat box and save it as a small RGBA PNG.
    Class 0 is transparent. Returns {"href", "bounds", "legend"} or None if saving fails."""
    try:
        from PIL import Image
        from rasterio.transform import from_bounds
        from rasterio.warp import Resampling, reproject
    except ImportError:
        return None
    h, w = classes.shape
    dst = np.zeros((h, w), dtype="uint8")
    reproject(classes.astype("uint8"), dst, src_transform=raster.transform, src_crs=raster.crs,
              dst_transform=from_bounds(*job.bbox, w, h), dst_crs="EPSG:4326", resampling=Resampling.nearest)
    rgba = np.zeros((h, w, 4), dtype="uint8")
    for k, col in palette.items():
        rgba[dst == k] = col
    out_dir = ROOT / cfg.get("outputs", {}).get("masks_dir", "backend/runtime/masks")
    os.makedirs(out_dir, exist_ok=True)
    name = digest({"j": job.instrument, "t": job.tile_id, "w": [x.model_dump(mode="json") for x in job.windows],
                   "r": job.region})[:20] + ".png"
    Image.fromarray(rgba, "RGBA").save(out_dir / name, optimize=True)
    colors = {str(k): "#%02x%02x%02x" % tuple(c[:3]) for k, c in palette.items() if k}
    return {"href": f"/v1/masks/{name}", "bounds": list(job.bbox), "legend": legend, "colors": colors}


def scene_ev(scene, role: Optional[str] = None) -> dict[str, Any]:
    ev = scene.evidence()
    if role:
        ev["role"] = role
    return ev
