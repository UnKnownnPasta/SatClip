---
id: 157
title: "SatlasPretrain: A Large-Scale Dataset for Remote Sensing Image Understanding"
authors: "Favyen Bastani, Piper Wolters, Ritwik Gupta, Joe Ferdinando, Aniruddha Kembhavi"
year: 2023
venue: "ICCV 2023 (per arXiv comment; Crossref DOI 10.1109/iccv51070.2023.01538)"
link: https://arxiv.org/abs/2211.15660
code: "https://satlas-pretrain.allen.ai/ (dataset, weights and code page stated in the abstract; not fetched)"
category: eo-foundation
era: recent
tags: [satlaspretrain, satlas, sentinel-2, naip, large-scale-labels, supervised-pretraining, multi-task, allen-ai]
verified: "2026-10-07 via curl to https://export.arxiv.org/api/query (title, authors, abstract with numbers, ICCV comment) and https://api.crossref.org (ICCV 2023 record); project page not fetched"
takeaway: "Supervised multi-task pretraining on 302M labels gives strong Sentinel-2 backbones; useful for optical land-cover and structure instruments, but optical-only and US-heavy at high resolution"
---

# Bastani et al. 2023, SatlasPretrain

## Problem
Remote sensing tasks are extremely varied and features range from kilometres to centimetres, but no dataset was large in both breadth and scale to pretrain general models.

## Approach
- A dataset combining Sentinel-2 and NAIP imagery with 302M labels across 137 categories and seven label types.
- Evaluates eight baselines plus a proposed multi-task method, and releases pretrained weights.

## Data and benchmarks
SatlasPretrain itself plus downstream transfer tasks.

## Key results
- Pretraining on SatlasPretrain raises average downstream accuracy by 18% over ImageNet and 6% over the next best baseline (from the abstract).
- Highlights open challenges: mixed-sensor time series and long-range spatial context.

## Limitations
- No SAR in the core dataset, so it does not help during monsoon cloud.
- NAIP is US-only; label sources are skewed to regions with open map data.

## What it means for SatClip
- **Adopt for dry-season optical instruments** (built-up growth, large structures) as a pretrained Sentinel-2 backbone, with Indian calibration before any card use.
- **Avoid for the flood beachhead**: optical-only.
- Novelty: no threat.
