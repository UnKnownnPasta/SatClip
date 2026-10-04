---
id: 056
title: "Neural Plasticity-Inspired Multimodal Foundation Model for Earth Observation"
authors: "Zhitong Xiong, Yi Wang, Fahong Zhang, Adam J. Stewart, Joëlle Hanna, Damian Borth, Ioannis Papoutsis, Bertrand Le Saux, Gustau Camps-Valls, Xiao Xiang Zhu"
year: 2024
venue: "arXiv preprint (v1 March 2024, v3 October 2025); peer-reviewed venue not confirmed"
link: https://arxiv.org/abs/2403.15356
code: https://github.com/zhu-xlab/DOFA
category: eo-foundation
era: recent
tags: [foundation-model, dofa, hypernetwork, wavelength-conditioned, multi-sensor, sar, sentinel-1, sentinel-2, hyperspectral, torchgeo]
verified: "2026-10-04 via https://arxiv.org/abs/2403.15356 and https://github.com/zhu-xlab/DOFA"
takeaway: "One encoder for any band set via wavelength conditioning (DOFA); lets SatClip use a single learned backbone for both Sentinel-1 and Sentinel-2 in experiments"
---

# Neural Plasticity-Inspired Multimodal Foundation Model for Earth Observation

Note: earlier arXiv versions (and the GitHub README) use the title "Neural Plasticity-Inspired Foundation Model for Observing the Earth Crossing Modalities". The model is called DOFA (Dynamic One-For-All).

## Problem
Each Earth observation sensor has its own band count, wavelengths and resolution, so most foundation models are tied to one sensor. Teams end up keeping separate models for SAR, multispectral and hyperspectral data.

## Approach
- A wavelength-conditioned dynamic hypernetwork generates the patch embedding weights from the central wavelength of each input band, inspired by neural plasticity.
- The rest of the network is a shared vision transformer, so any band combination maps into one representation space.
- Continual pretraining on data from five sensors.
- In code, the caller passes a list of wavelengths with the image (for example the C-band value for both Sentinel-1 channels, and per-band values for Sentinel-2).
- An optimised DOFA+ variant is described as using much less compute; we did not confirm its details.

## Data and benchmarks
- Five sensor types including SAR, multispectral, RGB and hyperspectral.
- 12 Earth observation downstream tasks (per the MCML summary of the abstract), plus generalisation to unseen sensors.
- ViT-Base weights on Hugging Face (XShadow/DOFA); code MIT licence. DOFA is also integrated in TorchGeo (we did not re-check the exact class name).

## Key results
The abstract reports top-tier results across downstream tasks and good transfer to sensors not seen in training. Specific numbers were not checked for this entry.

## Limitations
- Still a preprint as far as we could confirm.
- Single-date inputs; no explicit temporal modelling.
- ViT-B is heavy for whole-district CPU inference.
- Wavelength conditioning ignores other sensor differences (polarisation, incidence angle, processing level), so SAR inputs must be preprocessed consistently.

## What it means for SatClip
- If we add one learned backbone for experiments, DOFA is attractive because the same weights accept Sentinel-1 VV/VH and Sentinel-2 bands; this keeps the GPU pipeline simple.
- Always pass the true band wavelengths from STAC metadata, and log them in the evidence card, so runs are reproducible.
- Use DOFA features only for cross-checks and abstention signals; deterministic instruments still produce every reported number.
- Compare against CROMA (entry 055) on a small Indian flood set before choosing; prefer whichever is better calibrated after temperature scaling, not whichever scores higher raw.
