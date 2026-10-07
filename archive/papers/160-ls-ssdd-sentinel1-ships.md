---
id: 160
title: "LS-SSDD-v1.0: A Deep Learning Dataset Dedicated to Small Ship Detection from Large-Scale Sentinel-1 SAR Images"
authors: "Tianwen Zhang, Xiaoling Zhang, Xiao Ke, Xu Zhan, Jun Shi, Shunjun Wei, Dece Pan, Jianwei Li, Hao Su, Yue Zhou, Durga Kumar"
year: 2020
venue: "Remote Sensing (MDPI), 12(18), 2997"
link: https://doi.org/10.3390/rs12182997
code: "Not verified (dataset release described in the abstract; download location not fetched)"
category: object-detection
era: recent
tags: [sar, sentinel-1, ship-detection, small-objects, large-scene, ais, false-alarms, pure-background, dataset]
verified: "2026-10-07 via curl to api.crossref.org (title, authors, journal, volume, issue, article number, date) and api.openalex.org (abstract); not on arXiv; no accuracy numbers quoted because the abstract gives none"
takeaway: "The right benchmark if SatClip ever answers 'are there vessels here' from Sentinel-1: whole-scene, small-ship, AIS-checked labels, and an explicit focus on suppressing land false alarms"
---

# Zhang et al. 2020, LS-SSDD-v1.0 (small ships in large Sentinel-1 scenes)

## Problem
Most SAR ship datasets are small chips centred on ships, so detectors trained on them do not transfer to real use: scanning a whole Sentinel-1 scene where ships are tiny and most pixels are empty sea or land that produces false alarms.

## Approach
- Releases a dataset built from 15 large Sentinel-1 images, labelled by SAR experts with support from AIS ship-position records and Google Earth.
- Cuts each scene into sub-images (9000 in total) in a fixed way so detections can be stitched back onto the full scene.
- Proposes a Pure Background Hybrid Training mechanism that uses the many ship-free tiles to teach the detector to suppress land false alarms.

## Data and benchmarks
- 15 large-scale Sentinel-1 scenes, 9000 sub-images.
- Lists five design advantages: large backgrounds, small ships, many pure-background tiles, a fully automatic detection flow, and standardised baselines.

## Key results
- The abstract says ablations confirm the pure-background training reduces land false alarms; specific numbers were not read here.
- Supplies many standardised baselines (counts and scores not verified).

## Limitations
- Only 15 scenes, so geographic diversity is narrow; coverage of Indian coasts and rivers is not stated.
- AIS-aided labels still miss vessels without AIS, the same partial-label problem noted for xView3-SAR (entry 075).
- Ships only; no inland boats or flood-relevant objects.

## What it means for SatClip
- **Adopt as the evaluation set** for any future "vessel presence" instrument on Sentinel-1, because it matches SatClip's own sensor and whole-scene use.
- Copy the idea of training and calibrating on pure-background tiles: SatClip's abstention rule should be tuned on scenes where the true answer is "nothing here", since false alarms are what erode trust.
- **Avoid** reporting exact ship counts until a detector is calibrated on held-out scenes; a CFAR-style classical detector plus this benchmark is a CPU-friendly first step.
