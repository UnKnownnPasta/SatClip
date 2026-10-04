---
id: 058
title: "SpectralGPT: Spectral Remote Sensing Foundation Model"
authors: "Danfeng Hong, Bing Zhang, Xuyang Li, Yuxuan Li, Chenyu Li, Jing Yao, Naoto Yokoya, Hao Li, Pedram Ghamisi, Xiuping Jia, Antonio Plaza, Paolo Gamba, Jon Atli Benediktsson, Jocelyn Chanussot"
year: 2024
venue: "IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI), 2024 (accepted per arXiv comment)"
link: https://arxiv.org/abs/2311.07113
code: https://github.com/danfenghong/IEEE_TPAMI_SpectralGPT
category: eo-foundation
era: recent
tags: [foundation-model, spectral, sentinel-2, 3d-transformer, masked-autoencoder, change-detection, segmentation, segmunich, bigearthnet]
verified: "2026-10-04 via https://arxiv.org/abs/2311.07113 and https://github.com/danfenghong/IEEE_TPAMI_SpectralGPT"
takeaway: "3D spatial-spectral MAE for Sentinel-2 with change detection results; reference for spectral-aware features, but GPL licence and size keep it out of SatClip core"
---

# SpectralGPT: Spectral Remote Sensing Foundation Model

## Problem
Most remote sensing foundation models treat multispectral images like RGB photos, flattening the band dimension. This loses the sequential structure of the spectrum, which is exactly what indices such as NDVI exploit.

## Approach
- A 3D generative transformer: images are cut into 3D tokens that span space and groups of spectral bands, so spatial and spectral information is modelled together.
- Multi-target reconstruction to capture spectral sequential patterns.
- Progressive training so the model handles different input sizes, resolutions and time series.
- Models exceed 600 million parameters, per the abstract.

## Data and benchmarks
- Pretraining on about one million spectral images; the repo provides checkpoints trained on fMoW-Sentinel (SpectralGPT) and continued on BigEarthNet-S2 (SpectralGPT+).
- Downstream: single-label and multi-label scene classification, semantic segmentation (including a new SegMunich dataset the authors collected) and change detection.

## Key results
The abstract reports improvements over prior foundation models on all four downstream tasks; we did not re-verify specific numbers.

## Limitations
- Optical only; no SAR.
- Over 600M parameters, impractical for CPU.
- Code is GPL-3.0, which constrains how it can be bundled with other code.
- Pretraining data (fMoW-Sentinel, BigEarthNet) is mostly outside India, especially BigEarthNet (Europe).

## What it means for SatClip
- Keep NDVI difference as the vegetation change instrument: it is transparent, CPU-cheap and explainable to an official, which a 600M parameter model is not.
- SpectralGPT shows spectral structure matters; if we fine-tune anything on Sentinel-2, feed all relevant bands rather than RGB composites.
- Avoid bundling GPL code in our core pipeline; if used, run it as a separate optional GPU service.
- Its change detection results can serve as a reference baseline when we report how our log-ratio and NDVI difference instruments compare on OSCD (entry 035).
