---
id: 154
title: "AnySat: One Earth Observation Model for Many Resolutions, Scales, and Modalities"
authors: "Guillaume Astruc, Nicolas Gonthier, Clement Mallet, Loic Landrieu"
year: 2025
venue: "CVPR 2025 (Crossref DOI 10.1109/cvpr52734.2025.01819); arXiv v1 December 2024"
link: https://arxiv.org/abs/2412.14123
code: "https://github.com/gastruc/AnySat (stated in the abstract; not fetched)"
category: eo-foundation
era: recent
tags: [anysat, jepa, multimodal, multi-resolution, geoplex, sar, optical, flood, burn-scar, crop-type, change-detection]
verified: "2026-10-07 via curl to https://export.arxiv.org/api/query (title, authors, abstract) and https://api.crossref.org (CVPR 2025 proceedings record); repo URL from the abstract, not fetched; no numbers quoted because the abstract gives none"
takeaway: "A single JEPA model that accepts any mix of resolutions and sensors and covers flood and crop tasks; useful as a flexible second opinion, not as the source of card numbers"
---

# Astruc et al. 2025, AnySat

## Problem
Most geospatial models expect a fixed input configuration (one sensor, one resolution, one tile size), which limits real use where available data vary.

## Approach
- A joint embedding predictive architecture (JEPA) with scale-adaptive spatial encoders, trained self-supervised on heterogeneous data.
- GeoPlex: a collection of 5 multimodal datasets with 11 distinct sensors, used to train one model on all of them at once.

## Data and benchmarks
GeoPlex test sets plus 6 external datasets covering land cover, tree species, crop type, change detection, climate type, and segmentation of flood, burn scar and deforestation.

## Key results
- State-of-the-art results on GeoPlex and the 6 external datasets after fine-tuning or probing (per the abstract; numbers not verified here).

## Limitations
- Training data are mostly European or curated datasets; transfer to Indian monsoon scenes is unknown.
- No uncertainty or abstention mechanism described in the abstract.

## What it means for SatClip
- **Adopt only as a candidate second opinion**; its main appeal is that the same weights take Sentinel-1, Sentinel-2 and higher-resolution inputs, so one model could serve both flood and crop checks.
- Test on Sen1Floods11 India tiles before trusting it; calibrate any flood head separately.
- Novelty: no threat; it is a model, not a question-to-evidence product.
