---
id: 111
title: "Red and photographic infrared linear combinations for monitoring vegetation"
authors: "Compton J. Tucker"
year: 1979
venue: "Remote Sensing of Environment, 8(2): 127-150"
link: https://doi.org/10.1016/0034-4257(79)90013-0
code: "none found (formula only)"
category: historical
era: historical
tags: [ndvi, vegetation-index, red-nir, crop-monitoring, spectral-index]
verified: "2026-10-06 via https://api.crossref.org/works/10.1016/0034-4257(79)90013-0 (title, author, venue, volume, issue, pages, year); experimental details summarized from standard knowledge of the paper, full text not fetched"
takeaway: "The foundation of SatClip's NDVI-difference instrument: red and NIR combinations track green biomass, so NDVI change between clear dates is a defensible crop-damage signal"
---

# Tucker 1979, red and NIR vegetation indices

## Problem
Which combinations of red and near-infrared (photographic infrared) measurements best track vegetation amount and condition, and how do they compare with green-red combinations?

## Approach
- Compare several red and NIR combinations, including the simple ratio, the difference and the normalized difference ((NIR minus red) / (NIR plus red)), plus green-red analogues.
- Relate each to field-measured canopy variables such as biomass, chlorophyll and leaf water content.

## Data and benchmarks
Ground-based hand-held radiometer measurements over grassland plots with matched destructive sampling (details recalled from the literature, not re-confirmed from the full text).

## Key results
- Red and NIR combinations were more closely related to vegetation variables than green and red ones.
- The normalized difference and related ratios emerged as robust, simple indicators, establishing NDVI as the standard vegetation index.

## Limitations
- Saturates over dense canopies, which matters for kharif paddy at peak season.
- Sensitive to soil background, atmosphere, viewing geometry and, crucially, cloud and shadow.
- Plot-scale radiometry, not satellite imagery; satellite-scale behavior came later.

## What it means for SatClip
- The NDVI difference instrument (Sentinel-2 B4, B8) rests on this result: compute pre-event minus post-event NDVI on co-masked clear pixels, never across cloud-contaminated pixels.
- State on the evidence card the two scene dates and the phenology gap; a drop could be harvest rather than damage, so restrict comparisons to similar crop stages or flag the ambiguity.
- Account for saturation: small NDVI drops in dense paddy can understate damage, so pair with SAR VH change when available.
- Abstain when the common clear-pixel fraction over the district or crop mask is below threshold.
