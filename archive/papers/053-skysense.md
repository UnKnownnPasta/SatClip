---
id: 053
title: "SkySense: A Multi-Modal Remote Sensing Foundation Model Towards Universal Interpretation for Earth Observation Imagery"
authors: "Xin Guo, Jiangwei Lao, Bo Dang, Yingying Zhang, Lei Yu, Lixiang Ru, Liheng Zhong, Ziyuan Huang, Kang Wu, Dingxiang Hu, Huimei He, Jian Wang, Jingdong Chen, Ming Yang, Yongjun Zhang, Yansheng Li"
year: 2024
venue: "CVPR 2024"
link: https://arxiv.org/abs/2312.10115
code: https://github.com/Jack-bo1220/SkySense
category: eo-foundation
era: recent
tags: [foundation-model, multi-modal, sar, sentinel-1, sentinel-2, worldview, contrastive, geo-context, billion-scale]
verified: "2026-10-04 via https://arxiv.org/abs/2312.10115 and https://github.com/Jack-bo1220/SkySense"
takeaway: "Billion-parameter optical plus SAR plus time model showing fusion helps; a ceiling to cite, but non-commercial weights and size rule it out for SatClip"
---

# SkySense: A Multi-Modal Remote Sensing Foundation Model Towards Universal Interpretation for Earth Observation Imagery

## Problem
Earlier remote sensing foundation models usually handle one modality (optical or SAR) and one date. Real interpretation tasks benefit from combining very high resolution optical images, multispectral time series and radar, plus knowledge of where on Earth the image is.

## Approach
- A factorised multi-modal spatiotemporal encoder: separate spatial encoders for each input type, followed by a fusion stage across modality and time.
- Inputs: WorldView optical at about 0.3 m, Sentinel-2 time series (10 bands, 10 m) and Sentinel-1 SAR (VV and VH, 10 m).
- Multi-Granularity Contrastive Learning at pixel, object and image level, in single-modal and multi-modal feature spaces.
- Geo-Context Prototype Learning: the Earth is split into 4,096 regions with learned prototypes per region to inject regional context.
- Billion-parameter scale; pretraining used 80 A100-80GB GPUs.

## Data and benchmarks
- Pretraining set: 21.5 million temporal sequences covering about 8.78 million square km across 40 countries (around 300 TB).
- Evaluation: 16 datasets over 7 tasks, including semantic segmentation, object detection, change detection, scene classification and multi-modal segmentation.

## Key results
Per the abstract, SkySense beats 18 recent remote sensing foundation models, with average gains of 2.76% over GFM, 3.67% over SatLas and 3.61% over Scale-MAE.

## Limitations
- Weights are released for non-commercial research only; commercial use needs permission from the authors.
- Far too large for CPU inference; pretraining is out of reach for a student team.
- Pretraining data is not public in full, so its coverage of India is unknown.
- WorldView imagery is commercial; SatClip only reads public Sentinel data.

## What it means for SatClip
- Cite SkySense as evidence that SAR plus optical fusion improves interpretation, which supports our design of running SAR and optical instruments side by side and reporting both in one card.
- Do not adopt it: licence and compute conflict with an open, CPU-first government tool.
- Its geo-context idea maps cheaply to our setting: attach district, season (kharif or rabi) and orbit metadata to every instrument call so explanations and thresholds can be region-aware.
- Use its reported scores only as an upper reference when pitching; our goal is calibrated, auditable answers, not leaderboard wins.
