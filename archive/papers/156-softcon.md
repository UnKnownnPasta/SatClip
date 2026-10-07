---
id: 156
title: "Multi-Label Guided Soft Contrastive Learning for Efficient Earth Observation Pretraining"
authors: "Yi Wang, Conrad M Albrecht, Xiao Xiang Zhu"
year: 2024
venue: "IEEE Transactions on Geoscience and Remote Sensing (TGRS), 2024 (accepted per arXiv comment; Crossref DOI 10.1109/tgrs.2024.3466896)"
link: https://arxiv.org/abs/2405.20462
code: "https://github.com/zhu-xlab/softcon (stated in the abstract; not fetched)"
category: eo-foundation
era: recent
tags: [softcon, soft-contrastive, dinov2, continual-pretraining, sar, multispectral, bigearthnet, resnet50, vit-s, lightweight]
verified: "2026-10-07 via curl to https://export.arxiv.org/api/query (title, authors, abstract with numbers, TGRS comment) and https://api.crossref.org (TGRS record); repo URL not fetched"
takeaway: "Small SAR and multispectral backbones (ResNet50, ViT-S) that match larger models on BigEarthNet: the most CPU-practical pretrained SAR encoder candidate for a learned land-cover or water head"
---

# Wang, Albrecht and Zhu 2024, SoftCon

## Problem
EO contrastive pretraining struggles with complex scenes that have many valid positives, and usually ignores free resources such as global land-cover products and strong natural-image models.

## Approach
- Soft contrastive learning: cross-scene similarity is supervised by multi-labels generated from land-cover products, relaxing strict one-positive matching.
- Continual pretraining from strong vision models such as DINOv2 for both multispectral and SAR imagery, with simple weight initialisation and Siamese masking, even when modalities are not aligned.

## Data and benchmarks
11 downstream tasks, including BigEarthNet with 10% labels under linear probing.

## Key results
- Significantly better than most existing models on 10 of 11 tasks.
- BigEarthNet-10% linear probing mAP: 84.8 (ResNet50) and 85.0 (ViT-S), better than most ViT-L models; ViT-B reaches 86.8 multispectral and 82.5 SAR (all from the abstract).

## Limitations
- Land-cover-derived labels inherit the errors of those products.
- BigEarthNet is European; Indian performance is unverified.
- Linear-probe mAP is not calibration; probabilities still need fitting.

## What it means for SatClip
- **Adopt as the first learned SAR encoder to try on CPU.** A ResNet50 or ViT-S SAR backbone with a linear head is cheap enough for district servers and fits the planned BigEarthNet-based scene instrument (entry 017).
- Its SAR-only result suggests a cloud-proof land-cover context line during monsoon, provided a calibration set from Indian tiles is built and the card abstains below threshold.
- Novelty: no threat.
