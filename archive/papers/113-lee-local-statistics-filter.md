---
id: 113
title: "Digital Image Enhancement and Noise Filtering by Use of Local Statistics"
authors: "Jong-Sen Lee"
year: 1980
venue: "IEEE Transactions on Pattern Analysis and Machine Intelligence, PAMI-2(2): 165-168"
link: https://doi.org/10.1109/TPAMI.1980.4766994
code: "none found (Lee filter available in SNAP and many Python packages)"
category: historical
era: historical
tags: [speckle, lee-filter, adaptive-filter, sar, local-statistics, denoising]
verified: "2026-10-06 via https://api.crossref.org/works/10.1109/TPAMI.1980.4766994 (title, author, venue, volume, issue, pages, year); method summary from standard knowledge of the paper, full text not fetched"
takeaway: "The Lee filter is the cheap, explainable speckle reducer SatClip should apply to gamma0 before thresholding, with window size logged in the receipt"
---

# Lee local statistics filter

## Problem
Images corrupted by additive or multiplicative noise (such as radar speckle) need smoothing that removes noise without blurring edges, at low computational cost.

## Approach
- Estimate local mean and local variance in a moving window.
- Form a linear minimum mean square error estimate: output equals local mean plus a gain times (pixel minus local mean), where the gain shrinks toward zero in homogeneous areas and toward one where local variance exceeds the noise variance (edges, texture).
- Variants handle additive, multiplicative and combined noise models; the same local statistics also support contrast enhancement.

## Data and benchmarks
Demonstrated on example images with synthetic and real noise, including radar-like speckle; no standard benchmark.

## Key results
- Simple, non-iterative, adaptive smoothing that preserves edges better than mean or median filters.
- Became the basis for widely used SAR speckle filters (Lee, enhanced Lee, refined Lee).

## Limitations
- Needs an estimate of noise level (equivalent number of looks for SAR).
- Square windows still blur thin features such as narrow channels and embankments; refined Lee was introduced later for this.
- Leaves residual speckle in bright point targets and urban areas.

## What it means for SatClip
- Apply a Lee or refined Lee filter (for example 5x5 or 7x7) to Sentinel-1 gamma0 in linear power before converting to dB and running Kittler-Illingworth; this tightens the water mode and stabilizes thresholds.
- Record filter type and window in the receipt so results are reproducible and comparable across runs.
- Test sensitivity: if water area changes a lot between unfiltered and filtered input, reduce confidence on the card.
- Avoid heavy filtering for small water bodies near the pixel scale; report minimum mappable size.
