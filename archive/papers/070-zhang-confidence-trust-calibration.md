---
id: 070
title: "Effect of Confidence and Explanation on Accuracy and Trust Calibration in AI-Assisted Decision Making"
authors: "Yunfeng Zhang, Q. Vera Liao, Rachel K. E. Bellamy"
year: 2020
venue: "FAT* 2020 (ACM Conference on Fairness, Accountability, and Transparency)"
link: https://doi.org/10.1145/3351095.3372852
code: none
category: human-factors
era: recent
tags: [confidence-display, trust-calibration, explanations, shap, user-study, decision-support, human-ai-teams]
verified: "2026-10-04 via https://arxiv.org/abs/2001.02114 and https://ar5iv.labs.arxiv.org/html/2001.02114"
takeaway: "Showing a confidence score helped people rely on AI more when it was confident, but did not raise joint accuracy, and SHAP explanations did not help calibration; SatClip should show calibrated confidence and treat it as a reliance aid, not an accuracy fix"
---

# Effect of Confidence and Explanation on Accuracy and Trust Calibration in AI-Assisted Decision Making

## Problem
In high-stakes settings full automation is often undesirable, so a person makes the final decision with AI help. Designers need to know whether showing the model's confidence or a local explanation helps people trust the AI appropriately and decide better.

## Approach
Two online experiments on an income prediction task. Experiment 1 used a factorial design varying whether a confidence score was shown, whether the AI prediction was shown, and whether the model had access to all features (a partial model lacked one attribute, so humans had complementary knowledge). Experiment 2 compared a baseline, a confidence-score condition and a local explanation condition (Shapley-value based feature contributions).

## Data and benchmarks
- UCI Adult (1994 US Census) income dataset; predict above or below 50K USD from eight attributes.
- Model accuracy about 84%.
- Experiment 1: 72 Mechanical Turk participants; Experiment 2: a much smaller group (reported in the version we read as 9 participants; confirm against the final paper).

## Key results
- Showing confidence significantly increased switching to the AI's answer, mostly on high-confidence trials, so trust became better aligned with model confidence.
- That better calibration did not significantly improve joint human-AI accuracy (assisted accuracy hovered around 75% across conditions in our reading).
- Local explanations showed no calibration benefit over baseline and did not improve accuracy.
- Any accuracy gain depends on humans having knowledge the model lacks, so they can correct its errors.

## Limitations
- Lay crowdworkers acting as proxies for experts, with no real-world stakes beyond small incentives.
- Relies on the model's probabilities being well calibrated; the authors note some models need post-hoc calibration first.
- Tabular, binary task; small Experiment 2 sample.

## What it means for SatClip
- Show calibrated confidence on every evidence card, and actually calibrate it (temperature scaling or isotonic on held-out Indian scenes); an uncalibrated score would mislead exactly the reliance behaviour this study measured.
- Do not expect confidence alone to make officials more accurate; pair it with the abstention threshold so low-confidence answers are withheld rather than merely labelled.
- Surface what users know that SatClip does not: invite local knowledge (for example "was this field already fallow?") so human complementarity can correct instrument errors.
- Skip feature-attribution heatmaps for the CLIP instrument as a trust tool; prefer showing the mask overlay, scene and date, which are verifiable.
- In our usability study, log switching behaviour by confidence bin, as this paper did, to check that trust tracks our confidence.
