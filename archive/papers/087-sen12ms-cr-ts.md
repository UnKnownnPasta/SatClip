---
id: 087
title: "SEN12MS-CR-TS: A Remote Sensing Data Set for Multi-modal Multi-temporal Cloud Removal"
authors: "Patrick Ebel, Yajin Xu, Michael Schmitt, Xiao Xiang Zhu"
year: 2022
venue: "IEEE Transactions on Geoscience and Remote Sensing (per the arXiv version; volume and article number not confirmed)"
link: https://arxiv.org/abs/2201.09613
code: "https://patrickTUM.github.io/cloud_removal (project page with data links, as stated in the paper)"
category: sar-optical-fusion
era: recent
tags: [cloud-removal, dataset, sentinel-1, sentinel-2, multi-temporal, time-series, s2cloudless, google-earth-engine, 3d-cnn]
verified: "2026-10-05 via https://arxiv.org/abs/2201.09613v1 and https://arxiv.org/pdf/2201.09613 (full text); holdout split record at https://mediatum.ub.tum.de/1659251"
takeaway: "A year of co-registered S1/S2 time series with real clouds: shows that several cloudy dates plus SAR beat one date, and that very cloudy (>90%) cases stay hard"
---

# SEN12MS-CR-TS: A Remote Sensing Data Set for Multi-modal Multi-temporal Cloud Removal

## Problem
Roughly half of optical satellite observations are affected by cloud or haze. Earlier cloud removal datasets, including SEN12MS-CR (archived as [[019-sen12ms-cr]]), were single-date, which ignores the fact that other dates of the same place often see through gaps.

## Approach
A dataset of co-registered Sentinel-1 and Sentinel-2 time series, plus two baselines: a sequence-to-point 3D CNN that predicts one cloud-free image from several cloudy optical and SAR dates, and a sequence-to-sequence model that reconstructs the whole cloud-free series.

## Data and benchmarks
- 53 regions of interest worldwide (40 train, 13 test), each 4000 x 4000 px (about 40 x 40 km), more than 80,000 km2 in total.
- 30 time points per region across 2018, collected with Google Earth Engine.
- About 15,578 patch-wise observations of 256 x 256 px (as reported in the full text), non-overlapping.
- Mean cloud coverage about 44% in train and 50% in test, with a standard deviation of about 42%; the cloud cover distribution is bimodal (mostly clear or mostly cloudy).
- Cloud masks from s2cloudless.

## Key results
- Sequence-to-point 3D CNN: NRMSE 0.051, PSNR 26.68 dB, SSIM 0.836 (Table I as read).
- Sequence-to-sequence reconstruction is far harder: PSNR 11.59 dB, SSIM 0.512.
- Quality falls with cloud cover; above 90% coverage PSNR drops to about 24.8 dB.
- Multi-modal and multi-temporal inputs both help over single-date or optical-only setups.

## Limitations
- One year (2018) only; no monsoon-specific stratification, and only 53 regions.
- Test regions do not overlap training regions, which is good for honesty but limits density.
- Pixel metrics (PSNR, SSIM) do not tell us whether flood or crop answers derived from the reconstruction are right.

## What it means for SatClip
- Before reaching for reconstruction, SatClip should exploit the time series: search several Sentinel-2 dates in the window and composite only s2cloudless-clear pixels, naming each contributing scene ID.
- When cloud fraction in the region mask is very high (the >90% regime where even the best models degrade), route the question to SAR instruments or abstain, never to a reconstructed optical image.
- If we ever test optical gap filling for NDVI difference, SEN12MS-CR-TS is the benchmark, and we should report error stratified by cloud fraction, as this paper does.
