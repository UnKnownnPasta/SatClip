---
id: 074
title: "Oriented R-CNN for Object Detection"
authors: "Xingxing Xie, Gong Cheng, Jiabao Wang, Xiwen Yao, Junwei Han"
year: 2021
venue: "ICCV 2021"
link: https://arxiv.org/abs/2108.05699
code: https://github.com/jbwang1997/OBBDetection
category: object-detection
era: recent
tags: [oriented-object-detection, two-stage, rotated-boxes, region-proposal, dota, hrsc2016, mmdetection]
verified: "2026-10-04 via https://arxiv.org/abs/2108.05699 and https://github.com/jbwang1997/OBBDetection"
takeaway: "Simple, fast two-stage rotated-box detector (75.87% mAP on DOTA, 96.50% on HRSC2016, 15.1 FPS on a GPU); a strong baseline if SatClip ever adds ship detection, but its GPU speed does not translate to our CPU budget"
---

# Oriented R-CNN for Object Detection

## Problem
Rotated-box detectors needed accurate oriented proposals, but earlier approaches either used many rotated anchors (slow) or learned extra transformation stages (complex and costly).

## Approach
A two-stage framework. Its oriented Region Proposal Network predicts oriented proposals directly from horizontal anchors using a compact "midpoint offset" box representation, at almost no extra cost over a standard RPN. A second-stage Oriented R-CNN head then extracts rotated region features and refines classification and box regression. Built on MMDetection in the OBBDetection codebase.

## Data and benchmarks
- DOTA (aerial, 15 classes; see entry 071).
- HRSC2016 (ship detection in optical imagery).

## Key results
- 75.87% mAP on DOTA and 96.50% mAP on HRSC2016 with a ResNet-50 backbone (as stated in the abstract; these are the paper's best settings).
- 15.1 FPS at 1024 by 1024 on a single RTX 2080Ti GPU with ResNet-50.

## Limitations
- Speed is reported only on a GPU; CPU throughput is not given.
- Evaluated on very high resolution optical imagery, not on 10 m Sentinel-2 or SAR.
- Two-stage pipeline with a dedicated codebase; integration and maintenance cost is non-trivial.

## What it means for SatClip
- Do not add it to the core: SatClip's questions (flood, vegetation, land cover) are area-based, and at 10 m most target objects are sub-pixel.
- If a stretch goal adds ship or barge detection (for example on high-resolution partner imagery), use Oriented R-CNN as the baseline and measure CPU latency per 1024 tile before promising it in the UI.
- Any detection output must go through the same evidence-card discipline: box overlay, scene ID, date and a calibrated detection score, with abstention below threshold.
- Prefer pixel-level SAR instruments for Sentinel-1 maritime questions (see entry 075) over adapting an optical rotated detector.
