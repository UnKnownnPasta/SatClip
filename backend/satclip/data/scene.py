"""Catalogue-neutral scene record. Each catalogue names bands differently (Earth Search uses
`green`, Planetary Computer `B03`, CDSE `B03_10m`); instruments only ever see canonical names."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

# canonical name -> aliases seen in catalogues (lower-cased)
BAND_ALIASES: dict[str, tuple[str, ...]] = {
    "blue": ("blue", "b02", "b02_10m"),
    "green": ("green", "b03", "b03_10m"),
    "red": ("red", "b04", "b04_10m"),
    "nir": ("nir", "b08", "b08_10m"),
    "swir16": ("swir16", "b11", "b11_20m"),
    "scl": ("scl", "scl_20m"),
    "vv": ("vv",),
    "vh": ("vh",),
}
_LOOKUP = {alias: canon for canon, aliases in BAND_ALIASES.items() for alias in aliases}
REFLECTANCE = {"blue", "green", "red", "nir", "swir16"}


@dataclass
class Scene:
    id: str
    sensor: str                     # "S1" or "S2"
    datetime: str
    bbox: tuple[float, float, float, float]
    collection: str
    assets: dict[str, str]          # canonical band -> href
    catalog: Optional[str] = None
    cloud_cover: Optional[float] = None
    orbit_state: Optional[str] = None
    relative_orbit: Optional[int] = None
    platform: Optional[str] = None
    epsg: Optional[int] = None
    needs_signing: Optional[str] = None
    readable: bool = True
    scales: dict[str, tuple[float, float]] = field(default_factory=dict)  # band -> (scale, offset)
    processing_baseline: Optional[str] = None
    boa_offset_applied: Optional[bool] = None  # Earth Search: DNs already have the -1000 offset removed

    @property
    def date(self) -> str:
        return self.datetime[:10]

    def covers(self, bbox) -> bool:
        a = self.bbox
        return a[0] <= bbox[0] and a[1] <= bbox[1] and a[2] >= bbox[2] and a[3] >= bbox[3]

    def scale_offset(self, band: str) -> tuple[float, float]:
        """Digital number to physical value: value = dn * scale + offset."""
        if self.sensor == "S2" and band in REFLECTANCE and self.boa_offset_applied:
            # Measured on live data (2026-10-05): Earth Search DNs are already harmonised even though
            # raster:bands still lists offset -0.1, so applying it again gives negative reflectance.
            return (self.scales.get(band, (1e-4, 0.0))[0], 0.0)
        if band in self.scales:
            return self.scales[band]
        if self.sensor == "S2" and band in REFLECTANCE:
            # ESA processing baseline 04.00 (from 2022-01-25) adds a -1000 DN offset.
            pb = self.processing_baseline
            new = (float(pb) >= 4.0) if pb else self.date >= "2022-01-25"
            return 1e-4, (-0.1 if new else 0.0)
        return 1.0, 0.0

    def evidence(self) -> dict[str, Any]:
        """The scene facts printed on an evidence card and stored in the receipt."""
        return {"id": self.id, "date": self.date, "datetime": self.datetime, "sensor": self.sensor,
                "catalog": self.catalog, "collection": self.collection, "platform": self.platform,
                "cloud_cover": None if self.cloud_cover is None else round(self.cloud_cover, 2),
                "orbit_state": self.orbit_state, "relative_orbit": self.relative_orbit}


def _epsg(props: dict[str, Any]) -> Optional[int]:
    if props.get("proj:epsg"):
        return int(props["proj:epsg"])
    code = props.get("proj:code")
    if isinstance(code, str) and code.upper().startswith("EPSG:"):
        return int(code.split(":")[1])
    return None


def normalize_item(item: dict[str, Any], catalog: Optional[str] = None, needs_signing: Optional[str] = None,
                   readable: bool = True) -> Scene:
    props = item.get("properties", {})
    coll = item.get("collection") or ""
    platform = props.get("platform")
    sensor = "S1" if ("sentinel-1" in coll or str(platform).lower().startswith("sentinel-1")) else "S2"
    assets, scales = {}, {}
    for key, asset in (item.get("assets") or {}).items():
        canon = _LOOKUP.get(key.lower())
        if not canon or canon in assets or not asset.get("href"):
            continue
        assets[canon] = asset["href"]
        rb = (asset.get("raster:bands") or [{}])[0]
        if "scale" in rb or "offset" in rb:
            scales[canon] = (float(rb.get("scale", 1.0)), float(rb.get("offset", 0.0)))
    rel = props.get("sat:relative_orbit")
    return Scene(id=item["id"], sensor=sensor, datetime=props.get("datetime") or "", bbox=tuple(item["bbox"][:4]),
                 collection=coll, assets=assets, catalog=catalog, cloud_cover=props.get("eo:cloud_cover"),
                 orbit_state=props.get("sat:orbit_state"), relative_orbit=int(rel) if rel is not None else None,
                 platform=platform, epsg=_epsg(props), needs_signing=needs_signing, readable=readable,
                 scales=scales, processing_baseline=props.get("s2:processing_baseline"),
                 boa_offset_applied=props.get("earthsearch:boa_offset_applied"))
