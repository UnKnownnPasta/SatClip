---
id: 082
title: "FUSAR-GPT: A Spatiotemporal Feature-Embedded and Two-Stage Decoupled Visual Language Model for SAR Imagery"
authors: "Xiaokun Zhang, Yi Yang, Ziqi Ye, Baiyun, Xiaorong Guo, Qingchen Fang, Ruyi Zhang, Xinpeng Zhou, Haipeng Wang"
year: 2026
venue: "CVPR 2026 (poster)"
link: https://arxiv.org/abs/2602.19190
code: "none found"
category: rs-vlm
era: recent
tags: [vlm, sar, alphaearth, geospatial-embeddings, qwen2.5-vl, two-stage-sft, counting, detection, gaofen-3]
verified: "2026-10-05 via https://arxiv.org/abs/2602.19190, https://arxiv.org/html/2602.19190 and https://cvpr.thecvf.com/virtual/2026/poster/40157 (CVPR 2026 poster listing, no code link)"
takeaway: "Injecting location-keyed AlphaEarth embeddings lifts a 7B SAR VLM by 7 to 12 points, a hint that SatClip could add a precomputed geospatial prior; but its own counting accuracy is about 53% on a small test set, so SAR answers still need instruments"
---

# FUSAR-GPT: A Spatiotemporal Feature-Embedded and Two-Stage Decoupled Visual Language Model for SAR Imagery

## Problem
General VLMs pretrained on photos perform poorly on SAR: backscatter has no colour or familiar texture, scenes are noisy and information sparse, and SAR text corpora are scarce. Scaling the model does not fix this; the authors observe Qwen3-VL 8B scoring below the 4B version on SAR counting.

## Approach
Built on Qwen2.5-VL-7B. For each SAR image, its geographic and time footprint (a "spatiotemporal anchor") is used to fetch the matching AlphaEarth Foundations embedding field (a 64-dimensional embedding that summarizes optical, SAR and other sources per location). A modulation module inspired by conditional normalization injects these embeddings into the visual encoder output without altering the backbone. Training is decoupled: stage one trains the embedding MLP and LoRA adapters for knowledge injection on SAR image-text pairs; stage two trains only LoRA for downstream tasks. The authors note they do not explicitly model temporal dynamics, despite the "spatiotemporal" name.

## Data and benchmarks
Built from FUSAR-GEOVL (part of FUSAR-KLIP), which keeps real coordinates: 10k AlphaEarth-image-text triplets (Gaofen-3 and other platforms, multi-resolution), of which 2k images with target annotations are used for downstream training and evaluation. Tasks: target counting, grid-based localization, coarse and fine classification, category-prompted detection, and corpus-level captioning. Baselines (Qwen2, Qwen2.5, Qwen3, LLaVA, InternVL families) were fine-tuned under the same settings.

## Key results
From the paper:
- Counting accuracy 52.53% versus a best baseline of 45.45%; most baselines sit between 30% and 40%.
- Grid localization: 52.02% Acc@100, 79.29% Acc@50, 91.41% Top-1, about 8 to 12 points above the best baseline.
- Classification gains over Qwen2.5-VL-7B above 12 points in coarse categories.
- Fusion ablation: the modulation module (52.53) beats simple sum (36.36) and concatenation (37.88); ChatGPT-5.2 and Gemini-3 scored 18.18 and 30.3 on the same comparison table.
- Detection versus the specialist R3Det: F1 58.70 versus 52.20.

## Limitations
The evaluation set is small (derived from 2k annotated images; the counting percentages are consistent with a test split of roughly 200 images, our inference), so differences of a few points are fragile. Targets are ships, planes and similar objects in high-resolution Gaofen-3 style data, not water extent or crops in 10 m Sentinel-1. AlphaEarth embeddings are tied to a location and year, so they carry prior knowledge about a place rather than its state on the flood date, which risks the model answering from the prior instead of the image. No released code found, no confidence or abstention.

## What it means for SatClip
- Interesting idea to borrow cheaply: precomputed geospatial embeddings (AlphaEarth annual layers are distributed via Earth Engine) could serve as a context prior for SatClip's land-cover step, for example to tell the explainer that a pixel is usually paddy, without involving a 7B model.
- Danger to avoid: a prior that "knows" a place can mask what actually happened on the date. SatClip should keep the flood measurement purely from the dated Sentinel-1 scene and show any prior separately on the card.
- The paper's own numbers (counting near 53%, frontier chat models far lower) are another data point that SAR interpretation by VLMs is unreliable, supporting SatClip's instruments-first rule.
- No measurement, provenance, calibrated confidence or abstention, so it does not undercut the evidence-card claim.
