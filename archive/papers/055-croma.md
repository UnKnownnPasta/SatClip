---
id: 055
title: "CROMA: Remote Sensing Representations with Contrastive Radar-Optical Masked Autoencoders"
authors: "Anthony Fuller, Koreen Millard, James R. Green"
year: 2023
venue: "NeurIPS 2023"
link: https://arxiv.org/abs/2311.00566
code: https://github.com/antofuller/CROMA
category: eo-foundation
era: recent
tags: [sar, sentinel-1, sentinel-2, contrastive, masked-autoencoder, radar-optical-fusion, alibi, ssl4eo-s12, vit]
verified: "2026-10-04 via https://arxiv.org/abs/2311.00566 and https://github.com/antofuller/CROMA"
takeaway: "MIT-licensed radar plus optical encoder trained on Sentinel-1/2; best candidate for a learned SAR feature cross-check next to SatClip's Otsu water instrument"
---

# CROMA: Remote Sensing Representations with Contrastive Radar-Optical Masked Autoencoders

## Problem
Sentinel-1 radar and Sentinel-2 optical images of the same place carry complementary information, but most self-supervised methods use one sensor. Remote sensing images are also often larger at test time than in training, which standard position embeddings handle poorly.

## Approach
- Separate encoders for masked Sentinel-1 and masked Sentinel-2 patches that are aligned in space and time.
- A cross-modal contrastive loss pulls the radar and optical representations of the same location together.
- A lightweight fusion encoder combines both and a decoder reconstructs the masked patches (MAE style).
- X-ALiBi and 2D-ALiBi attention biases replace learned position embeddings, letting models run on images up to 17.6 times larger at test time than during training (per the abstract).

## Data and benchmarks
- Pretraining: SSL4EO-S12 (entry 054), about 1 million paired Sentinel-1 GRD and Sentinel-2 L2A samples.
- Classification: BigEarthNet, fMoW-Sentinel, EuroSAT, Canadian Cropland. Segmentation: DFC2020, DW-Expert, MARIDA.
- Compared with SatMAE, DINO, MAE, I-JEPA, DeCUR and other radar-optical models.
- Base (ViT-B) and Large (ViT-L) weights on Hugging Face, MIT licence. Inputs: 2 SAR bands and 12 optical bands, default 120 by 120 pixels.

## Key results
Per the abstract, average gains over prior state of the art: classification 1.8% (fine-tuning), 2.4% (linear probing), 1.4% (nonlinear probing); kNN 3.5%; K-means 8.4%; segmentation 6.4% across benchmarks.

## Limitations
- Static images only; the authors note they did not model time series, so change requires running it twice and comparing.
- ViT-B is feasible on CPU for small tiles but slow for whole districts.
- Benchmarks are mostly Europe and North America; not tested on Indian floods or paddy.
- Features need a probe or fine-tune; outputs are not calibrated.

## What it means for SatClip
- Strongest open choice for a learned SAR plus optical second opinion: a linear probe on CROMA features for water or not-water can be compared with the SAR Otsu mask, and large disagreement can trigger abstention.
- Run CROMA-Base only on the AOI chip, not the whole scene, to keep CPU time acceptable; record chip size and model version in the card.
- Expect fusion to help when Sentinel-2 is partly cloudy, but use only Sentinel-1 for cloudy monsoon scenes and say so in the explanation.
- MIT licence makes it safe to bundle; it is a better fit than SkySense (entry 053) for a public SIH demo.
