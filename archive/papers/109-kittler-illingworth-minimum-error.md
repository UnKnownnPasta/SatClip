---
id: 109
title: "Minimum error thresholding"
authors: "J. Kittler, J. Illingworth"
year: 1986
venue: "Pattern Recognition, 19(1): 41-47"
link: https://doi.org/10.1016/0031-3203(86)90030-0
code: "none found (scikit-image does not ship it; short NumPy implementations are common)"
category: historical
era: historical
tags: [thresholding, kittler-illingworth, minimum-error, gaussian-mixture, sar-water, flood-mapping]
verified: "2026-10-06 via https://api.crossref.org/works/10.1016/0031-3203(86)90030-0 (title, authors, venue, volume, issue, pages, year); method summary from standard knowledge of the paper, full text not fetched"
takeaway: "The core of SatClip's SAR water instrument: fit two Gaussians to the gamma0 dB histogram and pick the Bayes minimum error threshold, with the criterion value doubling as a quality check"
---

# Kittler-Illingworth minimum error thresholding

## Problem
Histogram thresholds chosen by heuristics or by between-class variance (Otsu) are poor when the two classes have very different sizes or spreads. The authors sought a threshold that directly minimizes classification error.

## Approach
- Model the histogram as a mixture of two normal distributions (object and background).
- For each candidate threshold, estimate each class's prior, mean and variance from the histogram on either side.
- Evaluate a criterion function equal (up to constants) to the average classification error of that fitted model, and choose the threshold minimizing it.
- An iterative variant refines the threshold quickly; the criterion's minimum also indicates how well the two-Gaussian model fits.

## Data and benchmarks
Demonstrated on synthetic and real gray-level image histograms; no large benchmark or remote sensing set.

## Key results
- Handles unequal class sizes and unequal variances better than variance-based criteria.
- Provides a principled, unsupervised threshold with an associated goodness of fit.

## Limitations
- Assumes two Gaussian classes; SAR backscatter in linear units is gamma-distributed, so the method works best on dB values where distributions are closer to normal.
- The criterion can have multiple local minima or edge minima when a class is nearly absent, giving spurious thresholds.
- Global per-histogram; spatial context and speckle are ignored.

## What it means for SatClip
- This is the SAR water instrument: apply it to Sentinel-1 VV (and optionally VH) gamma0 in dB, on tiles selected for bimodality (split-based selection, see entries 084 and 086), then pool.
- Reject thresholds that hit the histogram edge or fall outside a plausible water band (for example roughly -25 to -15 dB for VV), and feed criterion value, fitted means and variances into the calibrated confidence.
- Log the threshold, fitted parameters and tile IDs in the receipt so any answer is re-runnable.
- If too few tiles are bimodal, abstain rather than force a district-wide threshold.
