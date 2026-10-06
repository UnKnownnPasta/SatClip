---
id: 120
title: "PANGAEA: A Global and Inclusive Benchmark for Geospatial Foundation Models"
authors: "Valerio Marsocci, Yuru Jia, Georges Le Bellier, David Kerekes, Liang Zeng, et al. (15 authors, incl. Nicolas Audebert, Andrea Nascetti)"
year: 2024
venue: "arXiv preprint 2412.04204; published as PANGAEA: Assessing Geospatial Foundation Models Capabilities through a Global and Inclusive Benchmark, IEEE Geoscience and Remote Sensing Magazine, 14(1): 245-285 (2026)"
link: https://arxiv.org/abs/2412.04204
code: https://github.com/VMarsocci/pangaea-bench
category: rs-benchmark
era: recent
tags: [foundation-models, benchmark, sen1floods11, change-detection, sar, geographic-bias, limited-labels]
verified: "2026-10-06 via https://arxiv.org/abs/2412.04204, https://arxiv.org/html/2412.04204 (v2), Crossref record for 10.1109/mgrs.2025.3628194 and https://raw.githubusercontent.com/VMarsocci/pangaea-bench/main/README.md; journal title differs from arXiv title as shown"
takeaway: "On Sen1Floods11 a plain supervised UNet beats every geospatial foundation model and RemoteCLIP reaches only about 55 water IoU, so SatClip should keep classical SAR thresholding as its water instrument and not swap in a foundation model or RemoteCLIP for flood extent"
---

# PANGAEA

## Problem
Geospatial foundation models (GFMs) were evaluated on easy or narrow tasks, with little variety in resolution, sensor and time, and with datasets biased toward Europe and North America. It was unclear whether GFMs beat ordinary supervised models in realistic settings.

## Approach
- A standard, extensible protocol that runs many GFMs with the same decoders and training recipes across segmentation, change detection and regression.
- Compares GFMs (CROMA, DOFA, Prithvi, RemoteCLIP, SatlasNet, Scale-MAE, SpectralGPT, SSL4EO-S12 variants, GFM-Swin) with supervised UNet and ViT baselines.
- Tests full labels and reduced labels (50% and 10%), multi-temporal aggregation, domain adaptation and hyperparameter sensitivity.

## Data and benchmarks
- Datasets include HLS Burn Scars, MADOS, PASTIS-R, Sen1Floods11, xView2, Five Billion Pixels, DynamicEarthNet, Crop Type Mapping South Sudan, SpaceNet 7, AI4SmallFarms and BioMassters; GEO-Bench tasks were integrated later (README, June 2025).
- Sensors span Sentinel-1, Sentinel-2, HLS, Planet, Gaofen-2 and Maxar; the authors note that Asia is covered by only about 10% of public EO datasets.
- A public leaderboard and the TerraMind evaluation use this benchmark (README).

## Key results
- With full labels, supervised baselines, especially UNet, beat most GFMs; with 10% labels some GFMs such as CROMA come out ahead.
- On Sen1Floods11 (100% labels): UNet 91.42 mIoU and 85.05 water IoU; CROMA 90.89 and 84.15; Prithvi 90.37 and 83.26; RemoteCLIP 74.26 and 55.18.
- UNet stays best on Sen1Floods11 even at 10% labels (88.55 mIoU); the authors say pre-training brings little for this simple two-class task.
- On high-resolution data, most GFMs pre-trained on coarser imagery fall behind, except CROMA and DOFA.

## Limitations
- Mostly pixel-level tasks; no language, no question answering, no calibration or abstention metrics.
- Results depend on the chosen decoder and recipe; the authors include a hyperparameter sensitivity study but it cannot cover every setup.
- India-specific coverage is thin (AI4SmallFarms is Southeast Asia, Five Billion Pixels is China).

## What it means for SatClip
- Keep Kittler-Illingworth SAR thresholding (and a small supervised check such as a UNet trained on Sen1Floods11) as the water instrument; this paper shows big pretrained models do not beat that baseline for flood water.
- RemoteCLIP's weak water IoU here is a warning: use it only as a coarse land-cover sanity check on the evidence card, never as the source of a flooded-area number, and report its confidence separately.
- Reuse PANGAEA's harness to test any future encoder on Indian tiles before adoption, and add an India split to its geographic-bias analysis as a SatClip contribution.
