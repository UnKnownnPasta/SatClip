---
id: 162
title: "RTMDet: An Empirical Study of Designing Real-Time Object Detectors"
authors: "Chengqi Lyu, Wenwei Zhang, Haian Huang, Yue Zhou, Yudong Wang, Yanyi Liu, Shilong Zhang, Kai Chen"
year: 2022
venue: "arXiv preprint (arXiv:2212.07784, December 2022); no peer-reviewed venue found on arXiv or Crossref"
link: https://arxiv.org/abs/2212.07784
code: "https://github.com/open-mmlab/mmdetection/tree/3.x/configs/rtmdet (named in the abstract; not fetched)"
category: object-detection
era: recent
tags: [real-time-detection, rotated-detection, lightweight, depthwise-convolution, large-kernel, dynamic-label-assignment, mmdetection, mmrotate]
verified: "2026-10-07 via curl to https://export.arxiv.org/api/query?id_list=2212.07784 (title, authors, date, abstract); Crossref search found no conference or journal version; rotated-detection numbers are claimed in the abstract but not quoted because no figure is given there"
takeaway: "If SatClip ever adds a learned detector, start from the tiny RTMDet rotated variant in an open toolbox: one family covers boxes, rotated boxes and instance masks at several sizes, which suits a CPU budget better than heavy two-stage models"
---

# Lyu et al. 2022, RTMDet

## Problem
Real-time detectors (the YOLO line) are fast but each targets one task. The authors want a single efficient design that beats YOLO models on speed and accuracy and extends easily to instance segmentation and rotated-box detection.

## Approach
- Backbone and neck of matched capacity, built from a basic block with large-kernel depth-wise convolutions.
- Soft labels in the matching cost of dynamic label assignment.
- Improved training recipe; five model sizes from tiny to extra-large.

## Data and benchmarks
- COCO for general detection; the abstract also claims results on real-time instance segmentation and rotated object detection (benchmark names for the rotated task, such as DOTA, are not stated in the abstract).

## Key results
- 52.8% AP on COCO at over 300 FPS on an NVIDIA RTX 3090 GPU (largest model; as stated in the abstract).
- Best parameter-accuracy trade-off across its five sizes and claimed state of the art for real-time rotated detection (no rotated figure verified here).

## Limitations
- Speed is measured on a desktop GPU; CPU latency is not reported in the abstract.
- Designed for natural and very high resolution imagery; objects at Sentinel's 10 m are mostly a few pixels or smaller.
- Preprint only; claims rely on the authors' own toolbox benchmarks.

## What it means for SatClip
- **Adopt as the default learned detector candidate** (tiny rotated variant, exported to ONNX for CPU) if a ship or large-structure instrument is ever added; measure CPU latency ourselves before promising anything.
- Prefer it over Oriented R-CNN (entry 074) for SatClip's budget, and over heavier RS-specific backbones such as LSKNet (entry 163) unless accuracy demands it.
- Its output is still only a score per box: SatClip must calibrate those scores on held-out scenes (for example LS-SSDD, entry 160) before showing counts.
