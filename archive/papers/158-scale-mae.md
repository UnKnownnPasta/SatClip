---
id: 158
title: "Scale-MAE: A Scale-Aware Masked Autoencoder for Multiscale Geospatial Representation Learning"
authors: "Colorado J. Reed, Ritwik Gupta, Shufan Li, Sarah Brockman, Christopher Funk, Brian Clipp, Kurt Keutzer, Salvatore Candido, Matt Uyttendaele, Trevor Darrell"
year: 2023
venue: "ICCV 2023 (per arXiv comment; Crossref DOI 10.1109/iccv51070.2023.00378)"
link: https://arxiv.org/abs/2212.14532
code: "https://github.com/bair-climate-initiative/scale-mae (from general knowledge, not fetched)"
category: eo-foundation
era: recent
tags: [scale-mae, masked-autoencoder, ground-sample-distance, multiscale, positional-encoding, vit, knn-classification, spacenet]
verified: "2026-10-07 via curl to https://export.arxiv.org/api/query (title, authors, abstract with numbers, ICCV comment) and https://api.crossref.org (ICCV 2023 record); repo URL not verified"
takeaway: "Encoding ground sample distance into positional embeddings makes features robust across resolutions; a design lesson for any SatClip learned head that mixes 10 m Sentinel with finer imagery"
---

# Reed et al. 2023, Scale-MAE

## Problem
Pretrained models are usually made scale-invariant by heavy augmentation, which throws away the known physical scale of remote sensing images.

## Approach
- Masks an image at a known scale and sets the ViT positional encoding by the ground area covered, not the pixel count.
- Decodes through a bandpass filter to reconstruct low and high frequency images at lower and higher scales, which yields multiscale representations.

## Data and benchmarks
Eight remote sensing classification datasets (kNN evaluation) and SpaceNet building segmentation transfer.

## Key results
- Average 2.4 to 5.6% kNN classification improvement over the prior state of the art across the eight datasets.
- 0.9 to 1.7 mIoU gain on SpaceNet building segmentation across evaluation scales (both from the abstract).

## Limitations
- RGB, optical-only; no SAR or time series.
- Gains are modest and measured on representation quality, not on calibrated decisions.

## What it means for SatClip
- **Learn from, do not deploy.** If SatClip ever mixes Sentinel 10 m tiles with finer imagery in one learned head, pass ground sample distance explicitly; the card should also state resolution so users know what size of feature is measurable.
- Not relevant to the flood beachhead (no SAR).
- Novelty: no threat.
