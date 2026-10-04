---
id: 041
title: "Kuro Siwo: 33 billion m² under the water. A global multi-temporal satellite dataset for rapid flood mapping"
authors: "Nikolaos Ioannis Bountos, Maria Sdraka, Angelos Zavras, Andreas Karavias, Ilektra Karasante, Themistocles Herekakis, Angeliki Thanasou, Dimitrios Michail, Ioannis Papoutsis"
year: 2024
venue: "NeurIPS 2024 Datasets and Benchmarks Track (Advances in Neural Information Processing Systems, vol. 37)"
link: https://arxiv.org/abs/2311.12056
code: https://github.com/Orion-AI-Lab/KuroSiwo
category: change-detection
era: recent
tags: [sentinel-1, sar, flood, multi-temporal, pre-post-event, dataset, grd, slc, copernicus-ems, calibration, cc-by]
verified: "2026-10-04 via https://github.com/Orion-AI-Lab/KuroSiwo"
takeaway: "Expert-labelled Sentinel-1 pre/post flood set (43 events, CC BY, separates flood from permanent water); the best calibration set for SatClip's SAR flood change instrument, though Asia is underrepresented"
---

# Kuro Siwo: 33 billion m² under the water. A global multi-temporal satellite dataset for rapid flood mapping

## Problem
Deep learning for SAR flood mapping is held back by a shortage of large, carefully annotated, multi-temporal Sentinel-1 datasets. Existing rapid-mapping products are made under severe time pressure with inconsistent methods, so they are noisy as training or evaluation labels.

## Approach
The authors assemble Sentinel-1 acquisitions around 43 flood events worldwide. Each sample has two pre-event images and one post-event image in VV and VH. Starting from Copernicus Emergency Management Service (CEMS) rapid-mapping areas, a team of SAR experts re-annotated the samples by photo-interpretation into three classes: permanent water, flood, and no water. They release both GRD (processed) and SLC (raw complex) products, plus a large unlabelled SAR set for self-supervised pretraining, and benchmark segmentation and change-detection models (released weights include FloodViT and SNUNet).

## Data and benchmarks
43 flood events across Europe, the Americas, Africa, Asia and Australia, covering more than 338 billion square metres, of which about 33 billion square metres are flood or permanent water. GeoTIFFs and 224x224 patches, CC BY licence, distributed through Hugging Face. An additional benchmark of events from several continents (BlackBench) is mentioned in the arXiv summary.

## Key results
From the ar5iv version: the best model, a UNet with ResNet50 backbone, reached 80.12% F1 on the flood class, 78.24% F1 on permanent water and 76.20% mean IoU. Dedicated change-detection architectures did not beat semantic segmentation models fed with the pre- and post-event stack, and models generally did best when given all pre-event images.

## Limitations
About half of the events are in Europe, so South Asian monsoon floods (dense paddy, very large shallow floodplains) are underrepresented. A single post-event image may miss peak extent given Sentinel-1 revisit. SAR-specific failure modes remain: flooded vegetation and urban flooding (double bounce) are hard, and wind can roughen open water. Reported figures are for learned models; no threshold baseline numbers were confirmed from the sources read.

## What it means for SatClip
- Make Kuro Siwo the primary calibration set for the Sentinel-1 flood change instrument: fit the log-ratio threshold (entry 036) and the reliability curve mapping instrument posterior to calibrated confidence, using its flood class as positives and permanent water as a separate class.
- Copy its input design: use at least two pre-event scenes from the same relative orbit to build a stable dry reference (median), which both the paper's results and SAR practice favour over a single pre image.
- Its three-class labels match what SatClip must report: "newly flooded" must exclude permanent water (JRC Global Surface Water or a pre-event median), or river channels will be counted as flood.
- Hold out its Asian events (and Sen1Floods11's India chips, entry 022) as an India-proxy test split, and abstain or lower confidence in flooded-vegetation and dense-urban areas where it shows SAR fails.
