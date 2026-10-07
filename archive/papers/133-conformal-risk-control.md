---
id: 133
title: "Conformal Risk Control"
authors: "Anastasios N. Angelopoulos, Stephen Bates, Adam Fisch, Lihua Lei, Tal Schuster"
year: 2024
venue: "ICLR 2024 (spotlight); arXiv first posted August 2022"
link: https://arxiv.org/abs/2208.02814
code: "https://github.com/aangelopoulos/conformal-risk (listed in the arXiv comment; repository not opened from this session)"
category: trust-calibration
era: recent
tags: [conformal-prediction, risk-control, false-negative-rate, distribution-free, segmentation, finite-sample-guarantee]
verified: "2026-10-07 via arXiv API export.arxiv.org/api/query?id_list=2208.02814 (title, authors, first posted 2022-08-04, abstract, code link in comment) and OpenReview search api2.openreview.net (forum 33XGfHLtZg, venue ICLR 2024 spotlight, same five authors); WebFetch was refused, curl used; summary based on the abstract, full text not fetched"
takeaway: "Lets SatClip pick its flood-mask threshold from labelled Indian events so that the expected share of truly flooded area it misses stays below a stated level, with a finite-sample guarantee"
---

# Angelopoulos et al. 2024, Conformal Risk Control

## Problem
Standard conformal prediction guarantees that a prediction set contains the true label with a chosen probability (miscoverage). Many tasks care about other losses, such as the fraction of a true object a segmentation mask misses. Can the same distribution-free guarantee cover the expected value of a general loss?

## Approach
- Generalize split conformal prediction to control the expected value of any loss that is monotone in a tuning parameter (for example a threshold that makes a mask larger).
- On a held-out calibration set, choose the smallest parameter whose adjusted empirical risk is below the target level; this guarantees the expected risk on a new exchangeable example is at most the target.
- Extensions for distribution shift, quantile risk, multiple and adversarial risks, and U-statistic losses.

## Data and benchmarks
Worked examples from computer vision and natural language processing, including bounding the false negative rate of segmentation masks, a graph distance, and token-level F1, per the abstract.

## Key results
- The guarantee holds in finite samples without distributional or model assumptions beyond exchangeability, and is tight up to an O(1/n) term (per the abstract).
- It reduces to ordinary split conformal coverage when the loss is the miscoverage indicator.

## Limitations
- The guarantee is on average over new examples, not conditional on a given tile; a specific district can still do worse.
- Requires exchangeable calibration and test data; the shift extensions need weights or bounds that may be hard to estimate for new regions.
- Needs labelled calibration examples with dense ground truth.

## What it means for SatClip
- Natural fit for flood extent: define the loss as the fraction of truly flooded pixels in a tile that SatClip's mask misses (false negative rate), and calibrate the SAR threshold offset on labelled Indian events so the expected miss rate stays below, say, 10 percent.
- The same machinery can bound area error directly, giving each tile an area range that is wide enough in expectation, which is more honest for a district official than a single hectare figure.
- Pair with the 0.60 abstention rule: if meeting the risk target needs a mask so large that it is uninformative for that tile, abstain.
- Because the guarantee assumes exchangeability, calibrate per region and season (see entry 132) and state the calibration events on each answer card.
