---
id: 127
title: "Transforming classifier scores into accurate multiclass probability estimates"
authors: "Bianca Zadrozny, Charles Elkan"
year: 2002
venue: "Proceedings of the Eighth ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD 2002), pp. 694-699"
link: https://doi.org/10.1145/775047.775151
code: "none found (isotonic calibration is available in scikit-learn CalibratedClassifierCV method=isotonic)"
category: trust-calibration
era: historical
tags: [isotonic-regression, pav, post-hoc-calibration, multiclass-calibration, binary-coupling]
verified: "2026-10-07 via https://api.crossref.org/works/10.1145/775047.775151 (title, authors, proceedings, pages 694-699, date 2002-07-23); WebFetch was refused, curl used; content summarized from standard knowledge, full text not fetched, dataset names and numeric results not confirmed"
takeaway: "Isotonic regression is SatClip's default non-parametric calibrator for instrument scores once there are enough labelled tiles, since it assumes only that a higher score should never mean a lower flood probability"
---

# Zadrozny and Elkan 2002, isotonic calibration

## Problem
Classifier scores (from SVMs, naive Bayes, boosted trees and others) rank examples well but are poor probability estimates. Parametric fixes such as Platt's sigmoid (entry 126) assume a particular shape. How can one calibrate with weaker assumptions, and extend that to more than two classes?

## Approach
- Calibrate binary scores with isotonic regression, fitted by the pair-adjacent violators (PAV) algorithm: the learned map is any non-decreasing step function from score to probability.
- For multiclass problems, break the task into binary problems (one-against-all or all-pairs), calibrate each, then combine the calibrated binary probabilities into a multiclass distribution (a coupling step).

## Data and benchmarks
Evaluated on standard classification datasets with several base classifiers; the specific datasets were not confirmed here because the full text was not fetched.

## Key results
- Isotonic regression improves probability quality over raw scores and is competitive with or better than the sigmoid when enough calibration data exist (stated qualitatively; exact numbers not confirmed).
- The binary-to-multiclass coupling yields usable multiclass probabilities from calibrated binary pieces.

## Limitations
- Being non-parametric, isotonic regression can overfit with small calibration sets; the step function can be jagged and produce ties.
- Like all post-hoc methods, it assumes calibration and deployment data come from the same distribution.

## What it means for SatClip
- The only structural assumption, monotonicity, matches SatClip's instruments: a deeper backscatter drop or larger NDVI loss should never lower the flood or crop-loss probability.
- Use Platt (two parameters) while labelled Indian tiles are few, and switch to isotonic once a few thousand labelled pixels or tiles per sensor mode exist; pick between them on held-out reliability diagrams and ECE (entry 128).
- The multiclass coupling idea suits crop-change cards with several outcomes (no change, loss, gain, flooded), where each binary score is calibrated then combined before the abstention test.
