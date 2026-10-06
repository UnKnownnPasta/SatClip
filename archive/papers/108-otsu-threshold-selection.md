---
id: 108
title: "A Threshold Selection Method from Gray-Level Histograms"
authors: "Nobuyuki Otsu"
year: 1979
venue: "IEEE Transactions on Systems, Man, and Cybernetics, 9(1): 62-66"
link: https://doi.org/10.1109/TSMC.1979.4310076
code: "none found (implemented in scikit-image threshold_otsu and OpenCV THRESH_OTSU)"
category: historical
era: historical
tags: [thresholding, histogram, otsu, unsupervised, binarization, water-mapping-baseline]
verified: "2026-10-06 via https://api.crossref.org/works/10.1109/TSMC.1979.4310076 (title, author, venue, volume, issue, pages, year); method summary from standard knowledge of the paper, full text not fetched"
takeaway: "The default automatic threshold that SatClip must benchmark Kittler-Illingworth against, and a cheap fallback when the two-Gaussian fit fails"
---

# Otsu thresholding

## Problem
Picking a gray-level threshold that separates object from background usually needed manual tuning or assumptions about histogram shape. Otsu wanted a nonparametric, unsupervised rule computed only from the image histogram.

## Approach
- Treat every candidate threshold as splitting the histogram into two classes.
- Choose the threshold that maximizes the between-class variance (equivalently minimizes within-class variance), using only zeroth and first order cumulative moments.
- A single pass over the histogram suffices, and the method extends to multiple thresholds.
- The maximum of the separability measure gives a by-product score of how bimodal the histogram is.

## Data and benchmarks
The paper illustrates the method on a small set of gray-level images and their histograms rather than on a benchmark; no remote sensing data are involved.

## Key results
- Stable, fast, parameter-free threshold selection that became the de facto default in image processing.
- The separability score indicates when a threshold is meaningful at all.

## Limitations
- Biased toward splitting classes of similar size and variance; when water is a small fraction of a tile, the threshold drifts into the land mode.
- Assumes a bimodal histogram; returns a number even on unimodal tiles, which can fabricate water.
- No explicit noise model, so it ignores SAR speckle statistics.

## What it means for SatClip
- Implement Otsu alongside Kittler-Illingworth on gamma0 dB tiles and record both thresholds in the evidence card receipt; large disagreement is a signal to lower confidence.
- Use Otsu's separability score (or a bimodality test) as a gate: if a tile is not bimodal, do not threshold it, and let the split-based tile selection skip it.
- Never apply Otsu to a whole district histogram where water is a few percent of pixels; that is exactly the small-class failure case.
