---
id: 117
title: "XLRS-Bench: Could Your Multimodal LLMs Understand Extremely Large Ultra-High-Resolution Remote Sensing Imagery?"
authors: "Fengxiang Wang, Hongzhen Wang, Mingshuo Chen, Di Wang, et al. (12 authors, incl. Jing Zhang, Zhiyuan Liu, Maosong Sun)"
year: 2025
venue: "IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR 2025)"
link: https://arxiv.org/abs/2503.23771
code: https://xlrs-bench.github.io/ (project page; GitHub repo not confirmed)
category: rs-benchmark
era: recent
tags: [mllm-benchmark, ultra-high-resolution, counting, change-detection, visual-grounding, reasoning, bilingual]
verified: "2026-10-06 via https://arxiv.org/abs/2503.23771 and https://arxiv.org/html/2503.23771; CVPR 2025 acceptance taken from the arXiv comment; project page fetched but lists no repo link; grounding table units are not stated clearly"
takeaway: "On huge real scenes the best MLLMs average about 40% on four-option questions and almost never draw a correct box, so SatClip should tile scenes and measure with instruments rather than ask a VLM to read a whole Sentinel scene"
---

# XLRS-Bench

## Problem
RS benchmarks for multimodal LLMs use small crops, while real RS scenes are thousands of pixels wide. Existing sets also have limited annotation quality and few evaluation dimensions, especially for decision-oriented reasoning and change over time.

## Approach
- Collects 1,400 very large images (average about 8,500 x 8,500 pixels) from detection sets such as DOTA-v2 and ITCVD and segmentation sets such as MiniFrance.
- 45 experts annotate and cross-verify 16 sub-tasks: 10 perception abilities (classification, counting, spatial relations, object properties, fine-grained grounding) and 6 reasoning abilities (route planning, anomaly detection and interpretation, complex counting, condition-based grounding, regional counting with change detection).
- Detailed captions use a semi-automatic pipeline: GPT-4o sees nine sub-images plus a compressed full view, and humans verify.
- English and Chinese versions; VQA is four-option multiple choice.

## Data and benchmarks
- 45,942 annotations: 32,389 VQA pairs, 12,619 grounding instances, 934 detailed captions.
- Includes a bi-temporal sub-task (counting change between two dates, 270 questions).
- Models: GPT-4o, GPT-4o-mini, Qwen2-VL, LLaVA variants, CogVLM2, InternVL2, InternLM-XComposer-2.5, GeoChat.

## Key results
- Best English VQA average is about 40% (CogVLM2 39.80, Qwen2-VL 38.99); GPT-4o averages 32.15 and GeoChat 22.03, against a 25% chance level for four options.
- Counting is weak across the board: Qwen2-VL 39.72, GPT-4o 29.51 on the counting dimension.
- Visual grounding is close to zero: the best Acc@0.5 on the English set is 0.46 (GPT-4o), with most models below 0.2, and Acc@0.7 near 0.
- The RS-specific GeoChat trails general models, which the authors link to its small input resolution.

## Limitations
- Optical very high resolution only; the authors note no multispectral data and no SAR.
- Mostly multiple choice, so numeric answers are graded as picks, not as measured errors.
- Images come from existing detection and segmentation sets, mostly non-Indian locations.

## What it means for SatClip
- Strong evidence for SatClip's tile-by-tile instrument design: whole-scene VLM reading collapses on large images, and a Sentinel-1 district mosaic is exactly that scale.
- Never let a VLM answer "how many" or "where exactly": the change-counting sub-task shows near-chance performance, so SatClip's change answers should come from the log-ratio instrument with a confidence and abstention.
- If SatClip adds a VLM explanation step, feed it the instrument outputs and a small crop, not the full scene, and keep its text out of the number on the evidence card.
