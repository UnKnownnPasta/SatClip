---
id: 191
title: "Change detection techniques for ERS-1 SAR data"
authors: "Eric J. M. Rignot, Jakob J. van Zyl"
year: 1993
venue: "IEEE Transactions on Geoscience and Remote Sensing, 31(4), 896-906"
link: https://doi.org/10.1109/36.239913
code: "Not applicable"
category: historical
era: historical
tags: [sar, change-detection, ratio, log-ratio, speckle, number-of-looks, decorrelation, coherence, ers-1, foundational]
verified: "2026-10-08 via curl to api.crossref.org (title, two authors, volume 31, issue 4, pages 896-906, July 1993) and api.openalex.org (abstract; open copy listed at escholarship.org/uc/item/02j5r0qf, not fetched); WebFetch permission prompt timed out so curl was used"
takeaway: "The origin of ratioing SAR intensities instead of subtracting them: ratio fits multiplicative speckle and works best with many looks, while speckle decorrelation suits single-look data; the reason SatClip's SAR change instrument is a log-ratio"
---

# Rignot and van Zyl 1993, change detection techniques for ERS-1 SAR

## Problem
Optical change detection often subtracts two images. SAR images carry multiplicative speckle, so the same subtraction gives errors that grow with brightness. Which comparison is statistically right for SAR?

## Approach
- Compares two families of techniques using theory and real ERS-1 C-band data.
- Intensity change: compares the backscatter magnitude between two dates, contrasting differencing with ratioing.
- Decorrelation: estimates how much the speckle pattern itself decorrelates between dates, which flags change in surface structure or dielectric properties even when mean brightness is similar.

## Data and benchmarks
- Spaceborne ERS-1 SAR acquisitions plus theoretical predictions; no modern benchmark.

## Key results
(From the abstract.)
- Ratioing fits SAR statistics better than subtracting, and works best when the number of looks is large.
- Speckle decorrelation works best on one-look complex data, and can use intensity data if the number of looks is small.
- The two approaches are complementary.

## Limitations
- Early, small-scale demonstration; threshold selection is not automated (later solved by Bazi et al., entry 036, and Bruzzone and Prieto, entry 140).
- No accuracy numbers in the abstract.

## What it means for SatClip
- Adopt (already the design): the flood change instrument should keep using the log-ratio of co-registered, same-orbit Sentinel-1 intensities, with multilooking or speckle filtering (entry 113) before ratioing, since the paper ties ratio reliability to many looks.
- Cite this in the instrument card as the reason for ratio over difference.
- The decorrelation idea is the ancestor of the coherence-change approach for urban floods (entry 190), a candidate second change instrument.
