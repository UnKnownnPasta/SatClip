"""Auto-generate Indian image Q&A pairs for the language layer from open land-cover labels.

Why: RSVQA and BigEarthNet are European. The explainer must also see Indian landscapes (paddy, tea, char
islands, braided rivers, dense villages) and answer simple follow-ups about the shown image honestly.

Label source (decided in run 7, see training/README.md):
  * ESA WorldCover 10 m v200 (2021), CC BY 4.0, read as public COGs. Its classes give per-chip shares.
  * OpenStreetMap was tested first (Overpass, October 2026): rural Indian districts have almost no landuse
    polygons (a 35 x 33 km box in Barpeta returned 85 features, 5 of them farmland), so "no farmland in OSM"
    does not mean "no farmland". OSM is therefore used only for positive, named-feature questions
    (`--osm`: "Is a mapped river or water body visible?" answered yes only when OSM has one), never for
    absence or shares.
  * Bhuvan land-use layers are not used: their terms do not clearly allow redistribution of derived
    training data. Revisit if NRSC confirms a licence.

Images: Sentinel-2 L2A true colour from the dry season of 2021 (the WorldCover epoch) and, with --sar,
a Sentinel-1 RTC false-colour image of the same chip, both through SatClip's own data layer (so the same
catalogues, scaling and signing as production). Chips are 256 x 256 px at 10 m, sampled inside district
outlines. Districts follow the 80/10/10 hash split of build_intent_data.py, so test districts are unseen.

Answers are only written when the label is clear-cut (for example cropland >= 15% for "yes", < 1% for
"no"); ambiguous chips get no question rather than a guessed answer. Each row records the WorldCover shares
so answers can be audited.

    python training/lora/build_india_qa.py --districts 40 --chips 3            # small run, about 10 min
    python training/lora/build_india_qa.py --districts 300 --chips 6 --sar     # full run (hours)
Output: training/data/india_qa/{train,val,test}.jsonl and images/ (gitignored).
"""
from __future__ import annotations

import argparse
import json
import random
import sys
from datetime import date
from pathlib import Path
from typing import Any, Optional

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from schema import ROOT  # noqa: E402
from build_intent_data import split_of  # noqa: E402
from images import s1_false_colour, s2_rgb, save_png  # noqa: E402

sys.path.insert(0, str(ROOT / "backend"))

OUT = ROOT / "training" / "data" / "india_qa"
WC_URL = "https://esa-worldcover.s3.eu-central-1.amazonaws.com/v200/2021/map/ESA_WorldCover_10m_2021_v200_{tile}_Map.tif"
WC_CLASSES = {10: "tree cover", 20: "shrubland", 30: "grassland", 40: "cropland", 50: "built-up", 60: "bare or sparse ground",
              70: "snow and ice", 80: "open water", 90: "wetland", 95: "mangroves", 100: "moss and lichen"}
CHIP_PX, RES = 256, 10.0
WINDOWS = [(date(2021, 1, 10), date(2021, 2, 10)), (date(2021, 2, 10), date(2021, 3, 15)), (date(2020, 12, 1), date(2021, 1, 10))]
SYSTEM = ("You look at one satellite image of a place in India and answer briefly. Answer yes or no, or a short "
          "phrase. Say 'mixed' when no single type dominates. Never guess counts.")


def wc_tile(lon: float, lat: float) -> str:
    """WorldCover 3 x 3 degree tile name containing (lon, lat), for example N24E090."""
    la, lo = int(np.floor(lat / 3) * 3), int(np.floor(lon / 3) * 3)
    return f"{'N' if la >= 0 else 'S'}{abs(la):02d}{'E' if lo >= 0 else 'W'}{abs(lo):03d}"


def worldcover_shares(bbox: tuple[float, float, float, float]) -> Optional[dict[str, float]]:
    import rasterio
    from rasterio.windows import from_bounds
    cx, cy = (bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2
    with rasterio.open(WC_URL.format(tile=wc_tile(cx, cy))) as ds:
        a = ds.read(1, window=from_bounds(*bbox, ds.transform))
    if a.size == 0:
        return None
    v, c = np.unique(a[a > 0], return_counts=True)
    tot = c.sum()
    return {WC_CLASSES.get(int(k), str(k)): round(float(n / tot), 4) for k, n in zip(v, c)} if tot else None


def chip_bbox(lon: float, lat: float) -> tuple[float, float, float, float]:
    half_m = CHIP_PX * RES / 2
    dlat = half_m / 111_320
    dlon = half_m / (111_320 * np.cos(np.radians(lat)))
    return (round(lon - dlon, 6), round(lat - dlat, 6), round(lon + dlon, 6), round(lat + dlat, 6))


def sample_points(district: dict[str, Any], n: int, rng: random.Random) -> list[tuple[float, float]]:
    from shapely.geometry import Point, shape
    geom = shape(district["geometry"])
    x0, y0, x1, y1 = district["bbox"]
    pts: list[tuple[float, float]] = []
    for _ in range(n * 50):
        p = (rng.uniform(x0, x1), rng.uniform(y0, y1))
        if geom.contains(Point(p)):
            pts.append(p)
            if len(pts) == n:
                break
    return pts


def qa_from_shares(s: dict[str, float], rng: random.Random) -> list[tuple[str, str, str]]:
    """(question, answer, kind). Only clear-cut cases; thresholds are deliberately wide."""
    out = []
    crop, water, built, tree = (s.get("cropland", 0), s.get("open water", 0) + s.get("wetland", 0) * 0.5,
                                s.get("built-up", 0), s.get("tree cover", 0) + s.get("mangroves", 0))
    for name, share, q in (("cropland", crop, "Is there farmland in this image?"),
                           ("open water", water, "Is there open water such as a river or pond in this image?"),
                           ("built-up", built, "Are there built-up areas such as a town or villages in this image?"),
                           ("tree cover", tree, "Is there forest or tree cover in this image?")):
        if share >= 0.15:
            out.append((q, "yes", f"presence:{name}"))
        elif share < 0.01:
            out.append((q, "no", f"presence:{name}"))
    top = sorted(s.items(), key=lambda kv: -kv[1])
    if top and top[0][1] >= 0.6:
        out.append(("What is the main land cover in this image?", top[0][0], "dominant"))
    elif len(top) >= 2 and top[0][1] < 0.45 and top[0][1] + top[1][1] >= 0.7:
        out.append(("What is the main land cover in this image?", f"mixed: {top[0][0]} and {top[1][0]}", "dominant"))
    if built >= 0.3:
        out.append(("Is this area mostly urban or rural?", "urban", "urban_rural"))
    elif built < 0.05:
        out.append(("Is this area mostly urban or rural?", "rural", "urban_rural"))
    bins = [(0.0, 0.01, "almost none"), (0.01, 0.1, "under a tenth"), (0.1, 0.3, "between a tenth and a third"),
            (0.3, 0.6, "between a third and about half"), (0.6, 1.01, "more than half")]
    for lo, hi, label in bins:
        # skip values within 0.02 of a bin edge: the label would be a coin toss
        if lo + 0.02 <= water < hi - 0.02 or (lo == 0.0 and water < 0.008):
            out.append(("Roughly how much of this image is water?", label, "water_share"))
            break
    out.append(("How many houses are in this image?", "I cannot count objects reliably at 10 m resolution.", "refuse_count"))
    rng.shuffle(out)
    return out


def osm_water_named(bbox: tuple[float, float, float, float]) -> Optional[str]:
    """Positive-only OSM check: name of a mapped river or water body intersecting the chip, else None."""
    import httpx
    q = (f"[out:json][timeout:40];(way[\"waterway\"=\"river\"]({bbox[1]},{bbox[0]},{bbox[3]},{bbox[2]});"
         f"way[\"natural\"=\"water\"]({bbox[1]},{bbox[0]},{bbox[3]},{bbox[2]}););out tags 20;")
    for url in ("https://maps.mail.ru/osm/tools/overpass/api/interpreter", "https://overpass-api.de/api/interpreter"):
        try:
            r = httpx.post(url, data={"data": q}, timeout=60)
            r.raise_for_status()
            names = [e["tags"].get("name:en") or e["tags"].get("name") for e in r.json().get("elements", [])]
            names = [n for n in names if n]
            return names[0] if names else None
        except Exception:  # noqa: BLE001
            continue
    return None


def pick_s2(prov, bbox) -> Optional[Any]:
    from satclip.models import DateWindow
    for a, b in WINDOWS:
        cands = sorted((s for s in prov.candidates("S2", bbox, DateWindow(start=a, end=b)) if s.covers(bbox) and s.readable),
                       key=lambda s: s.cloud_cover if s.cloud_cover is not None else 100)
        for s in cands[:3]:
            ok, frac, _ = prov.tile_is_clear(s, bbox, 20.0)
            if ok and frac < 0.05:
                return s
    return None


def pick_s1(prov, bbox) -> Optional[Any]:
    from satclip.models import DateWindow
    for a, b in WINDOWS:
        for s in prov.candidates("S1", bbox, DateWindow(start=a, end=b)):
            if s.covers(bbox) and s.readable and "vv" in s.assets and "vh" in s.assets:
                return s
    return None


def build_chip(prov, district: dict[str, Any], pt: tuple[float, float], idx: int, args, rng: random.Random) -> list[dict]:
    bbox = chip_bbox(*pt)
    shares = worldcover_shares(bbox)
    if not shares:
        return []
    key = f"{district['name']}|{district['state']}"
    split = split_of(key)
    stem = f"{district['name'].replace(' ', '_')}_{district['state'].replace(' ', '_')}_{idx}"
    rows: list[dict] = []
    s2 = pick_s2(prov, bbox)
    images = []
    if s2 is not None:
        bands = [prov.read(s2, b, bbox, RES).data for b in ("red", "green", "blue")]
        if all(b.shape == bands[0].shape for b in bands) and np.isfinite(bands[0]).mean() > 0.95:
            images.append(("S2", s2, save_png(s2_rgb(*bands), OUT / "images" / f"{stem}_s2.png")))
    if args.sar:
        s1 = pick_s1(prov, bbox)
        if s1 is not None:
            vv, vh = (10 * np.log10(np.clip(prov.read(s1, b, bbox, RES).data, 1e-6, None)) for b in ("vv", "vh"))
            images.append(("S1", s1, save_png(s1_false_colour(vv, vh), OUT / "images" / f"{stem}_s1.png")))
    if not images:
        return []
    qa = qa_from_shares(shares, rng)
    if args.osm:
        name = osm_water_named(bbox)
        if name:
            qa.append(("Is a mapped river or water body visible here? If so, name it.", f"yes, {name}", "osm_named_water"))
    for sensor, scene, png in images:
        for q, a, kind in qa:
            if sensor == "S1" and kind.startswith(("presence:built", "presence:tree", "dominant", "urban")):
                continue  # radar false colour: keep to water and refusal questions, which radar supports
            rows.append({"split": split, "messages": [{"role": "system", "content": SYSTEM},
                                                      {"role": "user", "content": [{"type": "image"}, {"type": "text", "text": q}]},
                                                      {"role": "assistant", "content": a}],
                         "images": [str(png.relative_to(ROOT))],
                         "meta": {"district": key, "bbox": bbox, "sensor": sensor, "scene": scene.id, "date": scene.date,
                                  "kind": kind, "labels": "ESA WorldCover 2021 v200 (CC BY 4.0)", "shares": shares}})
    return rows


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--districts", type=int, default=40)
    ap.add_argument("--chips", type=int, default=3, help="chips per district")
    ap.add_argument("--sar", action="store_true", help="also write a Sentinel-1 false-colour image per chip")
    ap.add_argument("--osm", action="store_true", help="add positive-only OSM named-water questions")
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args()
    from satclip import gazetteer
    from satclip.data.provider import get_provider
    rng = random.Random(args.seed)
    districts = list(gazetteer._data()["by_key"].values())  # noqa: SLF001
    rng.shuffle(districts)
    prov = get_provider()
    OUT.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    done = 0
    for d in districts[: args.districts]:
        for i, pt in enumerate(sample_points(d, args.chips, rng)):
            try:
                rows += build_chip(prov, d, pt, i, args, rng)
            except Exception as exc:  # noqa: BLE001
                print(f"  skip {d['name']} chip {i}: {type(exc).__name__}: {exc}"[:160], flush=True)
        done += 1
        if done % 1 == 0:
            print(f"  {done}/{args.districts} districts, {len(rows)} pairs", flush=True)
    by: dict[str, list[dict]] = {}
    for r in rows:
        by.setdefault(r.pop("split"), []).append(r)
    stats = {}
    for split, rs in by.items():
        with open(OUT / f"{split}.jsonl", "w", encoding="utf-8") as f:
            for r in rs:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        stats[split] = len(rs)
    kinds: dict[str, int] = {}
    for r in rows:
        kinds[r["meta"]["kind"]] = kinds.get(r["meta"]["kind"], 0) + 1
    (OUT / "stats.json").write_text(json.dumps({"pairs": stats, "kinds": kinds, "args": vars(args)}, indent=1))
    print(json.dumps({"pairs": stats, "kinds": kinds}, indent=1))


if __name__ == "__main__":
    main()
