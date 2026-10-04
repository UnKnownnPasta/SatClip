---
id: 030
title: "Reliable Visual Question Answering: Abstain Rather Than Answer Incorrectly"
authors: "Spencer Whitehead, Suzanne Petryk, Vedaad Shakib, Joseph Gonzalez, Trevor Darrell, Anna Rohrbach, Marcus Rohrbach"
year: 2022
venue: "ECCV 2022"
link: https://arxiv.org/abs/2204.13631
code: https://github.com/facebookresearch/reliable_vqa
category: trust-calibration
era: recent
tags: [vqa, abstention, selective-prediction, risk-coverage, effective-reliability, selector]
verified: "2026-10-04 via https://arxiv.org/abs/2204.13631"
takeaway: "Softmax-thresholded VQA models answer under 7.5% of questions at 1% risk; a learned multimodal selector raises coverage from 6.8% to 15.6%, and Effective Reliability penalises wrong answers more than abstentions"
---

# Reliable Visual Question Answering: Abstain Rather Than Answer Incorrectly

## Problem
VQA systems answer every question, even when they are likely wrong. For real users, a wrong confident answer is worse than "I don't know", yet VQA evaluation rewarded answering everything.

## Approach
The paper frames VQA as selective prediction: the model may abstain. It compares abstention driven by the answer softmax score with a learned selection function, a separate head that sees image, question and answer representations and predicts whether the answer is correct. Evaluation uses risk-coverage analysis (coverage at fixed low risk levels) and a new Effective Reliability metric that gives credit for correct answers, zero for abstentions, and a penalty for wrong answers.

## Data and benchmarks
VQA v2, with several VQA model architectures.

## Key results
Per the abstract: models above 70% overall accuracy on VQA v2 can answer fewer than 7.5% of questions if they must keep risk at 1% using softmax confidence. The multimodal selector raises coverage at 1% risk by about 2.3 times, from 6.8% to 15.6%.

## Limitations
Even with the selector, coverage at very low risk stays small, showing that confidence estimation is still hard. The selector needs held-out labelled data and is trained in-distribution, so its behaviour under domain shift is uncertain. Natural images only. The penalty weight in Effective Reliability is a design choice that changes rankings.

## What it means for SatClip
- Adopt Effective Reliability (with an explicit cost for wrong answers, set by the use case: higher for flood relief than for planner curiosity) as SatClip's headline metric instead of plain accuracy.
- Expect low coverage at strict risk targets and be upfront about it; the paper's numbers show that honest abstention means declining many questions, which is a feature for district officials, not a bug.
- Copy the selector idea in a lightweight form: a small model (for example gradient-boosted trees) over instrument outputs and scene quality features (cloud cover, SAR noise, revisit gap, mask fragmentation) that predicts "this answer is right", trained on Indian validation cases.
- Report coverage at 1%, 5% and 10% risk alongside the evidence card, to beat VLM baselines that never abstain.
