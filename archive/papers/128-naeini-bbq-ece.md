---
id: 128
title: "Obtaining Well Calibrated Probabilities Using Bayesian Binning"
authors: "Mahdi Pakdaman Naeini, Gregory F. Cooper, Milos Hauskrecht"
year: 2015
venue: "Proceedings of the AAAI Conference on Artificial Intelligence, 29(1) (AAAI 2015)"
link: https://doi.org/10.1609/aaai.v29i1.9602
code: "none found"
category: trust-calibration
era: historical
tags: [bayesian-binning, bbq, expected-calibration-error, ece, mce, histogram-binning, post-hoc-calibration]
verified: "2026-10-07 via https://api.crossref.org/works/10.1609/aaai.v29i1.9602 (title, authors, journal, volume 29, issue 1, date 2015); WebFetch was refused, curl used; content summarized from standard knowledge, full text not fetched, dataset names and numeric results not confirmed"
takeaway: "Gives SatClip the ECE and MCE metrics for checking that a stated 0.80 confidence is right about 80 percent of the time, plus a binning calibrator that averages over bin choices"
---

# Naeini et al. 2015, Bayesian Binning into Quantiles (BBQ)

## Problem
Histogram binning calibrates scores by replacing each score with the observed positive rate in its bin, but results depend heavily on the number and placement of bins. There was also no widely used summary measure of calibration error.

## Approach
- BBQ (Bayesian Binning into Quantiles) considers many binning models with different numbers of equal-frequency bins.
- Each binning model is scored by its Bayesian marginal likelihood on calibration data, and predictions are a weighted average across models, so no single bin count must be chosen.
- The paper defines two summary measures that became standard: Expected Calibration Error (ECE, the bin-weighted average gap between confidence and accuracy) and Maximum Calibration Error (MCE, the worst bin's gap).

## Data and benchmarks
Experiments on simulated data and real binary classification datasets with several base classifiers; specific datasets were not confirmed here.

## Key results
- BBQ improves calibration over raw scores and is reported as competitive with or better than histogram binning, Platt scaling and isotonic regression on the paper's benchmarks, without hurting discrimination (stated qualitatively; exact numbers not confirmed).
- ECE and MCE give a single number for calibration that later work (Guo et al., entry 026) adopted.

## Limitations
- Binary classification only in the original form.
- ECE depends on the binning used to compute it and can hide errors in sparsely populated bins; MCE is noisy for small bins.
- Same-distribution assumption as all post-hoc calibrators.

## What it means for SatClip
- Report ECE and MCE per instrument and per region on held-out labelled events in the SatClip evaluation harness; MCE matters most near the 0.60 abstention threshold, since a badly calibrated bin there changes which cards are shown.
- Compute ECE separately for monsoon versus dry-season scenes and for each Indian state with labels, because a good global ECE can hide a bad local one.
- BBQ is an option when calibration data are moderate and choosing a bin count by hand would be arbitrary.
