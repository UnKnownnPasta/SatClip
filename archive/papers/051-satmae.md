---
id: 051
title: "SatMAE: Pre-training Transformers for Temporal and Multi-Spectral Satellite Imagery"
authors: "Yezhen Cong, Samar Khanna, Chenlin Meng, Patrick Liu, Erik Rozi, Yutong He, Marshall Burke, David B. Lobell, Stefano Ermon"
year: 2022
venue: "NeurIPS 2022"
link: https://arxiv.org/abs/2207.08051
code: https://github.com/sustainlab-group/SatMAE
category: eo-foundation
era: recent
tags: [masked-autoencoder, self-supervised, vit, multispectral, temporal, sentinel-2, fmow-sentinel, land-cover]
verified: "2026-10-04 via https://arxiv.org/abs/2207.08051 and https://sustainlab-group.github.io/SatMAE/"
takeaway: "The founding MAE recipe for multispectral and temporal satellite data; treat it as background and baseline, not as a SatClip runtime component"
---

# SatMAE: Pre-training Transformers for Temporal and Multi-Spectral Satellite Imagery

## Problem
Labelled satellite data is scarce while unlabelled imagery is abundant. Standard masked autoencoders (MAE) were built for single RGB photos and ignore two things satellite data has: repeated observations over time and many spectral bands.

## Approach
SatMAE adapts MAE to satellite imagery in two variants:
- Temporal SatMAE: a sequence of images of the same place is tokenised with a temporal embedding, and patches are masked independently across time so the model cannot simply copy a patch from another date.
- Spectral SatMAE: bands are split into groups, each encoded separately with its own spectral positional encoding, so the transformer knows which band group a token came from.

## Data and benchmarks
- Introduces fMoW-Sentinel, a Sentinel-2 multispectral dataset built on the locations of the fMoW benchmark (released with the code).
- Evaluated on fMoW (RGB and temporal), fMoW-Sentinel and downstream remote sensing tasks including land cover classification and semantic segmentation.

## Key results
Per the abstract: up to 7% improvement over previous state of the art on supervised benchmarks, and up to 14% on downstream land cover classification and segmentation tasks. We did not re-verify per-dataset numbers.

## Limitations
- Optical only; no SAR.
- ViT backbones are trained and fine-tuned on GPUs; the paper is not about CPU inference.
- Pretraining data is global but not India-focused; no flood or monsoon evaluation.
- Produces features, not calibrated answers; needs a fine-tuned head per task.

## What it means for SatClip
- Use it as background for the design debate: MAE features need labelled fine-tuning, which is why SatClip relies on deterministic instruments plus zero-shot CLIP for the CPU prototype.
- Its band grouping idea is worth copying if our LoRA/GPU pipeline ever feeds Sentinel-2 bands beyond RGB to a vision encoder.
- Do not ship SatMAE in the CPU path; later models in this archive (CROMA, DOFA, Prithvi-EO-2.0) supersede it and add SAR or sensor flexibility.
- If we compare a learned land cover head against zero-shot CLIP, a SatMAE fine-tune on fMoW-Sentinel style tiles is a citable, reproducible baseline.
