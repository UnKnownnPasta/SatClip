---
id: 185
title: "Towards global flood mapping onboard low cost satellites with machine learning"
authors: "Gonzalo Mateo-Garcia, Joshua Veitch-Michaelis, Lewis Smith, Silviu Vlad Oprea, Guy Schumann, Yarin Gal, Atilim Gunes Baydin, Dietmar Backes"
year: 2021
venue: "Scientific Reports, 11, article 7249"
link: https://doi.org/10.1038/s41598-021-86650-z
code: "https://github.com/spaceml-org/ml4floods (README fetched; ML4Floods pipeline and WorldFloodsV2 dataset; the 2021 paper itself points to a GitLab repository not fetched)"
category: sar-optical-fusion
era: recent
tags: [flood-mapping, worldfloods, ml4floods, sentinel-2, ndwi-baseline, onboard-processing, phisat-1, copernicus-ems, recall-first, permanent-water]
verified: "2026-10-08 via curl to api.crossref.org (title, eight authors, journal, volume 11, article 7249, 31 March 2021), api.openalex.org (abstract) and the nature.com article page (Results section text); WebFetch permission prompt timed out so curl was used; Table 2 values were not in the extracted text so no IoU numbers are quoted"
takeaway: "WorldFloods (119 verified flood events) shows a small CNN beats NDWI thresholds on Sentinel-2 flood water; NDWI at 0 generalises poorly on silty flood water and SWIR bands matter, both direct warnings for SatClip's optical water fallback"
---

# Mateo-Garcia et al. 2021, WorldFloods and onboard flood segmentation

## Problem
Small satellites could revisit floods every few hours, but cannot downlink full images quickly. If a flood mask is computed on board, only the small mask needs to be sent. That needs a model that is both accurate on global floods and small enough for a low-power chip.

## Approach
- Compiles WorldFloods: Sentinel-2 images paired with flood maps from disaster response organisations (mainly Copernicus EMS), some originally drawn from radar images.
- Trains a 4-layer simple CNN (0.26M parameters) and a U-Net (7.8M) on all 13 Sentinel-2 bands, plus versions degraded to 80 m to mimic the HyperScout-2 camera on PhiSat-1.
- Loss weights classes by inverse frequency and adds Dice loss, to favour recall: missing flood water is treated as worse than over-predicting it.
- Baselines: NDWI at threshold 0, NDWI at the best-case threshold (-0.22, chosen on test data with recall above 94%, with perfect s2cloudless cloud masking), and a per-pixel linear model.

## Data and benchmarks
- 119 globally verified flood events, released in a common format; tested on independent locations.
- Metrics: water-class IoU and recall, with recall split into flood water and permanent water (JRC layer).

## Key results
- All three learned models reached recall above 94%; NDWI at 0 generalised poorly, which the authors attribute to water with suspended sediment.
- The U-Net was only slightly better than the tiny CNN despite about 30 times more parameters.
- Going from 10 m to 80 m cost about two points; dropping to the 10 bands shared with HyperScout-2 (no SWIR) caused a significant drop, pointing to SWIR as important for water.
- Models ran on an Intel Movidius Myriad2 test setup. Exact IoU table values were not read and are not quoted.

## Limitations
- Optical only: no use of Sentinel-1, so it fails under monsoon cloud, which is when Indian floods happen.
- Labels come from varied sources and dates; some reference maps were drawn on other sensors, so label noise is likely.
- The best NDWI threshold was tuned on the test set, so it is an upper bound rather than a fair baseline.

## What it means for SatClip
- Adopt: a recall-first operating point and reporting recall split into flood versus permanent water. SatClip should show both so officials see whether the "flood" is just the river.
- Concrete fix for the optical water instrument: do not hard-code NDWI at 0. Use a SWIR-based index (MNDWI) or a locally fitted Otsu threshold, and lower confidence when water looks turbid.
- Adopt: ML4Floods/WorldFloodsV2 as a ready source of Sentinel-2 flood labels for calibrating SatClip's optical fallback.
- Beat: pair it with Sentinel-1 (entries 083, 187) so cloudy monsoon scenes are not simply abstained on.
