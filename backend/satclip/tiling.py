"""Deterministic global tile grid. Same tile size gives the same tile IDs for any AOI,
so overlapping questions share tiles and cache entries (ARCHITECTURE.md 6.1)."""
from __future__ import annotations

import math

from .models import BBox


def tile_id(col: int, row: int, size: float) -> str:
    return f"z{size:g}_{col}_{row}"


def tiles_for_bbox(bbox: BBox, size: float) -> list[tuple[str, BBox]]:
    min_lon, min_lat, max_lon, max_lat = bbox
    c0, c1 = math.floor((min_lon + 180) / size), math.ceil((max_lon + 180) / size - 1e-9)
    r0, r1 = math.floor((min_lat + 90) / size), math.ceil((max_lat + 90) / size - 1e-9)
    out = []
    for r in range(r0, r1):
        for c in range(c0, c1):
            tb = (round(c * size - 180, 9), round(r * size - 90, 9),
                  round((c + 1) * size - 180, 9), round((r + 1) * size - 90, 9))
            out.append((tile_id(c, r, size), tb))
    return out


def tile_area_km2(bbox: BBox) -> float:
    """Approximate area of a lon/lat box on a sphere (good to well under 1% at tile scale)."""
    r = 6371.0088
    lon0, lat0, lon1, lat1 = map(math.radians, bbox)
    return r * r * abs(lon1 - lon0) * abs(math.sin(lat1) - math.sin(lat0))
