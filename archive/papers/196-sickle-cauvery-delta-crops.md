---
id: 196
title: "SICKLE: A Multi-Sensor Satellite Imagery Dataset Annotated with Multiple Key Cropping Parameters"
authors: "Depanshu Sani, Sandeep Mahato, Sourabh Saini, Harsh Kumar Agarwal, Charu Chandra Devshali, Saket Anand, Gaurav Arora, Thiagarajan Jayaraman"
year: 2024
venue: "2024 IEEE/CVF Winter Conference on Applications of Computer Vision (WACV 2024), pp. 5983-5992, DOI 10.1109/WACV57701.2024.00589 (oral); arXiv:2312.00069"
link: https://arxiv.org/abs/2312.00069
code: "Project page https://sites.google.com/iiitd.ac.in/sickle/home (named in the paper; download terms not checked)"
category: indian-context
era: recent
tags: [india, tamil-nadu, cauvery-delta, paddy, crop-type, phenology, yield, sentinel-1, sentinel-2, landsat-8, smallholder, ground-survey, dataset]
verified: "2026-10-08 via curl to https://export.arxiv.org/api/query (title, authors, abstract, WACV comment), curl to https://api.crossref.org (WACV DOI and pages) and curl to https://arxiv.org/html/2312.00069v1 (challenges section, project URL); WebFetch permission request timed out; per-task benchmark numbers sit in a table that did not extract cleanly and are not quoted"
takeaway: "A ground-surveyed Indian smallholder paddy dataset (388 plots, 4 Cauvery Delta districts, Sentinel-1, Sentinel-2 and Landsat-8, 2018 to 2021) with sowing, transplanting and harvest dates; SatClip can use it as a held-out Indian set to calibrate and test crop-change answers, treating labels as noisy as the authors advise"
---

# Sani et al. 2024, SICKLE (Cauvery Delta, Tamil Nadu)

## Problem
Labelled crop datasets are plentiful in Europe and scarce in South Asia. Indian paddy is grown in the monsoon, so optical-only datasets that drop cloudy scenes miss the seasons that matter, and smallholder plots are smaller than most label grids.

## Approach
- Field surveys (with the MS Swaminathan Research Foundation) of plots in the Cauvery Delta, Tamil Nadu, mainly paddy farmers.
- Time series from Landsat-8 (multispectral and thermal), Sentinel-2 and Sentinel-1 for January 2018 to March 2021, organised by cropping season.
- Masks at 3 m, 10 m and 30 m for each plot; parameters include crop type, paddy variety, season, sowing, transplanting and harvesting dates, and yield per acre.
- Train, validation and test split chosen to minimise distribution distance between plot histograms.

## Data and benchmarks
- 2,370 season-wise samples from 388 plots (average 0.38 acre) across 4 districts; 21 crop types; about 209,000 images.
- 351 paddy samples from 145 plots carry the full parameter set.
- Benchmarks: crop-type segmentation, phenology date prediction (sowing, transplanting, harvest) and yield, run with U-Net 3D, ConvLSTM and U-TAE, per sensor and with cross-satellite fusion.

## Key results
- Establishes baselines for each task and sensor (values not extracted; see verified field).
- Authors stress that radar is needed in monsoon seasons and that fusion of sensors is required for usable systems.

## Limitations
- Labels come from ground surveys in January to March, not crop-cutting; the authors themselves say they are noisy and better treated as weak supervision.
- Many plots are under one acre, so 10 m and 30 m masks blur or merge plots and some small plots have no low-resolution mask.
- One agro-climatic region (delta paddy); not representative of rainfed or northern Indian cropping.
- Not a flood dataset.

## What it means for SatClip
- Adopt: use SICKLE as a held-out Indian test set for crop-change answers (paddy present or absent, transplanting shift) on Sentinel-1 and Sentinel-2, and to fit the calibration map for crop confidence on Indian smallholder conditions.
- Adopt: its plot-size statistics justify SatClip reporting plot-level answers only above a minimum area and abstaining below it.
- Avoid: do not treat its labels as exact truth when measuring calibration; report results with that caveat.
