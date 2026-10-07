"""Turn optical and radar rasters into the 8-bit RGB images an off-the-shelf VLM expects.

Optical (Sentinel-2): true colour B4, B3, B2, reflectance 0 to 0.3 stretched to 0 to 255.
Radar (Sentinel-1): the common false-colour composite R = VV, G = VH, B = VV - VH (all dB), each with a
fixed stretch, so the same backscatter always gives the same colour (EarthDial and SARChat, archive A003
and A021, also feed SAR as a 3-channel image). Fixed stretches keep images comparable across scenes and
dates; per-image percentile stretches would hide real change.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np

S1_STRETCH = {"vv": (-25.0, 0.0), "vh": (-30.0, -5.0), "ratio": (0.0, 15.0)}


def _scale(x: np.ndarray, lo: float, hi: float) -> np.ndarray:
    y = (np.nan_to_num(x, nan=lo) - lo) / (hi - lo)
    return (np.clip(y, 0, 1) * 255).astype("uint8")


def s2_rgb(red: np.ndarray, green: np.ndarray, blue: np.ndarray, max_reflectance: float = 0.3) -> np.ndarray:
    """Inputs are surface reflectance (0 to 1). BigEarthNet stores DN = reflectance x 10000."""
    return np.dstack([_scale(b, 0.0, max_reflectance) for b in (red, green, blue)])


def s1_false_colour(vv_db: np.ndarray, vh_db: np.ndarray) -> np.ndarray:
    return np.dstack([_scale(vv_db, *S1_STRETCH["vv"]), _scale(vh_db, *S1_STRETCH["vh"]),
                      _scale(vv_db - vh_db, *S1_STRETCH["ratio"])])


def save_png(rgb: np.ndarray, path: Path) -> Path:
    from PIL import Image
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(rgb, "RGB").save(path, optimize=True)
    return path
