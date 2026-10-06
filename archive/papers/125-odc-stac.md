---
id: 125
title: "odc-stac: Load STAC items into xarray Datasets (Open Data Cube)"
authors: "Open Data Cube project contributors"
year: 2021
venue: "Open-source Python library, PyPI odc-stac (first release Aug 2021; v0.5.3 current on 2026-10-06), documentation at odc-stac.readthedocs.io"
link: https://odc-stac.readthedocs.io/en/latest/
code: https://github.com/opendatacube/odc-stac
category: data-infrastructure
era: recent
tags: [odc-stac, open-data-cube, xarray, dask, stac, cog, windowed-read, datacube]
verified: "2026-10-06 via https://raw.githubusercontent.com/opendatacube/odc-stac/develop/README.rst, https://odc-stac.readthedocs.io/en/latest/_api/odc.stac.load.html (parameters: bbox, geopolygon, crs, resolution, groupby incl. solar_day, chunks, fail_on_error, pool, patch_url, fuse_func) and https://pypi.org/pypi/odc-stac/json (version 0.5.3, first upload 2021-08-26); GitHub API metadata (licence, stars) was not reachable from this session; no peer-reviewed paper found"
takeaway: "odc-stac turns a STAC search result into a district-clipped, grid-aligned xarray cube with windowed COG reads, which is close to exactly SatClip's data layer, so SatClip should reuse it (with patch_url for signing and fail_on_error off) rather than hand-roll reprojection and mosaicking"
---

# odc-stac

## Problem
After a STAC search, users still have to open many COGs, reproject them to a common grid, mosaic overlapping scenes from the same pass, and stack dates. Doing this by hand is error prone, and reading whole scenes wastes bandwidth when only a district is needed.

## Approach
- A single function, odc.stac.load, takes pystac items (from any catalogue) and returns an xarray Dataset with dimensions time, y, x and one variable per band.
- The output grid is set by crs plus resolution, an exact GeoBox, or like= an earlier result; extent is limited by bbox, lon/lat, x/y or a geopolygon such as a district boundary. Pixels snap to a regular grid.
- groupby controls what becomes one time slice ("time", "solar_day", "id", any property, or a custom key); fuse_func controls how overlapping items are combined.
- Loads eagerly with a thread pool, or lazily as Dask arrays via chunks; patch_url can rewrite every asset URL (for example to sign it); fail_on_error=False skips unreadable assets.
- Builds on the earlier Open Data Cube (see archive entry on the Australian Geoscience Data Cube) without needing its database.

## Data and benchmarks
A software library; no benchmark paper. It is used in Digital Earth Australia and Digital Earth Africa notebooks and in Planetary Computer examples (not re-verified here).

## Key results
Reduces the "STAC search to analysis cube" step to a few lines while reading only the windows of each COG that intersect the requested area, at the requested resolution.

## Limitations
- Silent skipping with fail_on_error=False can hide missing data unless the caller counts what was skipped.
- Default fusing keeps the first valid pixel; for SAR mosaics across adjacent slices this is usually fine, but for multi-orbit stacks it can mix geometries.
- Grid snapping can extend output slightly beyond the requested bounds, so area statistics must apply the exact district mask afterwards.

## What it means for SatClip
- Adopt odc.stac.load as the reader behind each tile worker: geopolygon = tile footprint intersected with the district, crs = local UTM, resolution = 10 m, groupby = "solar_day" so adjacent Sentinel-1 slices from one pass become one image.
- Use patch_url for Planetary Computer signing so the same code path works across all three catalogues.
- Set fail_on_error=False only together with explicit valid-pixel counting per tile; feed the valid fraction into the evidence card's confidence and abstain when coverage of the district is too low.
- Pin a fixed grid (anchor and resolution) so per-cell cache keys are stable across runs, which also makes the re-runnable receipt reproduce pixel for pixel.
- Record the odc-stac version in the receipt, since loader defaults affect results.
