---
id: 119
title: "GEO-Bench: Toward Foundation Models for Earth Monitoring"
authors: "Alexandre Lacoste, Nils Lehmann, Pau Rodriguez, Evan David Sherwin, Hannah Kerner, et al. (17 authors, incl. Yoshua Bengio, Stefano Ermon, Xiao Xiang Zhu)"
year: 2023
venue: "Advances in Neural Information Processing Systems 36 (NeurIPS 2023)"
link: https://arxiv.org/abs/2306.03831
code: https://github.com/ServiceNow/geo-bench
category: rs-benchmark
era: recent
tags: [foundation-models, benchmark, classification, segmentation, iqm, bootstrap, sentinel-2, evaluation-protocol]
verified: "2026-10-06 via https://arxiv.org/abs/2306.03831, https://arxiv.org/html/2306.03831, Crossref record (DOI 10.52202/075280-2223, Advances in NeurIPS 36) and https://raw.githubusercontent.com/ServiceNow/geo-bench/main/README.md; that it ran in the Datasets and Benchmarks track was not confirmed on the fetched pages"
takeaway: "GEO-Bench's evaluation protocol (many seeds, interquartile mean, bootstrapped confidence intervals) is the template SatClip should follow when it reports any instrument accuracy, and its finding that RS pre-training often did not beat ImageNet weights warns against assuming a geo model is better"
---

# GEO-Bench

## Problem
Foundation models for Earth observation were being proposed with inconsistent downstream tests, making it hard to tell which pre-training actually helps. The field lacked a curated, permissively licensed suite with a sound statistical protocol.

## Approach
- Adapts existing datasets into six classification and six segmentation tasks with uniform loaders, reduced training sets and fixed splits (names prefixed "m-").
- Recommends at least 10 seeds per configuration, the interquartile mean (IQM) of normalised scores, and stratified bootstrap confidence intervals for aggregate results.
- Reports 20 baselines, including ResNets, ConvNeXt, ViT and SwinV2 with ImageNet weights, and Sentinel-2 self-supervised models (SeCo, MoCo-S2, DINO-S2).

## Data and benchmarks
- Classification: m-bigearthnet, m-so2sat (Sentinel-1 and 2), m-brick-kiln, m-forestnet (Landsat-8), m-eurosat, m-pv4ger.
- Segmentation: m-pv4ger-seg, m-chesapeake-landcover, m-cashew-plantation, m-SA-crop-type, m-nz-cattle, m-NeonTree.
- Resolutions from 0.1 m to 15 m; multispectral, SAR and hyperspectral inputs appear in some tasks.

## Key results
- With RGB only, ConvNeXt and SwinV2 lead by a large margin and beat nearly all models on nearly all datasets.
- Models pre-trained on remote sensing (MoCo-S2, SeCo-S2) did not beat their ImageNet counterparts on aggregate RGB results.
- Adding multispectral bands to RGB-pretrained models by random initialisation gave no systematic gain; Sentinel-2 self-supervised ResNet50 gave a modest gain, and ViT-S lost accuracy with multispectral input.
- For segmentation, ResNet101 with DeepLabV3 was best on aggregate but not on every dataset.

## Limitations
- Stated by the authors: no temporal fine-tuning, no fusion with text or weather, and geographic coverage that could be much wider.
- Single-image classification and segmentation only; no change detection or language tasks.
- The maintainers now recommend GEO-Bench-2 (per the README), not reviewed here.

## What it means for SatClip
- Adopt the protocol for SatClip's own accuracy numbers: repeat runs, IQM, bootstrapped intervals, and show the interval on the evidence card's calibration page rather than a single score.
- Do not assume RemoteCLIP or another RS-pretrained model beats a strong generic baseline; benchmark the land-cover check against a plain ImageNet backbone on Indian tiles before trusting it.
- m-brick-kiln and m-SA-crop-type are cheap Sentinel-2 sanity checks for SatClip's agriculture questions while Indian labelled data is scarce.
