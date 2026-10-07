---
id: 168
title: "FUSAR-R1: A Large-Scale Reasoning Model for Intelligent Interpretation of SAR Images"
authors: "Yi Yang, Xiaokun Zhang, Yuxuan Li, Ruyi Zhang, Xinpeng Zhou, Haipeng Wang"
year: 2026
venue: "arXiv preprint (arXiv:2607.16819, v1 18 July 2026); no peer-reviewed venue found"
link: https://arxiv.org/abs/2607.16819
code: "No code or weights link found in the arXiv record or HTML full text"
category: rs-vlm
era: upcoming
tags: [sar, reasoning, chain-of-thought, grpo, reinforcement-learning, qwen3-vl, land-cover, counting, metadata-priors, fudan]
verified: "2026-10-07 via curl to https://export.arxiv.org/api/query (title, authors, date, abstract) and curl to https://arxiv.org/html/2607.16819v1 (method, Table V numbers, conclusion); WebFetch permission request timed out; backbone size and test-set sizes not stated in the text we read"
takeaway: "The newest SAR reasoning VLM still emits bare answers with no confidence, abstention or scene receipt, and its land-cover proportion error (MAE 7.67) is too coarse for flood extent, so SatClip should keep SAR numbers in thresholds and use the VLM only to explain"
---

# Yang et al. 2026, FUSAR-R1 (SAR reasoning model with chain of thought and GRPO)

## Problem
SAR images are hard to read (speckle, unusual scattering, target and background mixing), and existing SAR VLMs map image to answer without step-by-step expert-like analysis or self-correction, which the authors argue makes their outputs hard to trust.

## Approach
- Backbone: Qwen3-VL (exact parameter count not stated in the text we read; the paper calls it a moderate size).
- Rebuilds the authors' earlier FUSAR-GEOVL-1M dataset into explicit chain-of-thought traces: 7 steps for aircraft, 6 for ships, 6 for land cover, each starting from image metadata (satellite, band, ground resolution, latitude and longitude) and using a scale prior to convert pixels to metres.
- Qwen3-8B is used to fill gaps in the original captions, followed by logical-consistency filtering.
- Two stages: supervised cold start on the reasoning traces, then GRPO with a KL constraint and a multi-task reward (format, detection, counting and category, land cover). The land-cover reward covers single-label, multi-label (Jaccard), per-region labels and area-proportion error with a tolerance.

## Data and benchmarks
Six in-house evaluation tasks derived from FUSAR-GEOVL-1M: detection with JSON boxes, classification and counting, main land-cover category, all land-cover categories, regional land-cover category, and land-cover proportion. Baselines: InternVL3.5 (4B, 8B), LLaVA-1.5-7B, Qwen2.5-VL (3B, 7B). No public SAR benchmark from another group is reported in the comparison table.

## Key results
- Table V: FUSAR-R1 reaches 67.33% counting accuracy, 85.24% main land-cover accuracy, 93.44% all-category accuracy, 64.75% regional land-cover accuracy and 7.67 MAE on land-cover proportion; the best baseline values in the same table are 45.45%, 44.23%, 75.81%, 13.11% and 39.58 respectively.
- Detection ablation: cold start plus GRPO gives precision 0.807, recall 0.568, F1 0.676; RL without the cold start collapses.
- Physical-prior ablation: image resolution is the most important metadata input for accuracy.

## Limitations
- Evaluation is on the authors' own data split, mostly high-resolution military-style targets (aircraft, ships), not Sentinel-1 at 10 m or flood scenes.
- No calibration, confidence score, uncertainty output or refusal behaviour; the word uncertainty appears only as motivation.
- Reasoning traces were partly written by an LLM, so the explanations may sound expert while not being faithful to the pixels.
- No code or weights found.

## What it means for SatClip
- Beat: SatClip's evidence card (scene ID, date, mask, calibrated confidence, abstain) is exactly what FUSAR-R1 lacks; cite it as the 2026 state of the art in SAR VLMs that still gives no provenance.
- Adopt: its finding that resolution and location metadata are the strongest priors supports passing scene metadata (orbit, polarisation, pixel spacing, district) as structured text into SatClip's explainer prompt.
- Avoid: a land-cover proportion MAE of 7.67 points means a VLM-read "percent flooded" can be off by several percent of a district; SatClip must keep area numbers in the SAR threshold instrument.
