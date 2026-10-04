---
id: 008
title: "RemoteCLIP: A Vision Language Foundation Model for Remote Sensing"
authors: "Fan Liu, Delong Chen, Zhangqingyun Guan, et al."
year: 2024
venue: "IEEE Transactions on Geoscience and Remote Sensing (TGRS), 2024"
link: https://arxiv.org/abs/2306.11029
code: https://github.com/ChenDelong1999/RemoteCLIP
category: eo-foundation
era: recent
tags: [clip, contrastive, zero-shot, retrieval, counting, foundation-model, data-scaling, remotecount]
verified: "2026-10-04 via https://arxiv.org/abs/2306.11029"
takeaway: "Default CPU zero-shot and retrieval backbone; validate on Indian Sentinel-2 and calibrate its similarity scores before abstention"
---

# RemoteCLIP: A Vision Language Foundation Model for Remote Sensing

Full author list: Fan Liu, Delong Chen, Zhangqingyun Guan, Xiaocong Zhou, Jiale Zhu, Qiaolin Ye, Liyong Fu, Jun Zhou.

## Problem
Self-supervised and masked-image-modelling foundation models for remote sensing learn mostly low-level features, need labelled fine-tuning, and cannot do retrieval or zero-shot tasks because they have no language side. Paired remote sensing image-text data was also scarce.

## Approach
RemoteCLIP continues CLIP-style contrastive training on remote sensing data. To get enough pairs, the authors convert existing annotations into captions: Box-to-Caption (B2C) turns detection boxes into sentences and Mask-to-Box (M2B) turns segmentation masks into boxes first. UAV imagery is added too.

## Data and benchmarks
- The resulting pretraining set is described as 12 times larger than all previously available datasets combined.
- Evaluated on 16 datasets, including a new RemoteCount benchmark for object counting.
- Tasks: zero-shot classification, linear probing, k-NN, few-shot, image-text retrieval and counting.

## Key results
From the abstract:
- Consistently beats baseline foundation models across model scales.
- Retrieval: plus 9.14% mean recall over prior state of the art on RSITMD and plus 8.92% on RSICD.
- Zero-shot classification: up to 6.39% higher average accuracy than CLIP across 12 downstream datasets.

## Limitations
- Captions generated from boxes and masks are templated, so the text side is narrow (object lists rather than rich descriptions).
- Training sources are high-resolution RGB aerial/UAV; behaviour on 10 m Sentinel-2 and on SAR is not established.
- RGB only; no use of multispectral bands.
- Contrastive scores are not calibrated probabilities.

## What it means for SatClip
- Keep RemoteCLIP as the CPU retrieval and zero-shot backbone (ViT-B/32 is feasible on CPU); it is the baseline every other component must beat.
- Run a small zero-shot evaluation on Indian Sentinel-2 RGB composites before trusting its prompts, since its training resolution differs.
- Copy the B2C/M2B idea to turn Indian labelled data (for example land-cover or flood masks) into captions for our own fine-tune.
- Add temperature scaling or conformal calibration on top of raw similarity scores to drive the abstain threshold.
- Do not feed it SAR directly; route Sentinel-1 through a separate model or rule-based path.
