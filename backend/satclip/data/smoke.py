"""Live smoke check against the public catalogues: `python -m satclip.data.smoke`.

Searches Sentinel-1 and Sentinel-2 over a Barpeta tile, selects scenes, and reads one band window.
"""
from __future__ import annotations

import sys
from datetime import date

from ..config import settings
from ..models import DateWindow, Intent
from .provider import DataProvider

TILE = (91.0, 26.3, 91.05, 26.35)


def main() -> int:
    p = DataProvider.from_settings(settings())
    ok = True
    for intent, w in [(Intent.water_extent, DateWindow(start=date(2024, 7, 5), end=date(2024, 7, 17))),
                      (Intent.vegetation_change, DateWindow(start=date(2024, 11, 5), end=date(2024, 11, 17)))]:
        sel = p.for_tile(intent, [w], TILE)[0]
        print(f"{intent.value}: ok={sel.ok} sensor={sel.sensor} scene={sel.scene.id if sel.scene else None}")
        print(f"  reason: {sel.reason}")
        if sel.ok:
            band = "vv" if sel.sensor == "S1" else "nir"
            try:
                r = p.read(sel.scene, band, TILE, res_m=40)
                print(f"  read {band}: shape={r.data.shape} valid={r.valid_fraction:.2f} crs={r.crs}")
            except Exception as exc:  # noqa: BLE001
                ok = False
                print(f"  read failed: {exc!r}")
        else:
            ok = False
    print("catalogue log:", p.stac.log)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
