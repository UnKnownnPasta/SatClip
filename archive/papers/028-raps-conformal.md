---
id: 028
title: "Uncertainty Sets for Image Classifiers using Conformal Prediction"
authors: "Anastasios Angelopoulos, Stephen Bates, Jitendra Malik, Michael I. Jordan"
year: 2021
venue: "ICLR 2021 (Spotlight)"
link: https://arxiv.org/abs/2009.14193
code: https://github.com/aangelopoulos/conformal_classification
category: trust-calibration
era: recent
tags: [conformal-prediction, prediction-sets, coverage-guarantee, raps, aps, distribution-free]
verified: "2026-10-04 via https://arxiv.org/abs/2009.14193"
takeaway: "RAPS wraps any classifier to output label sets with a finite-sample coverage guarantee (for example 90%), with sets often 5 to 10 times smaller than a Platt-scaling baseline"
---

# Uncertainty Sets for Image Classifiers using Conformal Prediction

## Problem
A single top label with a softmax score gives no formal promise about correctness. Calibration methods such as Platt scaling improve scores but carry no guarantee. Users of high-stakes classifiers need a statement like "the true class is in this set with 90% probability", and the set should be small enough to be useful.

## Approach
The paper builds on split conformal prediction, specifically adaptive prediction sets (APS): on a held-out calibration set, compute a non-conformity score from sorted softmax probabilities, take a quantile, and at test time include classes until that quantile is reached. Their Regularized Adaptive Prediction Sets (RAPS) adds a penalty on including low-ranked, low-probability classes, which stops the long tail of noisy small scores from inflating set sizes. The guarantee is distribution-free and finite-sample, requiring only exchangeability between calibration and test data.

## Data and benchmarks
ImageNet and ImageNet-V2, with ResNet-152 and other pretrained models.

## Key results
Per the abstract, RAPS achieves the target coverage with sets that are often 5 to 10 times smaller than a stand-alone Platt scaling baseline. Detailed per-model set sizes and coverage figures were not extracted from the fetched page.

## Limitations
Coverage is marginal (on average over inputs), not conditional on each input or each subgroup, so coverage for a rare region or class can be worse than promised. It relies on exchangeability, which breaks under temporal or geographic shift. Sets can be uninformative (very large) when the base model is weak. Regularization hyperparameters need tuning on held-out data.

## What it means for SatClip
- Use conformal sets for SatClip's categorical answers (land-cover class, crop type, "flooded, not flooded, uncertain"): presenting "built-up or bare soil, 90% coverage" is more honest than one overconfident label.
- Map set size to abstention: if the conformal set at the chosen level contains contradictory answers (both flooded and not flooded), abstain and tell the user what extra evidence (a later SAR pass, a cloud-free optical scene) would help.
- Calibrate per region and season, and check coverage per district group, because marginal coverage can hide failures in exactly the under-represented Indian areas SatClip targets.
- The official code is small and model-agnostic, so it can wrap RemoteCLIP zero-shot logits on CPU with negligible overhead.
