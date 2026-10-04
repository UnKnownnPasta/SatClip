---
id: 027
title: "Selective Classification for Deep Neural Networks"
authors: "Yonatan Geifman, Ran El-Yaniv"
year: 2017
venue: "NeurIPS 2017 (NIPS 2017)"
link: https://arxiv.org/abs/1705.08500
code: none
category: trust-calibration
era: historical
tags: [selective-prediction, abstention, reject-option, risk-coverage, guarantees, softmax-response]
verified: "2026-10-04 via https://arxiv.org/abs/1705.08500 and https://nips.cc/virtual/2017/poster/9264"
takeaway: "Pick the abstention threshold from a target risk with a statistical guarantee on held-out data; trading coverage for reliability (2% ImageNet top-5 error at about 60% coverage)"
---

# Selective Classification for Deep Neural Networks

## Problem
Deep classifiers always answer, even when they are unsure. In mission-critical settings it is better to let the model decline some inputs so that the answers it does give meet a guaranteed error rate.

## Approach
Given an already trained network, the method adds a reject option driven by a confidence function (the paper considers the maximum softmax response and MC-dropout based scores). A user specifies a desired risk (error on accepted inputs) and a confidence level; using a labelled held-out set, the algorithm searches for the threshold on the confidence score that guarantees, with high probability, that the risk on accepted inputs will not exceed the target. Coverage (the fraction of inputs answered) is whatever remains after meeting that constraint. The underlying framing is the risk-coverage trade-off.

## Data and benchmarks
CIFAR-10, CIFAR-100 and ImageNet with standard pretrained architectures.

## Key results
On ImageNet the authors report 2% top-5 error guaranteed with 99.9% probability while still answering almost 60% of the test set (per the arXiv abstract and the NeurIPS poster page). Softmax response was a strong and cheap confidence function in their experiments.

## Limitations
The guarantee holds only if test data comes from the same distribution as the held-out calibration set. The quality of selection is capped by the confidence function: a poorly ranked score yields low coverage. Calibration sets must be large enough for tight bounds at low risk levels. The method addresses classification only.

## What it means for SatClip
- Use this as the formal basis for SatClip's abstention rule: choose the "answer versus abstain" threshold per instrument from a target error rate (for example 5% on flood-or-not at village level) using a held-out Indian labelled set, not by hand-tuning.
- Plot risk-coverage curves for each instrument and report the operating point on the evidence card methodology page, so users see how often SatClip answers and how often it is wrong when it does.
- Keep a separate calibration set per region and season; the guarantee breaks under distribution shift, which is exactly what monsoon versus dry imagery introduces.
- The confidence function matters more than the threshold: rank quality features such as cloud fraction, SAR incidence angle and margin from the water threshold, not just raw model scores.
