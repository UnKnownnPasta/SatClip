---
id: 152
title: "TESSERA: Temporal Embeddings of Surface Spectra for Earth Representation and Analysis"
authors: "Zhengpeng Feng, Clement Atzberger, Sadiq Jaffer, Jovana Knezevic, Silja Sormunen, Robin Young, Madeline C. Lisaius, Markus Immitzer, Toby Jackson, James Ball, David A. Coomes, Anil Madhavapeddy, Andrew Blake, Srinivasan Keshav"
year: 2025
venue: "arXiv preprint (v1 June 2025, v7 April 2026); no journal or conference listed on arXiv; peer-reviewed venue not verified"
link: https://arxiv.org/abs/2506.20380
code: "https://github.com/ucam-eo/tessera (stated in the abstract; not fetched)"
category: eo-foundation
era: recent
tags: [tessera, pixel-timeseries, embeddings, sentinel-1, sentinel-2, barlow-twins, int8, precomputed-embeddings, label-efficient, cpu-friendly]
verified: "2026-10-07 via curl to https://export.arxiv.org/api/query (title, authors, dates, abstract); Crossref lists only blog-style DOIs, no venue; repo URL from the abstract, not fetched; no accuracy numbers quoted because the abstract gives none"
takeaway: "Open, global, annual 10 m int8 Sentinel-1/2 embeddings with small heads: a cheap offline input for crop and land-cover second opinions, but annual granularity cannot answer dated flood questions"
---

# Feng et al. 2025, TESSERA pixel-wise S1/S2 embeddings

## Problem
Optical and radar time series are irregular because of orbits and clouds. Compositing fills gaps but throws away phenology, which matters for crop and vegetation tasks.

## Approach
- A pixel-wise foundation model over multi-modal Sentinel-1 and Sentinel-2 time series.
- Trained with Barlow Twins and sparse random temporal sampling, so the embedding is invariant to which valid observations happen to be available.
- Two regularisers: global shuffling to decorrelate spatial neighbours, and mix-based regularisation for robustness under extreme sparsity.
- Releases global, annual, 10 m, pixel-wise int8 embeddings with open weights, code and lightweight adaptation heads.

## Data and benchmarks
Classification, segmentation and regression tasks (details not re-checked here).

## Key results
- Reported state-of-the-art accuracy with high label efficiency, often needing only a small head and little compute (no figures verified here).
- The precomputed int8 product is the practical contribution: users can download embeddings instead of running the encoder.

## Limitations
- Annual embeddings summarise a year; they cannot say what changed between two dates within a monsoon.
- Embeddings are opaque: an official cannot inspect why a pixel looks like cropland.
- Not peer-reviewed as far as verified.

## What it means for SatClip
- **Adopt selectively.** For India tiles, precomputed int8 embeddings plus a tiny head are a CPU-cheap scene or land-cover instrument (a better candidate than RemoteCLIP zero-shot, which abstained on Darbhanga cropland), provided the head is calibrated on Indian labels.
- Because SAR is inside the embedding, it is cloud-robust for annual land cover, which suits the "what is this land" context line on a card.
- **Avoid** for flood change: the annual product cannot carry a scene ID and acquisition date per answer, so it cannot back an evidence card's headline number. Keep the S1 log-ratio instrument for that.
- Novelty: an embedding product, not an answer card; no threat.
