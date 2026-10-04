---
id: 001
title: "GeoChat: Grounded Large Vision-Language Model for Remote Sensing"
authors: "Kartik Kuckreja, Muhammad Sohail Danish, Muzammal Naseer, Abhijit Das, Salman Khan, Fahad Shahbaz Khan"
year: 2024
venue: "CVPR 2024"
link: https://arxiv.org/abs/2311.15826
code: https://github.com/mbzuai-oryx/geochat
category: rs-vlm
era: recent
tags: [vlm, grounding, referring-detection, vqa, scene-classification, llava, instruction-tuning, optical-rgb]
verified: "2026-10-04 via https://arxiv.org/abs/2311.15826"
takeaway: "Baseline RS chat model (RGB only, 7B); reuse its task-token routing and dataset-to-instruction recipe, but do not trust VLM-emitted boxes (about 10.6% referring detection acc@0.5)"
---

# GeoChat: Grounded Large Vision-Language Model for Remote Sensing

## Problem
General-purpose vision-language models answer satellite queries poorly. Remote sensing scenes are high resolution, span many scales and contain many small objects, so useful answers need region-level reasoning and spatial grounding, not just a whole-image caption.

## Approach
GeoChat adapts the LLaVA-1.5 design (CLIP ViT-L/14 vision tower, Vicuna-v1.5 language model) to remote sensing. It supports image-level questions, region-specific dialogue (the user passes a box as input) and grounded answers where the model emits bounding box coordinates for objects it mentions. Task tokens steer the model between modes, and positional encodings are interpolated so instruction tuning can run at 504x504 instead of 336x336.

## Data and benchmarks
The authors build a multimodal instruction-following set from existing RS image-text and detection datasets: about 318k instruction pairs (roughly 306k train, 12k test). Evaluation covers scene classification (UCMerced, AID), VQA (RSVQA-LRBEN), region captioning, grounded conversation and referring detection.

## Key results
From the paper PDF: zero-shot scene classification of 84.43% on UCMerced and 72.03% on AID, and 90.70% average accuracy on RSVQA-LRBEN. Referring detection is weak: 10.6% accuracy at IoU 0.5 overall.

## Limitations
Grounding is the clear weak spot: small-object accuracy at IoU 0.5 is reported around 2.9% versus 21.7% for large objects, and multi-object grounding drops to about 4.3%. Training data is RGB optical only (no SAR, no multispectral, no time series). Interpolated positional encoding is a workaround for, not a solution to, very large tiles. The model gives no calibrated confidence and no built-in abstention.

## What it means for SatClip
- Treat GeoChat as the baseline "RS chat" reference: its 7B LLaVA stack is too heavy for our CPU prototype, but its task-token idea (separate modes for classify, caption, VQA, ground) maps cleanly onto our query router.
- Do not rely on VLM-emitted boxes for object detection: its grounding numbers are low, so pair the language layer with a dedicated detector and report detector confidence.
- RGB only means it cannot serve monsoon-season flood queries; SatClip must keep a Sentinel-1 path that does not depend on this model family.
- Its instruction-pair recipe (convert existing labelled datasets into templated Q and A) is a cheap template for our planned LoRA fine-tune data.
- Benchmark against its UCMerced/AID zero-shot numbers when reporting RemoteCLIP scene classification, so judges can compare like for like.
