"""Build backend/satclip/resources/districts.json from geoBoundaries gbOpen IND ADM2 and ADM1
(simplified GeoJSON, ODbL 1.0, source lgdirectory.gov.in via Pathways Data; build 2023-12-12).

Usage: python tools/build_gazetteer.py ADM2.geojson ADM1.geojson
Download links: https://www.geoboundaries.org/api/current/gbOpen/IND/ADM2/ (simplifiedGeometryGeoJSON)
(GitHub LFS files: fetch through media.githubusercontent.com).
Each district gets: name, state, bbox, and an outline simplified to about 0.01 degree.
"""
import json
import os
import sys
import unicodedata

from shapely.geometry import mapping, shape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "backend", "satclip", "resources", "districts.json")


def ascii_name(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().strip()


def main(adm2_path, adm1_path):
    states = [(ascii_name(f["properties"]["shapeName"]), shape(f["geometry"]).buffer(0))
              for f in json.load(open(adm1_path, encoding="utf-8"))["features"]]
    out = []
    for f in json.load(open(adm2_path, encoding="utf-8"))["features"]:
        g = shape(f["geometry"]).buffer(0)
        p = g.representative_point()
        state = next((n for n, sg in states if sg.contains(p)), None)
        if state is None:
            state = min(states, key=lambda s: s[1].distance(p))[0]
        simple = g.simplify(0.01, preserve_topology=True)
        geom = mapping(simple)

        def rnd(c):
            return [rnd(x) for x in c] if isinstance(c[0], (list, tuple)) else [round(c[0], 4), round(c[1], 4)]
        out.append({"name": ascii_name(f["properties"]["shapeName"]), "state": state,
                    "bbox": [round(v, 4) for v in g.bounds], "geometry": {"type": geom["type"], "coordinates": rnd(geom["coordinates"])}})
    out.sort(key=lambda d: (d["name"].lower(), d["state"]))
    meta = {"source": "geoBoundaries gbOpen IND ADM2 (build 2023-12-12), lgdirectory.gov.in via Pathways Data",
            "license": "ODbL 1.0", "url": "https://www.geoboundaries.org/", "count": len(out)}
    json.dump({"meta": meta, "districts": out}, open(OUT, "w", encoding="utf-8"), separators=(",", ":"))
    print(f"wrote {len(out)} districts to {OUT} ({os.path.getsize(OUT)//1024} KB)")


if __name__ == "__main__":
    main(*sys.argv[1:3])
