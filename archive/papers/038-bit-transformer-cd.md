---
id: 038
title: "Remote Sensing Image Change Detection with Transformers"
authors: "Hao Chen, Zipeng Qi, Zhenwei Shi"
year: 2021
venue: "IEEE Transactions on Geoscience and Remote Sensing (TGRS), 2021, DOI 10.1109/TGRS.2021.3095166"
link: https://arxiv.org/abs/2103.00208
code: https://github.com/justchenhao/BIT_CD
category: change-detection
era: recent
tags: [transformer, bit, semantic-tokens, siamese, building-change, levir-cd, whu-cd, dsifn-cd, efficient, optical-rgb]
verified: "2026-10-04 via https://arxiv.org/abs/2103.00208"
takeaway: "Strong, small (about 3.5M params) learned CD baseline at 89.3 F1 on LEVIR-CD but only 69.3 on DSIFN; a cross-check at most, never the source of SatClip's number"
---

# Remote Sensing Image Change Detection with Transformers

## Problem
Purely convolutional change detectors have limited receptive fields and struggle to relate distant regions across two dates, while dense self-attention over all pixels is expensive (quadratic in pixel count).

## Approach
The Bitemporal Image Transformer (BIT) extracts features from each date with a ResNet18 backbone, compresses each into a small set of semantic tokens, runs a transformer encoder over the tokens of both dates jointly to model space-time context, then projects the refined tokens back to pixel space with a transformer decoder. A prediction head classifies change from the feature difference.

## Data and benchmarks
Three building or land-cover change datasets of very high resolution RGB imagery: LEVIR-CD (entry 037), WHU-CD and DSIFN-CD. Training uses 256x256 crops. Code is released for non-commercial research use only.

## Key results
From Table II of the arXiv version, BIT_S4 (ResNet18) scores F1 89.31 / IoU 80.68 on LEVIR-CD, F1 83.98 / IoU 72.39 on WHU-CD and F1 69.26 / IoU 52.97 on DSIFN-CD, with 3.55M parameters and 4.35 GFLOPs. The authors report it beats a deeper convolutional baseline by 1.7, 2.4 and 10.8 F1 points on the three sets with about a third of its parameters and compute.

## Limitations
RGB only, sub-metre imagery, mostly buildings. The big gap between LEVIR-CD and DSIFN-CD scores shows how dataset-dependent learned CD is. Outputs a per-pixel score without calibration, and there is no mechanism to say "insufficient evidence". Non-commercial licence.

## What it means for SatClip
- BIT shows a learned detector can be small enough for CPU inference, but its scores do not transfer across datasets, which is exactly why SatClip keeps transparent instruments (log-ratio, index differencing, CVA) as the source of every number.
- If a learned model is ever used, use it only as a secondary agreement signal on the evidence card ("instrument and model agree on 82% of the mask"), with disagreement lowering confidence or triggering abstention.
- Report cross-dataset results, not single-benchmark F1, when evaluating any learned component; the 89 vs 69 F1 spread is the cautionary example.
- Avoid shipping BIT weights in a product without checking licence terms.
