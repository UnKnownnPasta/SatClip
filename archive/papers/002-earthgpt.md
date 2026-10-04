---
id: 002
title: "EarthGPT: A Universal Multi-modal Large Language Model for Multi-sensor Image Comprehension in Remote Sensing Domain"
authors: "Wei Zhang, Miaoxin Cai, Tong Zhang, Yin Zhuang, Xuerui Mao"
year: 2024
venue: "IEEE Transactions on Geoscience and Remote Sensing (TGRS), 2024"
link: https://arxiv.org/abs/2401.16822
code: https://github.com/wivizhang/EarthGPT
category: rs-vlm
era: recent
tags: [vlm, multi-sensor, sar, infrared, optical, instruction-tuning, mmrs-1m, llama2]
verified: "2026-10-04 via https://arxiv.org/abs/2401.16822 and https://github.com/wivizhang/EarthGPT"
takeaway: "MMRS-1M (optical, SAR, infrared) is a ready seed for LoRA data; its pixel-level weakness supports keeping masks in a separate, non-LLM head"
---

# EarthGPT: A Universal Multi-modal Large Language Model for Multi-sensor Image Comprehension in Remote Sensing Domain

## Problem
Multimodal LLMs work well on natural photos but remote sensing differs strongly, and earlier RS assistants handled mostly optical RGB. Analysts also need SAR and infrared, and a single model that covers many interpretation tasks across sensors.

## Approach
EarthGPT (Beijing Institute of Technology) combines three ideas. A visual-enhanced perception module fuses multi-layer ViT features (DINOv2 ViT-L/14) with multi-scale CNN features (frozen CLIP ConvNeXt-L) to keep both semantics and fine detail. A cross-modal mutual comprehension stage unfreezes some LLaMA-2 attention and norm layers while aligning on natural image-text data. Finally a unified instruction-tuning step (bias tuning) on remote sensing data lets one model handle many tasks without task-specific retraining.

## Data and benchmarks
The main contribution is MMRS-1M: over 1M image-text instruction pairs assembled from 34 existing RS datasets, spanning optical, SAR and infrared imagery. Tasks include scene classification, detection, captioning, VQA, visual grounding and region captioning. The repo states the dataset was fully released in October 2024.

## Key results
The fetched HTML version reports zero-shot scene classification of 77.37% on CLRS and 74.72% on NaSC-TG2, ahead of the compared MLLMs. I did not confirm SAR-specific or detection numbers from the fetched pages.

## Limitations
The paper acknowledges difficulty on tasks that need precise pixel-level localization. SAR coverage comes from existing curated datasets, not from Sentinel-1 GRD scenes as distributed, so transfer to raw Sentinel-1 is untested here. Released model weights were not clearly stated in the repo. No calibrated confidence or abstention mechanism is described.

## What it means for SatClip
- MMRS-1M is a ready source of SAR and optical instruction pairs: mine it for our LoRA fine-tune instead of writing all templates from scratch (check per-source licenses first).
- Its dual-encoder fusion (ViT plus CNN) is heavier than our CPU budget allows; adopt the lesson (multi-scale features help small objects) via tiling, not via a second encoder.
- Use it as evidence that one assistant across SAR and optical is feasible, which supports our cloud-cover fallback story.
- Pixel-level weakness reinforces our plan to output region masks from a segmentation or change-detection head, not from the language model.
- Report NaSC-TG2 or CLRS zero-shot accuracy for RemoteCLIP alongside EarthGPT's numbers if we claim classification quality.
