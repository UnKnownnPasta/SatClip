---
id: 084
title: "Towards operational near real-time flood detection using a split-based automatic thresholding procedure on high resolution TerraSAR-X data"
authors: "Sandro Martinis, André Twele, Stefan Voigt"
year: 2009
venue: "Natural Hazards and Earth System Sciences 9(2), pp. 303-314"
link: https://doi.org/10.5194/nhess-9-303-2009
code: none found
category: sar-optical-fusion
era: historical
tags: [flood-mapping, split-based-thresholding, terrasar-x, kittler-illingworth, coefficient-of-variation, segmentation, dem-refinement, open-access]
verified: "2026-10-05 via https://nhess.copernicus.org/articles/9/303/2009/ (abstract page) and https://nhess.copernicus.org/articles/9/303/2009/nhess-9-303-2009.pdf (open-access full text)"
takeaway: "Origin of tile-wise SAR flood thresholding: only threshold tiles whose variability and darkness indicate both water and land, then pool their histograms"
---

# Towards operational near real-time flood detection using a split-based automatic thresholding procedure on high resolution TerraSAR-X data

## Problem
A single global histogram threshold fails on large SAR scenes because the water class is a small fraction of pixels, so its mode vanishes in the histogram. Manually picking training areas is too slow for disaster response.

## Approach
Split the scene into non-overlapping square sub-images of user-chosen size, select only those likely to contain both water and non-water, compute thresholds there, and derive one global threshold. The thresholded result seeds a multi-scale object-based segmentation, with optional DEM refinement.

Split selection (from the full text, River Severn case):
- Sub-image size s = 500 px, giving 1,187 splits from a 14,461 x 20,153 px scene.
- Coefficient of variation of a split at least 0.7 (signals mixed classes).
- Ratio of split mean to scene mean between 0.4 and 0.9 (darker than average, but not uniformly dark), which avoids mixed farmland and urban tiles.
- 7 splits passed; the 5 closest to the ideal in CV-ratio space were used.

Thresholding: Kittler-Illingworth minimum error (two Gaussian classes), a valley-seeking global minimum method, and a quality index method were compared. Split thresholds were combined either by averaging or by merging split histograms before thresholding; merging was preferred.

Refinement: three segmentation scales, then DEM rules that add or remove objects based on their height relative to the core flood (objects more than about 1 m above it excluded).

## Data and benchmarks
TerraSAR-X Stripmap imagery of the July 2007 River Severn flood, south-west England, with a reference map.

## Key results
Final configuration (segmentation plus DEM) reached 95.44% overall accuracy, 82.01% producer's accuracy and 98.65% user's accuracy for water. The thresholds were expressed in the scene's own gray-value units, not dB, so they do not transfer directly.

## Limitations
- One event, one sensor (X-band, 3 m class); C-band Sentinel-1 statistics differ.
- Split size and CV/ratio bounds were set by the authors for this scene.
- Producer's accuracy of 82% shows that missed water (flooded vegetation, wind, shadow confusion) remains.

## What it means for SatClip
- This is the reason SatClip's sar_water_otsu should not threshold a whole district at once: in a district where 3% is flooded, Otsu sees a unimodal histogram.
- Adopt tile pre-selection by CV and mean ratio as a cheap bimodality proxy alongside the Ashman D test from [[086-chini-hsba-thresholding]].
- Pool the histograms of selected tiles before thresholding instead of averaging per-tile thresholds; it was the more stable option here.
- Record in the evidence card how many tiles were used and the threshold value, so a reviewer can see when the estimate rests on very few tiles.
