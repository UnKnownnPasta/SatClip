---
id: 130
title: "What Uncertainties Do We Need in Bayesian Deep Learning for Computer Vision?"
authors: "Alex Kendall, Yarin Gal"
year: 2017
venue: "NeurIPS 2017 (NIPS 2017)"
link: https://arxiv.org/abs/1703.04977
code: "none found (no official repository confirmed)"
category: trust-calibration
era: historical
tags: [aleatoric-uncertainty, epistemic-uncertainty, semantic-segmentation, per-pixel-uncertainty, bayesian-deep-learning, mc-dropout]
verified: "2026-10-07 via arXiv API export.arxiv.org/api/query?id_list=1703.04977 (title, authors, first posted 2017-03-15, comment NIPS 2017, abstract); WebFetch was refused, curl used; summary based on the abstract plus standard knowledge, full text not fetched"
takeaway: "SatClip should separate uncertainty from the sensor (speckle, cloud, mixed pixels, which more data cannot fix) from uncertainty from the method (thresholds tuned elsewhere, which local labels can fix), and say which one caused an abstention"
---

# Kendall and Gal 2017, aleatoric versus epistemic uncertainty

## Problem
Vision models can be uncertain for two different reasons: noise in the observation itself (aleatoric) and lack of knowledge in the model (epistemic). Which should be modelled, and how, for dense per-pixel tasks?

## Approach
- A Bayesian deep learning framework combining both kinds.
- Epistemic uncertainty from sampling model weights (Monte Carlo dropout).
- Input-dependent (heteroscedastic) aleatoric uncertainty predicted by the network itself, which gives a loss that down-weights noisy pixels (learned attenuation).
- Applied to per-pixel semantic segmentation and depth regression.

## Data and benchmarks
Semantic segmentation and depth regression benchmarks (the abstract does not name them; commonly reported as CamVid, NYUv2 and Make3D, not confirmed here).

## Key results
- Modelling both types helps, and they behave differently: epistemic uncertainty is high on unfamiliar inputs and shrinks with more data, while aleatoric uncertainty is high at object edges, distant regions and noisy pixels and does not shrink with more data.
- The learned attenuation loss made models more robust to noisy data and gave new state-of-the-art results on the paper's segmentation and depth benchmarks (per the abstract; numbers not restated here).

## Limitations
- Epistemic estimates from MC dropout are approximate and can themselves be miscalibrated.
- Per-pixel uncertainty must still be aggregated to region-level quantities, which the paper does not address.

## What it means for SatClip
- Aleatoric sources for SatClip are concrete: SAR speckle, wind-roughened water, radar shadow and layover in hills, Sentinel-2 cloud and haze in the monsoon, and mixed pixels at field edges. More training data will not remove these; only a better scene (another date, another sensor) will.
- Epistemic sources: a threshold tuned on Bangladesh or Sen1Floods11 applied to a district it has never seen, or crop calendars that differ by state. Local labelled events reduce these.
- The abstention message should name the dominant cause, for example "cloud cover over 40 percent of the tile, try the next Sentinel-1 pass" versus "method not validated for this region", because the official's next step differs.
- Per-pixel uncertainty maps, propagated to tile area, give the range on the flooded-hectares number.
