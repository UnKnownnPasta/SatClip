---
id: 049
title: "OGC Cloud Optimized GeoTIFF Standard"
authors: "Joan Maso (editor), Open Geospatial Consortium"
year: 2023
venue: "OGC Implementation Standard 21-026, version 1.0 (approved 8 May 2023, published 14 July 2023)"
link: https://docs.ogc.org/is/21-026/21-026.html
code: none
category: data-infrastructure
era: recent
tags: [cog, geotiff, ogc-standard, http-range-requests, tiling, overviews, cloud-native, windowed-reads]
verified: "2026-10-04 via https://docs.ogc.org/is/21-026/21-026.html"
takeaway: "COG 1.0 formalises tiled GeoTIFFs with overviews and headers up front, served over HTTP range requests; this is what lets SatClip read only the district window from a Sentinel scene on a CPU worker"
---

# OGC Cloud Optimized GeoTIFF Standard (21-026)

## Problem
Satellite scenes are large files. Downloading whole scenes to answer a question about one district wastes bandwidth and time. The community "COG" convention solved this informally; OGC turned it into a formal standard so servers and clients can rely on it.

## Approach
The standard defines conformance classes for encoders and servers:
- GeoTIFF Tiles: TIFF 6.0 or BigTIFF with data stored in rectangular tiles (tile sizes multiples of 16), compression recommended.
- GeoTIFF Overviews: reduced-resolution versions stored as additional image file directories, the last overview fitting in one tile.
- GeoTIFF Keys: georeferencing on the full-resolution image, inherited by overviews.
- Optimized GeoTIFF: square tiles, power-of-two sizes strongly recommended, tile size not larger than a typical viewport (512 or 1024 recommended), and a recommended file layout with all headers and overview directories before the tile data, so one request fetches the whole header.
- HTTP Range: servers must honour byte-range requests, advertise them, and enable CORS for the range header on HTTPS.
A media type with a cloud-optimized profile is also defined.

## Data and benchmarks
Not applicable: a standard.

## Key results
A formal, testable definition of COG, so a client can check conformance instead of assuming it.

## Limitations
- Does not cover multi-dimensional time series (that is the domain of Zarr and similar formats); one COG is one image.
- Performance still depends on provider choices (tile size, compression, overviews) and on server latency; badly laid out files remain readable but slow.
- Sentinel-2 L1C/L2A in the original SAFE format are JPEG2000, not COG; COG access depends on catalogues that re-host them as COG (for example Element 84 Earth Search or Planetary Computer).

## What it means for SatClip
- Adopt windowed reads as the only read path: GDAL or rasterio with /vsicurl/ (or signed HTTPS from the catalogue) reading only the tiles intersecting the query AOI, at the overview level matched to the requested scale.
- Pick catalogues whose Sentinel-1 and Sentinel-2 assets are true COGs, and test on startup that the header arrives in one range request and that Accept-Ranges is present.
- Use overviews for fast previews on the card and full resolution only for the measurement, and record both the asset href and pixel window in the receipt.
- Write SatClip output masks as COGs with the recommended layout so they stream into map viewers and can be re-read by anyone checking a card.
</content>
</invoke>
