---
id: 052
title: "Prithvi-EO-2.0: A Versatile Multi-Temporal Foundation Model for Earth Observation Applications"
authors: "Daniela Szwarcman, Sujit Roy, Paolo Fraccaro, Þorsteinn Elí Gíslason, Benedikt Blumenstiel, Rinki Ghosal, Pedro Henrique de Oliveira, Joao Lucas de Sousa Almeida, Rocco Sedona, Yanghui Kang, Srija Chakraborty, Sizhe Wang, Carlos Gomes, Ankur Kumar, Myscon Truong, Denys Godwin, Hyunho Lee, Chia-Yu Hsu, Rohit Lal, Ata Akbari Asanjan, Besart Mujeci, Disha Shidham, Trevor Keenan, Paulo Arevalo, Wenwen Li, Hamed Alemohammad, Pontus Olofsson, Christopher Hain, Robert Kennedy, Bianca Zadrozny, David Bell, Gabriele Cavallaro, Campbell Watson, Manil Maskey, Rahul Ramachandran, Juan Bernabe Moreno"
year: 2024
venue: "arXiv preprint (December 2024); peer-reviewed venue not confirmed"
link: https://arxiv.org/abs/2412.02732
code: https://github.com/NASA-IMPACT/Prithvi-EO-2.0
category: eo-foundation
era: recent
tags: [foundation-model, masked-autoencoder, hls, landsat, sentinel-2, multi-temporal, flood-mapping, terratorch, nasa, ibm]
verified: "2026-10-04 via https://arxiv.org/abs/2412.02732 and https://github.com/NASA-IMPACT/Prithvi-EO-2.0"
takeaway: "Open NASA/IBM multi-temporal HLS model with flood and crop fine-tune recipes; best GPU candidate for a learned second opinion next to SatClip's optical instruments, not a CPU default"
---

# Prithvi-EO-2.0: A Versatile Multi-Temporal Foundation Model for Earth Observation Applications

## Problem
The first Prithvi model (NASA/IBM, 2023) showed that a masked autoencoder on Harmonized Landsat Sentinel-2 (HLS) data transfers well, but it had limited temporal handling, no location or date awareness, and a single size. Users also need practical fine-tuning tools for disaster and agriculture tasks.

## Approach
- Vision transformer masked autoencoder in two sizes: 300M (ViT-L) and 600M (ViT-H) parameters.
- 3D patch and positional embeddings so a time series of images is one input.
- Optional temporal and location embeddings (the TL variants), added to tokens with dropout so the model still works when metadata is missing.
- Released on Hugging Face with fine-tuning through IBM's TerraTorch library.

## Data and benchmarks
- Pretraining: 4.2 million global time series samples from the HLS archive at 30 m, six bands (Blue, Green, Red, NIR, SWIR1, SWIR2), four timestamps per sample, covering 2014 to 2023.
- Evaluation: GEO-Bench (12 datasets, with repeated seeds and tuning) plus downstream applications in flood mapping, wildfire scars, landslides, crop classification and biomass/ecosystem tasks.

## Key results
Per the abstract: the 600M TL model improves on the original Prithvi by 8% across a range of tasks and outperforms six other geospatial foundation models on tasks spanning 0.1 m to 15 m resolution. We did not re-verify individual flood mapping scores.

## Limitations
- Optical only (HLS); clouds during the Indian monsoon block exactly the flood scenes that matter, where Sentinel-1 SAR is needed.
- 30 m HLS inputs differ from 10 m Sentinel-2 L2A; using Sentinel-2 directly requires band matching and resampling.
- 300M to 600M parameters is slow on CPU for district-scale tiles.
- Fine-tuned heads output class scores that are not calibrated probabilities.

## What it means for SatClip
- Do not put Prithvi in the CPU prototype; keep SAR Otsu water mapping and NDVI difference as the instruments that produce the numbers.
- Offer it as an optional GPU instrument: the repo's flood and crop fine-tune configs could give a learned mask to compare against our Otsu or NDVI mask, and disagreement between the two can lower confidence or trigger abstention.
- If adopted, temperature-scale its outputs on a held-out Indian set (for example Sen1Floods11 India chips, entry 022) before any number reaches an evidence card.
- The weights are CC BY 4.0 per the paper, which is compatible with a public SIH demo; record model version and Hugging Face revision in each card.
