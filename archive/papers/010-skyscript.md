---
id: 010
title: "SkyScript: A Large and Semantically Diverse Vision-Language Dataset for Remote Sensing"
authors: "Zhecheng Wang, Rajanie Prabha, Tianyuan Huang, Jiajun Wu, Ram Rajagopal"
year: 2024
venue: "AAAI 2024 (Proceedings of the AAAI Conference on Artificial Intelligence, vol. 38, no. 6)"
link: https://arxiv.org/abs/2312.12856
code: https://github.com/wangzhecheng/SkyScript
category: rs-benchmark
era: recent
tags: [dataset, openstreetmap, clip, zero-shot, fine-grained, retrieval, google-earth-engine, skyclip]
verified: "2026-10-04 via https://arxiv.org/abs/2312.12856 and https://ojs.aaai.org/index.php/AAAI/article/view/28393"
takeaway: "Reuse the OSM-to-caption trick for Indian training pairs, watching for sparse rural OSM coverage; add SkyCLIP to the backbone bake-off"
---

# SkyScript: A Large and Semantically Diverse Vision-Language Dataset for Remote Sensing

## Problem
Remote sensing images and matching text cannot be scraped from the web at scale the way natural photos can, so there was no large, semantically varied image-text corpus for building versatile remote sensing VLMs.

## Approach
SkyScript links open, unlabelled satellite and aerial images to OpenStreetMap through geo-coordinates. OSM tags at a location become the semantic content of the caption, giving rich and diverse text without manual labelling. A CLIP model is then continually pretrained on the result (released as SkyCLIP).

## Data and benchmarks
- Paper: 2.6 million image-text pairs covering 29K distinct semantic tags.
- The GitHub README describes 5.2 million pairs in total (likely a later or fuller release; the discrepancy is noted, not resolved).
- Images are pulled from multiple Google Earth Engine collections, each identified by an alias code.
- Evaluation: zero-shot scene classification on seven benchmarks, fine-grained attribute classification and cross-modal retrieval.

## Key results
- Plus 6.2% average zero-shot scene classification accuracy over baseline models across seven benchmark datasets (abstract).
- Demonstrates zero-shot transfer to fine-grained object attributes and to retrieval (abstract, no figures given).
- README lists six released CLIP checkpoints (SkyCLIP ViT-L/14 and ViT-B/32 variants, plus a LAION-RS baseline) with top-1 zero-shot accuracy spanning roughly 49.7% to 60.7% across models and benchmarks.

## Limitations
- OSM coverage and tag density are uneven; rural India is much sparser than Europe or the US, so caption quality will drop there.
- Captions are tag lists, not natural answers.
- Mixed resolutions across sources; SAR not included.
- Absolute zero-shot accuracy is still modest (around 50% to 60%).

## What it means for SatClip
- Adopt the OSM-to-caption trick to auto-generate Indian training pairs from Sentinel-2 chips plus OSM and Bhuvan-style land-use layers.
- Add SkyCLIP (ViT-B/32, MIT licence) to the backbone bake-off alongside RemoteCLIP and GeoRSCLIP.
- Expect OSM gaps in rural districts; combine with official land-cover maps rather than relying on OSM alone.
- Modest zero-shot accuracy reinforces the need for calibrated confidence and abstention rather than always answering.
- Use its fine-grained attribute tasks as inspiration for officer-relevant attributes (irrigated vs rainfed, built-up density).
