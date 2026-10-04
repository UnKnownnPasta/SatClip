---
id: 047
title: "Google Earth Engine: Planetary-scale geospatial analysis for everyone"
authors: "Noel Gorelick, Matt Hancher, Mike Dixon, Simon Ilyushchenko, David Thau, Rebecca Moore"
year: 2017
venue: "Remote Sensing of Environment, 202, 18-27, DOI 10.1016/j.rse.2017.06.031"
link: https://doi.org/10.1016/j.rse.2017.06.031
code: none
category: data-infrastructure
era: historical
tags: [google-earth-engine, cloud-platform, data-catalog, lazy-evaluation, tiling, javascript-api, python-api, planetary-scale]
verified: "2026-10-04 via https://research.google/pubs/google-earth-engine-planetary-scale-geospatial-analysis-for-everyone/"
takeaway: "The reference cloud EO platform: a hosted multi-sensor catalogue with lazy, tile-parallel evaluation; most Indian SAR flood papers run on it, but it is closed and code-centric, so SatClip should match its ergonomics on open STAC plus COG"
---

# Google Earth Engine (Gorelick et al., 2017)

## Problem
Analysing decades of satellite imagery at national or global scale used to demand remote sensing expertise, bulk downloads and supercomputer access. Many groups working on deforestation, drought, disasters, food security and water lacked that capacity.

## Approach
Earth Engine is a cloud platform from Google that combines a curated public catalogue of satellite and geospatial data with a parallel computation engine. Users write scripts (JavaScript code editor or Python client) that build a graph of operations; the server evaluates it lazily, only for the pixels and scale actually requested, and splits work into tiles processed in parallel across Google's infrastructure. Interactive map previews and batch exports share the same code.

## Data and benchmarks
The paper describes the hosted catalogue (Landsat, Sentinel, MODIS, climate and terrain layers among others) and illustrates the system with large applications. We did not re-check specific figures from the full text (catalogue size, performance numbers) because the publisher page was not readable; none are quoted here.

## Key results
A platform that made planetary-scale analyses routine and became the default tool in many remote sensing papers, including several Indian Sentinel-1 flood and crop studies in this archive (entries 042, 043, 044).

## Limitations
- Proprietary service with terms of use; results depend on Google's preprocessing of collections (for example its Sentinel-1 GRD processing) which users cannot fully inspect or change.
- Requires writing code, so it does not serve non-GIS users directly.
- Reproducibility depends on the catalogue staying unchanged, and asset versions are not always pinned in published scripts.
- Quotas and licensing questions for commercial or government use.

## What it means for SatClip
- Adopt its core execution ideas on an open stack: lazy evaluation over only the requested window and scale, and tile-wise parallel jobs on CPU workers, using STAC search (entry 050) and COG range reads (entry 049).
- Avoid a hard dependency on GEE for the production path: our receipts must point to public STAC items and open code that anyone can re-run without an account.
- Use GEE as a cross-check during development: re-implement the Kerala 2018 Otsu workflow (entry 042) and compare our flood area with a GEE run on the same dates to catch preprocessing differences (calibration, terrain flattening, speckle filtering).
- Beat it on accessibility: the user asks in plain language and gets the evidence card, instead of writing a script.
</content>
</invoke>
