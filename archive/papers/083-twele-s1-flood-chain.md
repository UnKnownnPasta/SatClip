---
id: 083
title: "Sentinel-1-based flood mapping: a fully automated processing chain"
authors: "André Twele, Wenxi Cao, Simon Plank, Sandro Martinis"
year: 2016
venue: "International Journal of Remote Sensing 37(13), pp. 2990-3004"
link: https://doi.org/10.1080/01431161.2016.1192304
code: none found
category: sar-optical-fusion
era: historical
tags: [flood-mapping, sentinel-1, automatic-thresholding, tile-based, kittler-illingworth, fuzzy-logic, hand, region-growing, near-real-time, vv-vs-vh]
verified: "2026-10-05 via https://elib.dlr.de/102476 (bibliographic record and abstract), https://elib.dlr.de/102505 (companion LPS 2016 paper) and https://extwiki.eodc.eu/GFM/PDD/GFM_algorithms/DLR_algo (operational descendant algorithm description); publisher full text at tandfonline is paywalled and was not read"
takeaway: "Blueprint for sar_water_otsu: pick bimodal, darker-than-average tiles, threshold them, then refine with slope, size and HAND fuzzy rules; VV is slightly better than VH in calm wind"
---

# Sentinel-1-based flood mapping: a fully automated processing chain

## Problem
Flood response needs water extent maps within hours, without an analyst tuning thresholds per scene. Sentinel-1 offers systematic, cloud-independent C-band acquisitions, but a raw scene-wide histogram is rarely bimodal because water covers a small fraction of a large scene.

## Approach
DLR adapted its earlier TerraSAR-X flood service (see [[085-martinis-tsx-flood-service]]) to Sentinel-1. The chain runs with no user intervention: automatic download from the ESA hub, geometric and radiometric pre-processing, automatic computation of auxiliary layers (DEM, slope, a topographic flood-proneness index, reference water), an unsupervised tile-based threshold initialisation, fuzzy-logic refinement, and web delivery for a user-defined area of interest.

The full paper is paywalled. The following parameters come from the Copernicus Global Flood Monitoring (GFM) documentation of the DLR algorithm, which cites Martinis et al. 2015 and Twele et al. 2016 as its basis; they may have been tuned since 2016:
- Two-level quadtree tiling: 200x200 px parent tiles, each split into four 100x100 px children.
- A tile is a candidate if its mean backscatter is below the scene mean and the standard deviation of its four child means exceeds the mean of all such standard deviations plus 2 times their standard deviation (relaxed to 1.28 if fewer than 10 tiles qualify).
- Tiles are rejected if over 50% no-data or over 20% outside flood-prone terrain (HAND mask).
- The 5 tiles with the highest spread are thresholded with Kittler-Illingworth minimum error thresholding; the global threshold is their mean.
- Fallback when the threshold is above -15 dB or fails: a percentile of backscatter over known permanent water, with defaults around -18 dB.
- Fuzzy refinement: Z-shaped membership for backscatter (from water mean to threshold) and slope (0 to 18 degrees), S-shaped for water body size (10 to 500 px); mean membership of at least 0.6 is water.
- Region growing from seeds of at least 30 px with membership 0.35 to 0.6 allowed for growth; tiny blobs removed.

## Data and benchmarks
Two flood scenarios at the Greece-Turkey border, validated against reference data (validation details not read; paywalled).

## Key results
- Overall accuracy 94.0% to 96.1%, Cohen's kappa 0.879 to 0.910 (abstract).
- Flood maps delivered in under 45 minutes after scene availability on the ESA hub.
- VV gave marginally better accuracy than VH under calm wind.

## Limitations
- Only two test events in one region; generalisation to Indian monsoon floods (paddy fields, flooded vegetation, wind-roughened water) is not shown.
- Open-water only: flooded vegetation and urban floods (double bounce brightening) are missed by a low-backscatter rule.
- Exact tile sizes and fuzzy limits in the 2016 paper itself could not be read; the numbers above are from the later operational description.

## What it means for SatClip
- Replace a scene-wide Otsu with a tile-selection step: compute stats on 200x200 px tiles (10 m pixels, so 2 km), keep tiles darker than the AOI mean whose child-mean spread passes the mean + 2 sigma rule, threshold only those, and average.
- Report the number of qualifying tiles in the evidence card; if fewer than about 5 to 10 qualify, lower confidence or abstain rather than silently using a default threshold.
- Sanity-bound the VV threshold: if Otsu returns a value above -15 dB, treat it as a failed split (likely no real water class) and abstain or fall back to a permanent-water percentile, flagged as a fallback.
- Add cheap post-filters before counting flooded area: slope above about 18 degrees and HAND-high terrain suppress water; drop blobs under about 8 to 10 px.
- Default to VV, keep VH as a cross-check; note wind as a known failure mode in the explanation.
