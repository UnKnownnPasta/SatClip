---
id: 036
title: "An unsupervised approach based on the generalized Gaussian model to automatic change detection in multitemporal SAR images"
authors: "Yakoub Bazi, Lorenzo Bruzzone, Farid Melgani"
year: 2005
venue: "IEEE Transactions on Geoscience and Remote Sensing (TGRS), vol. 43, no. 4, pp. 874-887, DOI 10.1109/TGRS.2004.842441"
link: https://doi.org/10.1109/TGRS.2004.842441
code: none
category: change-detection
era: historical
tags: [sar, log-ratio, unsupervised, thresholding, kittler-illingworth, generalized-gaussian, despeckling, ers-2, interpretable]
verified: "2026-10-04 via https://api.crossref.org/works/10.1109/TGRS.2004.842441"
takeaway: "Canonical SAR change recipe (despeckle, log-ratio, automatic threshold from a fitted two-class model); adopt it nearly as-is for Sentinel-1 change with the fitted model doubling as a confidence source"
---

# An unsupervised approach based on the generalized Gaussian model to automatic change detection in multitemporal SAR images

## Problem
Detecting change between two single-channel SAR images is hard because speckle makes pixel values noisy, and picking a change threshold by hand is subjective and not repeatable. Earlier automatic thresholds assumed Gaussian class distributions that fit log-ratio SAR data poorly.

## Approach
A three-step unsupervised pipeline: (1) adaptive iterative despeckling of both images, (2) comparison with the log-ratio operator, which turns multiplicative speckle into additive noise and compresses the dynamic range, and (3) automatic thresholding of the log-ratio image with a modified Kittler-Illingworth minimum-error criterion, in which the changed and unchanged class distributions are modelled with generalized Gaussians (a family that can be more peaked or heavier-tailed than a normal). The paper also picks the number of despeckling iterations automatically by watching how the result behaves, instead of fixing it empirically.

## Data and benchmarks
Experiments use multitemporal ERS-2 SAR image pairs with differing speckle levels. The specific scenes were not confirmed from the sources read (abstract and bibliographic record only).

## Key results
Per the abstract, the unsupervised threshold reaches accuracy comparable to the best manually chosen (supervised trial-and-error) threshold across the test datasets. Exact error counts or kappa values could not be confirmed and are not quoted.

## Limitations
Single polarization, single channel, two dates only. Assumes good co-registration and identical acquisition geometry. The two-class model struggles when the changed area is a tiny fraction of the scene (the histogram mode for change is then barely visible). Treats increases and decreases of backscatter together unless split by sign. Wind-roughened water, wet soil and vegetation growth can all trigger change.

## What it means for SatClip
- This is the reference design for SatClip's SAR log-ratio change instrument: Sentinel-1 GRD, same relative orbit and pass direction, speckle filter, 10*log10 ratio of post over pre, signed so that backscatter drops (flooding) and rises (new structures, flattened crops) are reported separately.
- Fit the two-class (generalized) Gaussian model per scene and use the posterior probability at each pixel as the raw confidence, then calibrate it on labelled flood data (Kuro Siwo, entry 041, and Sen1Floods11, entry 022).
- Abstain when the fit is degenerate (no clear change mode, or changed fraction below a minimum), which is exactly when this method is known to be unreliable.
- Record filter type and iterations, threshold value and fitted parameters in the receipt so a reviewer can re-run the same number.
