---
id: 097
title: "TerraMind: Large-Scale Generative Multimodality for Earth Observation"
authors: "Johannes Jakubik, Felix Yang, Benedikt Blumenstiel, Erik Scheurer, Rocco Sedona, Stefano Maurogiovanni, Jente Bosmans, Nikolaos Dionelis, Valerio Marsocci, Niklas Kopp, Rahul Ramachandran, Paolo Fraccaro, Thomas Brunschwiler, Gabriele Cavallaro, Juan Bernabe-Moreno, Nicolas Longépé (IBM Research, ESA, Forschungszentrum Jülich and others)"
year: 2025
venue: "ICCV 2025 (arXiv:2504.11171, v1 15 April 2025, latest v5 June 2026)"
link: https://arxiv.org/abs/2504.11171
code: https://github.com/IBM/terramind
category: upcoming
era: recent
tags: [foundation-model, generative, any-to-any, sentinel-1, sentinel-2, terratorch, flood-mapping, ibm, esa, open-weights]
verified: "2026-10-05 via https://arxiv.org/abs/2504.11171, https://arxiv.org/html/2504.11171v1, https://huggingface.co/ibm-esa-geospatial/TerraMind-1.0-base, ICCV 2025 open access listing (search result)"
takeaway: "Open Apache-2.0 any-to-any model over Sentinel-1/2, DEM, LULC and NDVI with strong water mapping; a candidate fine-tuned instrument or cross-check for SatClip, but its generated 'imagined' modalities must never feed evidence-card numbers"
---

# TerraMind: Large-Scale Generative Multimodality for Earth Observation

## Problem
Earth observation foundation models were mostly encoders for one or two modalities. They could not translate between modalities (for example SAR to optical when clouds block the view) or generate missing inputs, and most were trained on limited modality sets.

## Approach
TerraMind is a dual-scale, any-to-any generative transformer that works on both token-level and pixel-level representations of each modality. It can take any subset of modalities as input and generate others. "Thinking in Modalities" (TiM) is a chain-of-thought analogue: the model first generates an intermediate modality (for example a land-cover map) and then uses it to improve the final output during fine-tuning or inference.

## Data and benchmarks
- Pretrained on TerraMesh: about 9 million spatiotemporally aligned global samples over nine modalities, including Sentinel-1 (GRD and RTC), Sentinel-2 (L1C and L2A), RGB, DEM, land use and land cover, NDVI, geographic coordinates and synthetic captions. The model card cites about 500 billion tokens.
- Evaluated on the PANGAEA benchmark plus zero-shot tasks (water mapping, land-use segmentation, geolocation).

## Key results
As reported:
- TerraMind v1-B about 58.35 mean mIoU on PANGAEA, ahead of the 12 compared geospatial models.
- Water body mapping around 84.75 IoU with TiM; TiM adds up to about 2 percentage points mIoU on flood detection.
- Base model training took 12 days on 32 A100 GPUs.
- Weights, code and pretraining data released under a permissive license (Apache 2.0 on Hugging Face), integrated into the TerraTorch fine-tuning library.

## Limitations
- GPU-heavy to train and fine-tune; CPU inference cost at district scale not reported.
- Generated modalities (for example synthetic optical from SAR) look plausible but are not measurements; they can hallucinate structure.
- Benchmarks are mostly global or European; Indian monsoon paddy and flooded vegetation are not specifically evaluated.
- Not a question-answering or explanation system.

## What it means for SatClip
- Threat level: low to medium. It is a model, not an evidence-card product, but IBM/ESA could add an LLM front end (as with Prithvi, entry 052).
- Adopt: a fine-tuned TerraMind (tiny or base) via TerraTorch is a credible second opinion for SAR water masks; disagreement between our threshold instrument and TerraMind could lower confidence or trigger abstention.
- Avoid: using TiM or SAR-to-optical generation to "fill in" cloudy Sentinel-2 scenes for NDVI. Synthetic pixels are not evidence, and a receipt that cites a generated image would mislead officials.
- Beat: transparency and cost. SatClip's headline numbers come from simple, explainable instruments with scene IDs; TerraMind is an optional learned check, clearly labelled as such on the card.
