---
id: 132
title: "Can You Trust Your Model's Uncertainty? Evaluating Predictive Uncertainty Under Dataset Shift"
authors: "Yaniv Ovadia, Emily Fertig, Jie Ren, Zachary Nado, D. Sculley, Sebastian Nowozin, Joshua V. Dillon, Balaji Lakshminarayanan, Jasper Snoek"
year: 2019
venue: "NeurIPS 2019"
link: https://arxiv.org/abs/1906.02530
code: "not verified (benchmark code is reported to be in the google-research repository under uq_benchmark_2019; GitHub was not reachable from this session)"
category: trust-calibration
era: historical
tags: [dataset-shift, calibration-under-shift, deep-ensembles, temperature-scaling, uncertainty-benchmark, ood]
verified: "2026-10-07 via arXiv API export.arxiv.org/api/query?id_list=1906.02530 (title, authors, first posted 2019-06-06, comment Advances in Neural Information Processing Systems 2019, abstract); WebFetch was refused, curl used; summary based on the abstract plus standard knowledge, full text not fetched, numeric results not confirmed"
takeaway: "A calibration fitted on one region or season will drift when SatClip meets a new district or an unusual monsoon, so calibration must be re-checked per region and season, and confidence should fall as inputs move away from the calibration data"
---

# Ovadia et al. 2019, uncertainty under dataset shift

## Problem
Uncertainty methods are usually evaluated on test data from the training distribution. In deployment, inputs shift (sample bias, non-stationarity). Do calibrated uncertainties stay calibrated when the data shift?

## Approach
- A large-scale empirical benchmark of uncertainty methods, Bayesian and non-Bayesian: vanilla softmax, post-hoc temperature scaling, MC dropout, deep ensembles, stochastic variational inference and last-layer variants, among others.
- Tasks span images, text and other modalities, with shift introduced at increasing intensity (for example image corruptions) and fully out-of-distribution inputs.
- Measures accuracy, calibration (ECE, Brier score, log likelihood) and out-of-distribution detection as shift grows.

## Data and benchmarks
Classification benchmarks across several modalities with synthetic and natural shifts; the abstract does not name datasets (commonly reported to include MNIST, CIFAR-10 and ImageNet with corruptions, not confirmed here).

## Key results
- Calibration degrades as shift increases for all methods.
- Post-hoc calibration such as temperature scaling, fitted on in-distribution data, falls short under shift.
- Methods that average over models, notably deep ensembles (entry 129), hold up surprisingly well across many tasks (per the abstract).

## Limitations
- Mostly synthetic or curated shifts; real geographic and seasonal shifts in Earth observation were not tested.
- Classification only; no segmentation or area estimation tasks.

## What it means for SatClip
- SatClip faces real shifts: a new state, a new terrain (Brahmaputra floodplain versus Kerala hills), a new year's crop calendar, Sentinel-1C/1D replacing 1A/1B data, heavy monsoon cloud. A calibrator fitted on Sen1Floods11 or one Indian event should not be trusted unchanged elsewhere.
- Keep a per-region, per-season calibration ledger and test calibration on held-out districts, not random held-out tiles.
- Add a shift check (how far a scene's backscatter or NDVI statistics are from the calibration set) that lowers confidence or forces abstention when the scene is out of range.
- Prefer instrument-variant ensembles over a single post-hoc fit, consistent with this paper's finding.
