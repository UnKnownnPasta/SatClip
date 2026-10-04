---
id: 032
title: "Spatial-Aware Conformal Prediction for Trustworthy Hyperspectral Image Classification"
authors: "Kangdao Liu, Tianhao Sun, Hao Zeng, Yongshan Zhang, Chi-Man Pun, Chi-Man Vong"
year: 2024
venue: "arXiv preprint (arXiv:2409.01236, v2 October 2024)"
link: https://arxiv.org/abs/2409.01236
code: https://github.com/J4ckLiu/SACP
category: trust-calibration
era: recent
tags: [conformal-prediction, remote-sensing, hyperspectral, pixel-classification, spatial-correlation, coverage-guarantee]
verified: "2026-10-04 via https://arxiv.org/abs/2409.01236 and https://github.com/J4ckLiu/SACP"
takeaway: "Conformal prediction works for per-pixel RS classification, and smoothing non-conformity scores over spatial neighbours gives smaller sets at the same guaranteed coverage; apply it to SatClip masks"
---

# Spatial-Aware Conformal Prediction for Trustworthy Hyperspectral Image Classification

## Problem
Deep hyperspectral image classifiers reach high accuracy but give no rigorous statement of how confident each pixel label is. Standard conformal prediction treats each pixel independently and ignores the strong spatial correlation in remote sensing imagery.

## Approach
The authors first argue theoretically that conformal prediction's coverage guarantee applies to hyperspectral pixel classification. They then propose SACP (Spatial-Aware Conformal Prediction), which aggregates non-conformity scores from spatially correlated neighbouring pixels before computing the conformal quantile, so that a pixel surrounded by confident neighbours gets a tighter set. It is a post-hoc wrapper that works with existing scores such as APS, RAPS and SAPS.

## Data and benchmarks
The released code supports Indian Pines, Pavia University and Salinas, the standard hyperspectral benchmarks. (Indian Pines is an agricultural test site in Indiana, USA, not India.)

## Key results
The abstract claims that both theory and experiments show SACP improves prediction set efficiency (smaller sets) while maintaining the user-specified coverage, for example 95%. Specific set-size or coverage figures were not confirmed from the fetched abstract or README, so none are quoted.

## Limitations
Preprint status on arXiv at the time of verification; no peer-reviewed venue was shown. Benchmarks are small, single-scene airborne hyperspectral images with random pixel splits, where calibration and test pixels are spatially close, which flatters exchangeability. No Sentinel-1 or Sentinel-2 data, no temporal change, no geographic shift.

## What it means for SatClip
- Apply conformal prediction to SatClip's per-pixel masks (water, built-up, crop stress), not just to scene-level answers, and use spatial aggregation of scores so isolated noisy pixels do not dominate.
- Turn per-pixel sets into the evidence card's mask legend: "certainly water", "certainly not water", "ambiguous" (set contains both), and report the ambiguous area as a fraction so users see uncertainty spatially.
- Avoid the random-pixel-split trap in our own evaluation: calibrate and test on spatially and temporally separate Indian tiles (different districts and dates), or coverage claims will be optimistic.
- The code is light and model-agnostic, suitable for CPU post-processing of SAR threshold margins once they are mapped to scores.
