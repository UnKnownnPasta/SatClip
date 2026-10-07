---
id: 173
title: "GEOID-Flood: A Large-Scale Multi-Modal Benchmark Dataset for Flood Segmentation"
authors: "Gaetano Chiriaco, Luca Barco, Andrea Bragagnolo, Claudio Rossi, Edoardo Arnaudo"
year: 2026
venue: "ECCV 2026 Terrabytes II Workshop (per arXiv comment); arXiv:2608.02315, v1 3 August 2026"
link: https://arxiv.org/abs/2608.02315
code: "https://github.com/links-ads/geoid-flood (dataset and code, stated in the abstract; not fetched)"
category: upcoming
era: upcoming
tags: [flood-mapping, sentinel-1, grd, rtc, sentinel-2, dem, copernicus-ems, benchmark, foundation-models, terramind, permanent-water, temporal-holdout]
verified: "2026-10-07 via curl to https://export.arxiv.org/api/query (title, authors, date, abstract, workshop comment) and curl to https://arxiv.org/html/2608.02315v1 (splits, Tables 2 to 5 text, limitations); WebFetch permission request timed out; workshop acceptance taken from the arXiv comment only"
takeaway: "A new 2026 Sentinel-1 flood benchmark with event-level splits, a temporally disjoint 2026 test set and separate permanent-water and flooded-water labels; ideal for scoring and calibrating SatClip's SAR flood instrument, though only 79 of 219 events are outside Europe"
---

# Chiriaco et al. 2026, GEOID-Flood benchmark

## Problem
Existing flood datasets rarely combine bi-temporal SAR with co-registered optical data at scale, use inconsistent SAR preprocessing, often split tiles randomly (spatial leakage) and derive permanent water from incomplete sources. This makes it hard to know whether geospatial foundation models really help flood mapping.

## Approach
- Built from Copernicus Emergency Management Service rapid-mapping activations: 219 events in 65 countries over ten years, more than 14,000 tiles.
- Each tile: pre- and post-event Sentinel-1 in both GRD and RTC form, a cloud-free pre-event Sentinel-2 composite, a DEM, and manually validated labels with three classes (background, permanent water, flooded water).
- Event-level splits stratified by continent, with touching AoIs kept in the same split: 8,938 train, 1,241 validation, 2,674 test tiles, plus a held-out set of 1,429 tiles from CEMS activations after January 2026 (EMSR857 to EMSR871, February to March 2026).

## Data and benchmarks
Encoders compared include TerraMind (T, S, B, L), other foundation models and ImageNet-pretrained CNN/Swin backbones, under single-image, bi-temporal and optical-SAR fusion settings; cross-dataset transfer compared with Kuro Siwo, MMFlood, WorldFloods v2 and Sen1Floods11, all reprocessed the same way.

## Key results
- Binary water IoU on Sentinel-1 GRD spans 0.844 to 0.884 across almost all encoders; TerraMind-L finetuned is best (IoU 0.884, F1 0.936), while a 32M Swin-T reaches 0.873.
- Flooded water is much harder: best single-image flood IoU 0.484; finetuned early fusion with optical reaches 0.521.
- GRD slightly beats RTC on pre-event water (IoU 0.931 vs 0.922); adding the DEM gives no clear gain.
- Models trained on GEOID-Flood transfer to the 2026 held-out events better than models trained on the other four datasets.

## Limitations
- Geographically skewed to Europe (140 of 219 events); South Asian monsoon floods are under-represented.
- Labels inherit noise from CEMS delineations and a model-derived permanent-water layer.
- No classical threshold baseline (for example Otsu on VV/VH) was found in the text we read, so the gain of learned models over simple instruments is not measured here.

## What it means for SatClip
- Adopt: use the test split and the post-January-2026 held-out set to score SatClip's SAR threshold instrument and to fit its calibration on events it has never seen; report flooded-water IoU separately from permanent water, as this benchmark does.
- Adopt: GRD is enough; the small RTC advantage was not found, which supports SatClip's CPU-friendly preprocessing choices, though terrain-heavy Indian districts still need checking.
- Beat: add the missing classical baseline (split-based thresholding) and an abstention-aware metric (accuracy at a given coverage), which this benchmark does not provide.
- Gap: assemble a small Indian subset (Assam, Bihar, Kerala) because the benchmark's coverage of South Asia is thin.
