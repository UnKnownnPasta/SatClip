---
id: 129
title: "Simple and Scalable Predictive Uncertainty Estimation using Deep Ensembles"
authors: "Balaji Lakshminarayanan, Alexander Pritzel, Charles Blundell"
year: 2017
venue: "NeurIPS 2017 (NIPS 2017)"
link: https://arxiv.org/abs/1612.01474
code: "none found (no official repository confirmed)"
category: trust-calibration
era: historical
tags: [deep-ensembles, predictive-uncertainty, epistemic-uncertainty, out-of-distribution, proper-scoring-rules]
verified: "2026-10-07 via arXiv API export.arxiv.org/api/query?id_list=1612.01474 (title, authors, first posted 2016-12-05, comment NIPS 2017, abstract); WebFetch was refused, curl used; summary based on the abstract plus standard knowledge, full text not fetched"
takeaway: "Running several independently varied instrument settings and reporting their spread is a cheap, model-agnostic way for SatClip to widen confidence when the instruments disagree"
---

# Lakshminarayanan et al. 2017, Deep Ensembles

## Problem
Neural networks give overconfident predictions and no reliable uncertainty. Bayesian neural networks address this but need changes to training and are expensive. Is there a simpler route to good predictive uncertainty?

## Approach
- Train several networks independently from different random initializations (and random data order), then average their predictive distributions.
- Train each member with a proper scoring rule (log likelihood; for regression, a Gaussian mean and variance head).
- Optionally add adversarial training to smooth predictions near the data.

## Data and benchmarks
Classification and regression benchmarks, out-of-distribution tests (examples from known versus unknown distributions), and a scaled-up evaluation on ImageNet, per the abstract.

## Key results
- The ensemble's uncertainty estimates are reported as well calibrated, matching or beating approximate Bayesian neural networks on the paper's benchmarks.
- On out-of-distribution inputs the ensemble expresses higher uncertainty.
- The method is parallel, needs little tuning, and scales to ImageNet.

## Limitations
- Training and inference cost grow linearly with the number of members.
- Members trained the same way can still share blind spots, so ensembles do not fix all shift failures (see entry 132).

## What it means for SatClip
- SatClip's numbers come from classical instruments, not networks, but the ensemble idea transfers: compute flooded area with a small set of reasonable variants (Otsu and Kittler-Illingworth thresholds, VV and VH, two speckle filter sizes) and treat their spread as epistemic uncertainty.
- When the variants disagree strongly on a tile's flooded area, lower the confidence or abstain; when they agree, the reported range can be tight.
- Report the area as a range across variants, not a single number, alongside the scene ID and date.
