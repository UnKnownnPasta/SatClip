"""Windowed reads of Cloud Optimized GeoTIFFs (OGC COG, archive A049).

A tile's lon/lat box is converted to the raster's own CRS and only the overlapping internal
blocks are fetched with HTTP range requests. Pixels are never reprojected for measurement;
reprojection happens only for map overlays.
"""
from __future__ import annotations

import os
import threading
import time
from dataclasses import dataclass
from typing import Any, Callable, Optional

import numpy as np

# GDAL settings for efficient remote COG access (range requests, no directory listing).
GDAL_ENV = {
    "GDAL_DISABLE_READDIR_ON_OPEN": "EMPTY_DIR",
    "CPL_VSIL_CURL_ALLOWED_EXTENSIONS": ".tif,.tiff,.TIF",
    "GDAL_HTTP_MERGE_CONSECUTIVE_RANGES": "YES",
    "GDAL_HTTP_MULTIPLEX": "YES",
    "GDAL_HTTP_MAX_RETRY": "3",
    "GDAL_HTTP_RETRY_DELAY": "1",
    "VSI_CACHE": "TRUE",
    "AWS_NO_SIGN_REQUEST": "YES",
}
if os.environ.get("CURL_CA_BUNDLE") is None and os.path.exists("/root/.ccr/ca-bundle.crt"):
    GDAL_ENV["CURL_CA_BUNDLE"] = "/root/.ccr/ca-bundle.crt"

CLOUDY_SCL = (3, 8, 9, 10)  # cloud shadow, cloud medium, cloud high, thin cirrus
NODATA_SCL = (0,)


@dataclass
class RasterWindow:
    data: np.ndarray            # float32, NaN where nodata or outside the raster
    crs: str
    transform: Any              # affine transform of `data`
    res_m: float
    valid_fraction: float
    bounds: tuple[float, float, float, float]  # in `crs`


READ_ATTEMPTS = 4   # transient HTTP read failures are retried; a tile that still fails is reported as an error


def _nearest(a: np.ndarray, h: int, w: int) -> np.ndarray:
    """Deterministic nearest-neighbour resize (pixel centres), done in numpy rather than by GDAL."""
    H, W = a.shape
    if (H, W) == (h, w):
        return a
    ys = np.minimum(((np.arange(h) + 0.5) * H / h).astype(int), H - 1)
    xs = np.minimum(((np.arange(w) + 0.5) * W / w).astype(int), W - 1)
    return a[np.ix_(ys, xs)]


def _average(a: np.ndarray, h: int, w: int) -> np.ndarray:
    """Deterministic area-average resize: each source pixel goes to the output pixel containing its
    centre; NaN pixels are ignored and an output pixel with no valid source pixel is NaN."""
    H, W = a.shape
    if (H, W) == (h, w):
        return a
    iy = np.minimum(((np.arange(H) + 0.5) * h / H).astype(int), h - 1)
    ix = np.minimum(((np.arange(W) + 0.5) * w / W).astype(int), w - 1)
    idx = (iy[:, None] * w + ix[None, :]).ravel()
    v = a.ravel()
    ok = np.isfinite(v)
    tot = np.bincount(idx[ok], weights=v[ok].astype("float64"), minlength=h * w)
    cnt = np.bincount(idx[ok], minlength=h * w)
    with np.errstate(invalid="ignore", divide="ignore"):
        out = np.where(cnt > 0, tot / np.maximum(cnt, 1), np.nan)
    return out.reshape(h, w).astype("float32")


RESIZE = {"nearest": _nearest, "average": _average}


def read_window(href: str, bbox_lonlat, res_m: Optional[float] = None, band: int = 1,
                resampling: str = "nearest") -> RasterWindow:
    """Read one band for a lon/lat box at res_m.

    Run 8 found that letting GDAL decimate (out_shape smaller than the window) is not deterministic
    under concurrent reads: whether a block is already in GDAL's cache changes the code path, and a
    3-pixel strip came back with different source pixels. So the window is snapped to whole native
    pixels, read at native resolution, and resized here ("average" for reflectance and backscatter,
    "nearest" for class bands such as SCL). Reads are retried on transient I/O errors."""
    import rasterio
    from rasterio.errors import RasterioIOError
    from rasterio.transform import from_bounds
    from rasterio.warp import transform_bounds
    from rasterio.windows import from_bounds as win_from_bounds

    if resampling not in RESIZE:
        raise ValueError(f"resampling must be one of {sorted(RESIZE)} (deterministic numpy resize)")
    last: Optional[Exception] = None
    for attempt in range(READ_ATTEMPTS):
        # GDAL's /vsicurl cache remembers a failed byte range, so a retry must use a fresh URL key.
        url = href if attempt == 0 else f"{href}{'&' if '?' in href else '?'}satclip_retry={attempt}"
        try:
            with rasterio.Env(**GDAL_ENV), rasterio.open(url) as ds:
                crs = ds.crs.to_string()
                left, bottom, right, top = transform_bounds("EPSG:4326", ds.crs, *bbox_lonlat, densify_pts=21)
                native = abs(ds.res[0])
                res = float(res_m or native)
                w = max(1, int(round((right - left) / res)))
                h = max(1, int(round((top - bottom) / res)))
                win = win_from_bounds(left, bottom, right, top, transform=ds.transform).round_offsets().round_lengths()
                arr = ds.read(band, window=win, boundless=True, masked=True)
                data = np.ma.filled(arr.astype("float32"), np.nan)
                if ds.nodata is not None and not np.isnan(ds.nodata):
                    data[data == ds.nodata] = np.nan
                wl, wt = ds.transform * (win.col_off, win.row_off)
                wr, wb = ds.transform * (win.col_off + win.width, win.row_off + win.height)
            data = RESIZE[resampling](data, h, w)
            left, right, bottom, top = wl, wr, min(wb, wt), max(wb, wt)
            break
        except RasterioIOError as exc:
            last = exc
            time.sleep(0.5 * (attempt + 1))
    else:
        raise last  # type: ignore[misc]
    valid = float(np.isfinite(data).mean()) if data.size else 0.0
    return RasterWindow(data=data, crs=crs, transform=from_bounds(left, bottom, right, top, w, h), res_m=res,
                        valid_fraction=valid, bounds=(left, bottom, right, top))


def scl_cloud_fraction(scl: np.ndarray) -> float:
    """Share of valid pixels flagged as cloud, shadow or cirrus in the Sentinel-2 scene classification."""
    v = scl[np.isfinite(scl)]
    v = v[~np.isin(v, NODATA_SCL)]
    if v.size == 0:
        return 1.0
    return float(np.isin(v, CLOUDY_SCL).mean())


# ---------- Planetary Computer signing ----------

_TOKENS: dict[str, tuple[str, float]] = {}
_LOCK = threading.Lock()
PC_TOKEN_URL = "https://planetarycomputer.microsoft.com/api/sas/v1/token/{collection}"


def _fetch_pc_token(collection: str) -> tuple[str, float]:
    import httpx
    from datetime import datetime
    r = httpx.get(PC_TOKEN_URL.format(collection=collection), timeout=20)
    r.raise_for_status()
    d = r.json()
    exp = datetime.fromisoformat(d["msft:expiry"].replace("Z", "+00:00")).timestamp()
    return d["token"], exp


def sign_href(href: str, signing: Optional[str], collection: str,
              fetch_token: Callable[[str], tuple[str, float]] = _fetch_pc_token) -> str:
    """Append a short-lived anonymous SAS token for Planetary Computer assets; other hrefs pass through."""
    if signing != "planetary-computer":
        return href
    with _LOCK:
        tok = _TOKENS.get(collection)
        if not tok or tok[1] - time.time() < 300:
            tok = fetch_token(collection)
            _TOKENS[collection] = tok
    return f"{href}{'&' if '?' in href else '?'}{tok[0]}"
