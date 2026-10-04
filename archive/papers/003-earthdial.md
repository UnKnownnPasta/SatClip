---
id: 003
title: "EarthDial: Turning Multi-sensory Earth Observations to Interactive Dialogues"
authors: "Sagar Soni, Akshay Dudhane, Hiyam Debary et al."
year: 2025
venue: "CVPR 2025"
link: https://arxiv.org/abs/2412.15190
code: https://github.com/hiyamdebary/EarthDial
category: rs-vlm
era: recent
tags: [vlm, sentinel-1, sentinel-2, sar, multispectral, multi-temporal, change-detection, internvl2, small-model]
verified: "2026-10-04 via https://arxiv.org/abs/2412.15190 and https://github.com/hiyamdebary/EarthDial"
takeaway: "Closest prior work (4B, open weights, Sentinel-1 VH plus S2 plus change); top LoRA base candidate, and SatClip must beat it on provenance, calibration and abstention"
---

# EarthDial: Turning Multi-sensory Earth Observations to Interactive Dialogues

## Problem
Earth observation analysis for disaster response and resource management needs conversational models that handle more than RGB: multispectral, SAR, multi-temporal and multi-resolution imagery. Existing RS assistants were mostly single-sensor and single-date.

## Approach
EarthDial is a 4B-parameter assistant built on InternVL2 with a Phi-3 Mini language model. It is trained in stages, with later stages adding multispectral, SAR and temporal inputs so one dialogue model covers classification, detection, captioning, VQA, visual reasoning, grounding and change description. Separate checkpoints are released (RGB, multispectral, and a methane / urban heat island variant).

## Data and benchmarks
The instruction set holds about 11.11M pairs across RGB, Sentinel-2, SAR, near-infrared and infrared. The PDF lists roughly 1.67M Sentinel-1 VH image-text pairs, about 64.6k bi-temporal change-detection pairs, and about 37.6k temporal disaster-assessment pairs. Evaluation spans 44 downstream datasets.

## Key results
Reported in the PDF: scene classification of 88.76% on AID and 92.42% on UCMerced (GeoChat: 72.03% and 84.43%), and 68.82% on BigEarthNet. On SAR ship detection it reports mAP@0.5 of about 12 (small), 26 (medium) and 36 (large) versus near zero for GPT-4o. Change captioning ROUGE-1 is around 32 to 34 versus 14 to 17 for GeoChat.

## Limitations
The appendix shows failures in ambiguous scenes, rare object types and subtle temporal changes. Detection mAP on small SAR targets remains low in absolute terms. Outputs are text and boxes without calibrated confidence or an abstention rule. At 4B parameters, CPU inference is possible but slow.

## What it means for SatClip
- This is the closest prior work to SatClip's scope (Sentinel-1 plus Sentinel-2, change detection, disaster use): position SatClip against it explicitly and cite it.
- Strong candidate base for our LoRA fine-tune: open weights, 4B size, already seen Sentinel-1 VH tokens; test a quantized build on our CPU target before committing.
- Adopt its idea of sensor-specific input tokens so the model knows whether it is reading VH SAR or optical bands.
- Beat it on trust, not accuracy: add scene ID, date, region mask, calibrated confidence and abstention, none of which it provides.
- Its disaster-assessment and change pairs are a useful seed set for flood and crop-damage queries; verify license and Indian coverage.
