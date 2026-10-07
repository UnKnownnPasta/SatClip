---
id: 155
title: "Towards a Unified Copernicus Foundation Model for Earth Vision"
authors: "Yi Wang, Zhitong Xiong, Chenying Liu, Adam J. Stewart, Thomas Dujardin, Nikolaos Ioannis Bountos, Angelos Zavras, Franziska Gerken, Ioannis Papoutsis, Laura Leal-Taixé, Xiao Xiang Zhu"
year: 2025
venue: "ICCV 2025 (accepted per arXiv comment; Crossref DOI 10.1109/iccv51701.2025.00922)"
link: https://arxiv.org/abs/2503.11849
code: "https://github.com/zhu-xlab/Copernicus-FM (stated in the abstract; not fetched)"
category: eo-foundation
era: recent
tags: [copernicus-fm, copernicus-pretrain, copernicus-bench, sentinel-1, sentinel-2, sentinel-3, sentinel-5p, hypernetwork, metadata-encoding, sar]
verified: "2026-10-07 via curl to https://export.arxiv.org/api/query (title, authors, abstract, ICCV comment) and https://api.crossref.org (ICCV 2025 proceedings record); repo URL not fetched"
takeaway: "Covers every Sentinel mission with metadata-aware encoding and ships Copernicus-Bench; a good benchmark source for SAR tasks, but too heavy and indirect to sit in SatClip's truth path"
---

# Wang et al. 2025, Copernicus-FM

## Problem
Most EO foundation models are tied to fixed spectral sensors, look only at the land surface, and ignore metadata beyond the pixels.

## Approach
- Copernicus-Pretrain: 18.7M aligned images from all major Copernicus Sentinel missions, from surface to atmosphere.
- Copernicus-FM: one model that processes any spectral or non-spectral modality using extended dynamic hypernetworks (building on DOFA, entry 056) and flexible metadata encoding.
- Copernicus-Bench: 15 hierarchical downstream tasks, from preprocessing to specialised applications, per Sentinel mission.

## Data and benchmarks
Copernicus-Bench (15 tasks); specific task names and scores not re-checked here.

## Key results
- Claimed gains in scalability, versatility and multimodal adaptability (no numbers in the abstract).
- Links EO with weather and climate data sources.

## Limitations
- Large pretraining scale; CPU inference cost not checked.
- No uncertainty or abstention.

## What it means for SatClip
- **Use the benchmark, not the model, first.** Copernicus-Bench Sentinel-1 tasks can extend SatClip's calibration and regression tests beyond Sen1Floods11 and Kuro Siwo.
- Metadata encoding (time, location, acquisition parameters) echoes SatClip's practice of keeping acquisition metadata with every answer, but here it feeds the model rather than the user.
- Novelty: no threat.
