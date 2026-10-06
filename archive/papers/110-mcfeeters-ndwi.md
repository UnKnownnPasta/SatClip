---
id: 110
title: "The use of the Normalized Difference Water Index (NDWI) in the delineation of open water features"
authors: "S. K. McFeeters"
year: 1996
venue: "International Journal of Remote Sensing, 17(7): 1425-1432"
link: https://doi.org/10.1080/01431169608948714
code: "none found (formula only)"
category: historical
era: historical
tags: [ndwi, spectral-index, optical-water, green-nir, open-water, sentinel-2]
verified: "2026-10-06 via https://api.crossref.org/works/10.1080/01431169608948714 (title, author, venue, volume, issue, pages, year); method summary from standard knowledge of the paper, full text not fetched"
takeaway: "Gives SatClip its optical water instrument, (Green minus NIR) over (Green plus NIR) on Sentinel-2 B3 and B8, used only on cloud-free, shadow-masked pixels as a cross-check on SAR"
---

# McFeeters NDWI

## Problem
Open water needed to be delineated from multispectral imagery in a simple, repeatable way, analogous to how NDVI highlights vegetation.

## Approach
- Define NDWI as the normalized difference of green and near-infrared reflectance: (Green minus NIR) / (Green plus NIR).
- Water reflects more green than NIR, so it gets positive values; vegetation and soil mostly get zero or negative values.
- A threshold near zero separates open water from land.

## Data and benchmarks
Demonstrated on Landsat-type multispectral imagery over a study area with open water bodies; it is a methods note rather than a benchmarked comparison. Exact scenes not confirmed here.

## Key results
- A single, sensor-agnostic index that makes open water stand out and suppresses vegetation and soil.
- Became the standard optical water index and the template for later variants.

## Limitations
- Built-up surfaces can also give positive values, causing urban false water; Xu (2006) MNDWI swaps NIR for SWIR to reduce this.
- Turbid or vegetated floodwater and mixed pixels are often missed.
- Clouds, cloud shadows and terrain shadows corrupt it; useless under monsoon overcast.

## What it means for SatClip
- Implement NDWI on Sentinel-2 L2A (B3, B8) as the optical water instrument, but only on pixels passing the SCL cloud, shadow and snow mask; report the valid-pixel fraction on the card and abstain when it is low.
- Prefer a data-driven threshold (Otsu or K-I on the NDWI histogram) over a fixed zero, and record it in the receipt.
- Use NDWI mainly to cross-validate SAR water on clear dates (pre-monsoon baselines, post-event clear days) and to calibrate SAR confidence, not as the monsoon primary.
- Consider MNDWI (B11 SWIR) in urban districts to avoid built-up false positives.
