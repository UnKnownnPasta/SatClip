---
id: 217
title: "Spatio-Temporal Analysis of Urban Floods in Mumbai, India, Using Sentinel-1 SAR Data"
authors: "Kiran Jalem, Gouranga Pal, Sagar Kumar Swain, K. K. Basheer Ahammed"
year: 2026
venue: "Earth (MDPI), 7(3), article 91 (published 31 May 2026), DOI 10.3390/earth7030091; open access"
link: https://doi.org/10.3390/earth7030091
code: "No code statement; data available on request"
category: indian-context
era: recent
tags: [mumbai, urban-flood, sentinel-1, vv, vh, bimodality, dip-test, kde-threshold, jrc-gsw, ward-level, bmc, chirps, india]
verified: "2026-10-09 via WebSearch (candidate found) and WebFetch of the open-access article at mdpi.com/2673-4834/7/3/91 (title, authors, affiliations, dates, DOI, method, validation, numbers, author-stated limitations). The per-scene acquisition table and the VH table for years other than 2024 were not in the extracted text"
takeaway: "Multi-year (2018 to 2025) Sentinel-1 flood mapping of Mumbai by ward, using tile-wise bimodality testing before thresholding and JRC permanent-water removal, checked against 500+ municipal and crowd-sourced flood points; useful as Indian urban reference points but its accuracy is not quantified"
---

# Jalem et al. 2026, Mumbai urban floods from Sentinel-1

## Problem
Mumbai floods almost every monsoon, but earlier studies looked at single events or short rainfall windows. The authors want a multi-year, ward-level flood record from SAR, linked to municipal infrastructure records and rainfall.

## Approach
- Sentinel-1 IW, VV and VH, sixteen pre-flood and during/post-flood image pairs, processed in SNAP 9.0 (thermal noise removal, Lee Sigma speckle filter, calibration to sigma0 in dB, incidence-angle normalisation).
- Threshold selection by blocks: Hartigan's dip test (dip statistic above 0.05) keeps only bimodal blocks, then kernel density estimation finds the minimum between the two modes as the threshold; morphological filtering cleans the mask.
- Remove permanent water with JRC Global Surface Water seasonality, cross-checked against recent Sentinel-1; a 30 m DEM is used for shadow masking and context.
- No coherence, HAND or explicit change ratio is used; double bounce is discussed only as an explanation.

## Data and benchmarks
- Flood seasons from July 2018 to August 2025 over Greater Mumbai.
- Reference: more than 500 points from the Brihanmumbai Municipal Corporation flood portal, NIUA reports, crowd-sourced flood points and field reports, compared by spatial agreement only.
- CHIRPS daily rainfall for correlation.

## Key results
- VV flood extent: about 93 km2 (2018), 34 km2 (2019), 85 km2 (2020), 72 km2 (2021), 152 km2 (2024, the maximum); VH gave 67 km2 in 2024.
- Mean flooded area per ward rose from about 3.3 km2 (2018) to about 8.9 km2 (2024); Chembur West peaked at 16.47 km2 in 2024.
- Peak daily rainfall correlated with total flooded area (Pearson r = 0.72, p < 0.01).
- Good overlap with BMC hotspot maps in Chembur and Ghatkopar, low overlap in Colaba and Byculla.

## Limitations
- No pixel-level accuracy (no confusion matrix or kappa), only point overlap.
- Internal inconsistencies noted on reading: the rainfall threshold differs between abstract (300 mm/day) and Section 3.4 (250 mm/day); Colaba is called low exposure in the abstract but listed among the highest-inundation wards in Section 3.3; the second most flood-prone ward differs between abstract (Matunga) and results (Dahisar).
- Intensity thresholding in a dense city will miss water between buildings (entries 214, 215); the VV vs VH gap (152 vs 67 km2 in 2024) shows how sensitive the totals are to polarisation.
- Static built-up layers, 30 m DEM, coarse rainfall.

## What it means for SatClip
- Adopt in sar_water_otsu: run a bimodality check (dip test or Ashman's D) on each tile before trusting Otsu, and fall back to "cannot tell" or a neighbouring tile threshold when the histogram is unimodal; this is cheap and directly addresses Otsu failure on mostly dry tiles.
- Adopt: the BMC flood-spot points are a candidate Indian urban check set; request them and use them as point labels.
- Avoid: do not quote city flood area from a single polarisation without showing both; report VV and VH or their agreement.
- Avoid: do not treat these extents as ground truth for calibration; accuracy is unquantified and the urban signal is likely under-detected.
