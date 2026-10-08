---
id: 198
title: "Dropout as a Bayesian Approximation: Representing Model Uncertainty in Deep Learning"
authors: "Yarin Gal, Zoubin Ghahramani"
year: 2016
venue: "Proceedings of the 33rd International Conference on Machine Learning (ICML 2016); arXiv:1506.02142 (v1 June 2015, v6 October 2016)"
link: https://arxiv.org/abs/1506.02142
code: "No official code link in the arXiv record"
category: historical
era: historical
tags: [mc-dropout, bayesian-deep-learning, model-uncertainty, epistemic, gaussian-process, uncertainty-estimation, foundation]
verified: "2026-10-08 via curl to https://export.arxiv.org/api/query (title, authors, dates, abstract, comment stating publication in ICML 2016 and an October 2016 correction to standard errors); WebFetch permission request timed out; ICML proceedings page not fetched, so volume and page numbers are not given"
takeaway: "The founding paper for MC dropout: keep dropout on at test time and average several passes to get a cheap model-uncertainty estimate; SatClip can use it on its flood or crop segmentation head as one input to the confidence score, but must still calibrate it, since raw MC dropout is not calibrated by itself"
---

# Gal and Ghahramani 2016, MC dropout as approximate Bayesian inference

## Problem
Standard deep networks give point predictions and softmax scores that do not express how unsure the model is. Full Bayesian neural networks express this but are too costly to train and run.

## Approach
- Shows that a network trained with dropout before each weight layer is mathematically equivalent to an approximation of a deep Gaussian process, so dropout training is a form of approximate variational inference.
- Practical recipe: keep dropout active at test time, run T stochastic forward passes, and use the mean as the prediction and the spread (variance, or predictive entropy for classification) as model uncertainty.
- No change to training and no extra parameters; cost is T forward passes at inference.

## Data and benchmarks
MNIST experiments on uncertainty behaviour, a set of UCI regression datasets compared with earlier Bayesian approximations, and a deep reinforcement learning task using the uncertainty for exploration.

## Key results
- Reports better predictive log-likelihood and RMSE than the existing approximate Bayesian methods it compares against on the regression benchmarks (abstract; numbers not restated here).
- The October 2016 revision fixed a standard-error mistake and added an updated results table.

## Limitations
- The approximation's quality depends on dropout rate and placement; later work (for example Ovadia et al. 2019, entry 132) found MC dropout uncertainty degrades under dataset shift and is often worse than deep ensembles (entry 129).
- Produces uncertainty, not calibrated probabilities; post-hoc calibration is still needed.
- T passes multiply inference cost, which matters on CPU.

## What it means for SatClip
- Adopt: a low-cost way to get per-pixel model uncertainty from SatClip's segmentation head without training an ensemble; aggregate it over the district mask as a feature for the confidence model.
- Avoid: do not show MC dropout variance to users as "confidence"; feed it into the calibration step (temperature or isotonic, entries 026 and 127) and the abstention threshold.
- CPU budget: a small T (for example 5 to 10) on a COG window is feasible; compare against a 3 to 5 member ensemble before choosing.
