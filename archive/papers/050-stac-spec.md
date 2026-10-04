---
id: 050
title: "SpatioTemporal Asset Catalog (STAC) Specification"
authors: "STAC community, Radiant Earth Foundation (stac-spec contributors)"
year: 2024
venue: "Standard specification (v1.1.0, released 11 September 2024; v1.0.0 released 25 May 2021)"
link: https://stacspec.org/en
code: https://github.com/radiantearth/stac-spec
category: data-infrastructure
era: recent
tags: [stac, metadata, catalog, search-api, geojson, cloud-native, interoperability, sentinel, planetary-computer, copernicus]
verified: "2026-10-04 via https://github.com/radiantearth/stac-spec/releases"
takeaway: "STAC is the common search language of public EO catalogues (Item, Catalog, Collection, API); SatClip should search with STAC API and record STAC Item IDs and hrefs in every receipt"
---

# SpatioTemporal Asset Catalog (STAC) Specification

## Problem
Every satellite data provider used to expose its archive through its own search interface and metadata format, so tools had to be rewritten for each catalogue and results were hard to reproduce or share.

## Approach
STAC is a small, extensible JSON specification. It has four parts: the Item (a GeoJSON Feature describing one spatiotemporal asset, with geometry, datetime, properties and links to asset files), the Catalog (links that organise Items for browsing), the Collection (a Catalog with extra metadata such as spatial and temporal extent, licence, keywords and providers), and the STAC API (a RESTful search interface built on OGC API - Features, so clients can query by bounding box, time and properties). Extensions add domain fields such as electro-optical bands, SAR, projection, view geometry and processing.

## Data and benchmarks
Not applicable: a specification. Stable v1.0.0 was released on 25 May 2021 after several betas and release candidates; v1.1.0 on 11 September 2024 unified band descriptions and expanded common metadata.

## Key results
Widely used across major open catalogues; Microsoft Planetary Computer and Element 84 Earth Search expose Sentinel-1 and Sentinel-2 via STAC API, and the Copernicus Data Space Ecosystem offers a STAC endpoint. (We did not re-verify each provider's current STAC version here.)

## Limitations
- Catalogues differ in which extensions and property names they fill (for example cloud cover, orbit direction, relative orbit), so a query that works on one may need mapping on another.
- STAC describes and locates data; it does not guarantee assets are COGs or analysis-ready.
- Spec evolution (1.0 to 1.1) means clients should tolerate both band conventions.

## What it means for SatClip
- Adopt STAC API as the only search path in the data layer: query by AOI geometry, date window and filters (eo:cloud_cover for Sentinel-2, sat:orbit_state and sat:relative_orbit for Sentinel-1), then read assets as COG windows (entry 049).
- Put the STAC Item ID, collection ID, catalogue URL and asset href into every receipt, so anyone can fetch the same scenes; this is the core of our re-runnable promise.
- Write a thin provider adapter for property name differences between Planetary Computer, Earth Search and Copernicus Data Space, and fall back between them when one is down or lacks a date.
- Publish SatClip's own outputs (masks, measurements) as STAC Items with the processing extension, so a card can be loaded into QGIS or any STAC browser.
</content>
</invoke>
