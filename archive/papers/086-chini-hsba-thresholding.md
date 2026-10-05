---
id: 086
title: "A hierarchical split-based approach for parametric thresholding of SAR images: Flood inundation as a test case"
authors: "Marco Chini, Renaud Hostache, Laura Giustarini, Patrick Matgen"
year: 2017
venue: "IEEE Transactions on Geoscience and Remote Sensing (2017; listed as early access, pp. 1-14, on the LIST record; final volume and issue not confirmed)"
link: https://doi.org/10.1109/TGRS.2017.2737664
code: none found
category: sar-optical-fusion
era: historical
tags: [flood-mapping, bimodality, ashman-d, hierarchical-tiling, gaussian-fitting, region-growing, change-detection, envisat, terrasar-x]
verified: "2026-10-05 via https://www.list.lu/en/environment/scientific-publications/scientific-publications-detail/a-hierarchical-split-based-approach-for-parametric-thresholding-of-sar-images-flood-inundation-as-a (record and abstract) and https://eo4society.esa.int/wp-content/uploads/2023/11/HAZARD_Floods_Exercises_Chini.pdf (ESA training slides by the first author); final volume and issue not confirmed; full paper paywalled"
takeaway: "Use Ashman D > 2 plus a 10% minority-class rule as SatClip's explicit bimodality check, searching tiles of variable size rather than a fixed grid"
---

# A hierarchical split-based approach for parametric thresholding of SAR images: Flood inundation as a test case

## Problem
Parametric thresholding (fit two distributions, take their intersection) needs a histogram where both classes are well represented. When floods cover a small part of a scene, image-wide fits fail, and fixed-size tiles may be too large or too small for the local flood pattern.

## Approach
HSBA (hierarchical split-based approach) recursively splits the image into tiles of decreasing size and keeps tiles whose histogram shows a usable two-class mix. Per the first author's ESA training material:
- Bimodality test: Ashman's D coefficient must exceed 2.
- The smaller class must make up at least 10% of the tile.
- For change images, the change class must have a positive mean.
- Class distributions are assumed Gaussian and fitted with Levenberg-Marquardt; the threshold is where the fitted water and non-water curves cross.
- Region growing then extends the seed classification over the whole scene, on the assumption that flood pixels cluster spatially, and it can be combined with change detection against a pre-flood image.

Minimum tile size and exact recursion rules were not visible in the sources I could read.

## Data and benchmarks
2007 River Severn (UK) flood with ENVISAT ASAR Wide Swath (moderate resolution) and TerraSAR-X (high resolution).

## Key results
The abstract states that results match benchmarks that relied on manual tile selection, so the method automates parameter estimation without losing accuracy. Numerical accuracies were not in the fetched pages.

## Limitations
- Gaussian class assumption is crude for SAR intensity (log transform helps).
- One flood event tested in the paper; transfer is asserted, not shown, in the abstract.
- Like all backscatter thresholds, misses flooded vegetation and urban water.

## What it means for SatClip
- Make the bimodality check in sar_water_otsu concrete: compute Ashman's D = sqrt(2) |mu1 - mu2| / sqrt(sigma1^2 + sigma2^2) on the two Otsu classes of the dB histogram, require D > 2 and minority fraction >= 10%, else do not trust the threshold.
- Search tiles hierarchically (district, then halves, quarters, and so on) and stop at the first level where enough tiles pass, instead of one fixed tile size.
- Output D and the minority fraction in the evidence card; they are natural inputs to the calibrated confidence and the abstain rule.
- Pair with SAR log-ratio change (already archived via Bazi 2005) for the change-detection variant: apply the same D > 2 test to the log-ratio histogram.
