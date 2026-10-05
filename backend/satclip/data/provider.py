"""The single entry point instruments use to get pixels (ARCHITECTURE.md 6.6).

Searches run once per 1 degree *search cell* per sensor and date window, so every tile of a
district shares one cached catalogue call. Instruments see canonical band names and physical
values (reflectance for Sentinel-2, linear backscatter for Sentinel-1 RTC).
"""
from __future__ import annotations

import math
import threading
from datetime import timedelta
from typing import Any, Optional

import numpy as np

from ..models import DateWindow, Intent
from .cog import RasterWindow, read_window, scl_cloud_fraction, sign_href
from .scene import Scene
from .select import Selection, middle, pair_for_change, select_scenes, sensor_order
from .stac import StacClient, StacError

CHANGE = {Intent.water_change, Intent.vegetation_change}


def search_cell(bbox, deg: float = 1.0) -> tuple[float, float, float, float]:
    x0, y0 = math.floor(bbox[0] / deg) * deg, math.floor(bbox[1] / deg) * deg
    return (round(x0, 9), round(y0, 9), round(x0 + deg, 9), round(y0 + deg, 9))


class DataProvider:
    def __init__(self, stac: StacClient, cfg: dict[str, Any]):
        self.stac, self.cfg = stac, cfg
        self.cell_deg = float(cfg.get("stac", {}).get("search_cell_deg", 1.0))
        self._cache: dict[tuple, list[Scene]] = {}
        self._lock = threading.Lock()
        self.errors: list[str] = []

    @classmethod
    def from_settings(cls, cfg: dict[str, Any]) -> "DataProvider":
        return cls(StacClient.from_settings(cfg), cfg)

    def _search_window(self, w: DateWindow) -> tuple:
        days = int(self.cfg.get("scene", {}).get("max_days_from_request", 12))
        mid = middle(w)
        return min(w.start, mid - timedelta(days=days)), max(w.end, mid + timedelta(days=days))

    def candidates(self, sensor: str, tile, window: DateWindow) -> list[Scene]:
        cell = search_cell(tile, self.cell_deg)
        start, end = self._search_window(window)
        key = (sensor, cell, start, end)
        with self._lock:
            if key in self._cache:
                return self._cache[key]
        try:
            found = self.stac.search(sensor, cell, start, end)
        except StacError as exc:
            self.errors.append(f"{sensor}: {exc}")
            found = []
        with self._lock:
            self._cache[key] = found
        return found

    def _cands(self, intent: Intent, tile, window: DateWindow) -> dict[str, list[Scene]]:
        return {s: self.candidates(s, tile, window) for s in sensor_order(intent, window, self.cfg)}

    def for_tile(self, intent: Intent, windows: list[DateWindow], tile) -> list[Selection]:
        """One selection for single-date intents; [before, after] for change intents with two windows."""
        if intent in CHANGE and len(windows) >= 2:
            b, a = windows[0], windows[-1]
            cb, ca = self._cands(intent, tile, b), self._cands(intent, tile, a)
            # the before window must offer the sensor the after window may pick
            for s in ca:
                cb.setdefault(s, self.candidates(s, tile, b))
            return list(pair_for_change(intent, b, a, tile, cb, ca, self.cfg))
        sel = select_scenes(intent, windows[0], tile, self._cands(intent, tile, windows[0]), self.cfg)
        if not sel.ok and self.errors and not any(self._cands(intent, tile, windows[0]).values()):
            sel.reason = "no catalogue reachable (" + self.errors[-1][:120] + ")"
        return [sel]

    def read(self, scene: Scene, band: str, tile, res_m: float = 20.0) -> RasterWindow:
        href = sign_href(scene.assets[band], scene.needs_signing, scene.collection)
        resampling = "nearest" if band == "scl" else "average"
        r = read_window(href, tile, res_m=res_m, resampling=resampling)
        scale, offset = scene.scale_offset(band)
        if (scale, offset) != (1.0, 0.0):
            r.data = r.data * np.float32(scale) + np.float32(offset)
        return r

    def tile_is_clear(self, scene: Scene, tile, res_m: float = 20.0) -> tuple[bool, float, Optional[RasterWindow]]:
        """For optical scenes: is this tile's cloud share under the configured limit? Radar is always clear."""
        if scene.sensor != "S2":
            return True, 0.0, None
        scl = self.read(scene, "scl", tile, res_m)
        frac = scl_cloud_fraction(scl.data)
        lim = float(self.cfg.get("scene", {}).get("max_tile_cloud_pct", 30)) / 100
        return frac <= lim, frac, scl


_PROVIDER: Optional[DataProvider] = None


def get_provider() -> DataProvider:
    global _PROVIDER
    if _PROVIDER is None:
        from ..config import settings
        _PROVIDER = DataProvider.from_settings(settings())
    return _PROVIDER


def set_provider(p: Optional[DataProvider]) -> None:
    """Tests and the API inject a provider (for example one backed by recorded fixtures)."""
    global _PROVIDER
    _PROVIDER = p
