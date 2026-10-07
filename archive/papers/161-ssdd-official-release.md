---
id: 161
title: "SAR Ship Detection Dataset (SSDD): Official Release and Comprehensive Data Analysis"
authors: "Tianwen Zhang, Xiaoling Zhang, Jianwei Li, Xiaowo Xu, Baoyou Wang, Xu Zhan, Yanqin Xu, Xiao Ke, Tianjiao Zeng, Hao Su, Israr Ahmad, Dece Pan, Chang Liu, Yue Zhou, Jun Shi, Shunjun Wei"
year: 2021
venue: "Remote Sensing (MDPI), 13(18), 3690"
link: https://doi.org/10.3390/rs13183690
code: "Not verified (dataset release; download location not fetched)"
category: object-detection
era: recent
tags: [sar, ship-detection, dataset, rotated-boxes, polygon-segmentation, evaluation-protocol, reproducibility, inshore-offshore]
verified: "2026-10-07 via curl to api.crossref.org (title, authors, journal, volume, issue, article number, date) and api.openalex.org (abstract); not on arXiv; source sensors of SSDD images not stated in the abstract and not checked"
takeaway: "A case study in why fixed evaluation protocols matter: the most used SAR ship benchmark was being split and scored inconsistently, so SatClip must publish its own frozen splits and scoring rules with every instrument"
---

# Zhang et al. 2021, SSDD official release

## Problem
SSDD was the first open deep-learning SAR ship dataset and became the default benchmark, but its original labels were coarse and papers used it in different ways (different splits, size definitions, inshore rules). Results were therefore not comparable, and its horizontal boxes no longer fit rotated-box or segmentation research.

## Approach
- The dataset's publishers relabel ships more carefully and release three versions: horizontal boxes (BBox-SSDD), rotated boxes (RBox-SSDD) and polygon masks (PSeg-SSDD).
- Fix strict usage standards: train-test split, an inshore versus offshore protocol, ship-size definitions, and rules for dense small ships and ships berthed side by side in ports.
- Base those standards on how existing papers had actually used the data.

## Data and benchmarks
- Survey of 161 public reports, of which 46.59% (about 75) used SSDD.
- Comprehensive statistical analysis of the three label versions (details not re-checked).

## Key results
- Mainly a data and protocol contribution; the abstract reports usage statistics, not detector scores.
- Gives design advice for future detectors based on the data analysis (not verified in detail).

## Limitations
- Small chip-based dataset; it does not test whole-scene search the way LS-SSDD (entry 160) does.
- Mixed sensors and resolutions (not confirmed here) mean results may not reflect Sentinel-1 at 10 m alone.
- Protocols fix comparability but not label completeness.

## What it means for SatClip
- **Adopt the lesson, not the dataset**: every SatClip instrument (SAR water, NDVI change, any later ship detector) ships with a frozen split, a written scoring rule and an inshore-style edge-case rule (for example river banks and paddy fields for water), recorded in the receipt.
- When citing external accuracy for a component, cite the protocol used, or treat the figure as not comparable.
- Use SSDD only for a quick sanity test of a ship detector; use LS-SSDD for Sentinel-1 claims.
