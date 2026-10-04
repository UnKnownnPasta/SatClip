---
id: 048
title: "The Australian Geoscience Data Cube - Foundations and lessons learned"
authors: "Adam Lewis, Simon Oliver, Leo Lymburner, Ben Evans, Lesley Wyborn, Norman Mueller, Gregory Raevksi, Jeremy Hooke, Rob Woodcock, Joshua Sixsmith, Wenjun Wu, Peter Tan, Fuqin Li, Brian Killough, Stuart Minchin, Dale Roberts, Damien Ayers, Biswajit Bala, John Dwyer, Arnold Dekker, Trevor Dhu, Andrew Hicks, Alex Ip, Matt Purss, Clare Richards, Stephen Sagar, Claire Trenham, Peter Wang, Lan-Wei Wang"
year: 2017
venue: "Remote Sensing of Environment, 202, 276-292, DOI 10.1016/j.rse.2017.03.015"
link: https://doi.org/10.1016/j.rse.2017.03.015
code: https://github.com/opendatacube/datacube-core
category: data-infrastructure
era: historical
tags: [open-data-cube, analysis-ready-data, provenance, surface-reflectance, time-series, landsat, ceos, apache-2, hpc]
verified: "2026-10-04 via https://openresearch-repository.anu.edu.au/items/a1274cca-c22d-4a4f-8b51-726487d18bc3/full"
takeaway: "Open Data Cube foundations: analysis-ready, provenance-tracked data plus a light index and open (Apache 2.0) code make time series trustworthy; SatClip should copy the provenance discipline, not the heavy ingest"
---

# The Australian Geoscience Data Cube (Lewis et al., 2017)

## Problem
Earth observation archives have Big Data problems of volume, velocity and variety. Analysts spent most of their effort preparing and aligning scenes instead of extracting information from the full time series, and results were hard to trace back to inputs.

## Approach
Version 2 of the AGDC (which became the Open Data Cube) rests on three foundations: (1) data preparation, with geometric and radiometric correction to consistent surface reflectance suitable for time-series analysis, plus collection management that records provenance; (2) software to index, manage and access the data through a minimal relational model with a "not-only-SQL" style index; (3) high performance computing at Australia's National Computational Infrastructure. Code is released under Apache License 2.0.

## Data and benchmarks
Built around the Landsat archive over Australia, processed into surface reflectance products for continental time-series analysis. We did not confirm specific volume or speed figures from the full text, so none are quoted.

## Key results
Showed that national-scale time-series analysis becomes practical once data are analysis ready and indexed with provenance. The open code was taken up internationally, including through CEOS efforts to support developing countries.

## Limitations
- Designed around ingesting and indexing large holdings on HPC; heavy to run for a small team.
- Predates the cloud-native STAC plus COG pattern; later ODC versions added STAC indexing, but the paper itself reflects the HPC era.
- Analysis-ready preparation is mostly optical (Landsat) in this paper; SAR ARD is not its focus.

## What it means for SatClip
- Adopt the provenance principle: every measurement on a card should carry its input scene IDs, processing level, software version and parameters, as the AGDC collection management does.
- Avoid copying the full ingest-and-index model for the prototype; we read COG windows on demand from public STAC catalogues instead of building our own national cube.
- Prefer analysis-ready inputs where catalogues offer them (Sentinel-2 L2A surface reflectance, radiometrically terrain-corrected Sentinel-1 where available) and say on the card which ARD level was used.
- If SatClip later needs fast repeated district time series, the Open Data Cube (with STAC indexing) is the open option to evaluate before building our own cache.
</content>
</invoke>
