---
id: 202
title: "SHRUG-FM: Reliability-Aware Foundation Models for Earth Observation"
authors: "Maria Gonzalez-Calabuig, Kai-Hendrik Cohrs, Vishal Nedungadi, Zuzanna Osika, Ruben Cartuyvels, Steffen Knoblauch, Joppe Massant, Shruti Nath, Patrick Ebel, Vasileios Sitokonstantinou"
year: 2026
venue: "CVPR 2026 EarthVision workshop proceedings (per arXiv comment); arXiv:2511.10370 (v1 November 2025, v2 April 2026)"
link: https://arxiv.org/abs/2511.10370
code: "https://github.com/vishalned/SHRUG-FM (stated in the paper; repository contents not inspected)"
category: trust-calibration
era: recent
tags: [selective-prediction, abstention, ood-detection, geospatial-foundation-model, flood-mapping, worldfloods, risk-coverage, decision-tree, ssl4eo-s12, sentinel-2]
verified: "2026-10-09 via curl to https://export.arxiv.org/api/query?id_list=2511.10370 (title, authors, dates, EarthVision 2026 comment, abstract), WebFetch of https://arxiv.org/html/2511.10370v2 (signals, datasets, failure thresholds, metrics, key numbers, binary accept/reject output) and curl of the same HTML page (Limitations and Conclusions sections, dataset split sizes)"
takeaway: "Abstention for EO segmentation that fuses input-space OOD (terrain and hydro attributes vs pretraining data), embedding OOD and ensemble uncertainty in a depth-3 decision tree; it cuts risk on kept flood and burn-scar tiles but outputs a binary keep/abstain, not a calibrated probability; the closest prior art for SatClip's abstain step"
---

# Gonzalez-Calabuig et al. 2026, SHRUG-FM

## Problem
Geospatial foundation models fail quietly in places unlike their pretraining data. For rapid mapping (floods, burn scars, landslides) users need the model to say when not to trust a prediction.

## Approach
- Three reliability signals per image tile:
  - Input-level OOD: percentile ranks of physical attributes (HydroATLAS land-cover and hydrology attributes, Copernicus DEM elevation and slope) relative to the pretraining set, plus a density estimate of pretraining locations.
  - Embedding-level OOD: distances to 64 k-means prototypes of pretraining embeddings.
  - Task uncertainty: ensemble mutual information and entropy averaged over the tile.
- A shallow decision tree (max depth 3) on about seven selected features maps the signals to accept or reject.
- Failure is defined per task as F1 below a cutoff (0.6 for burn scars and floods, 0.5 for landslides).
- Backbone: a ViT-S/16 pretrained with MoCo on SSL4EO-S12 (Sentinel-1 and Sentinel-2), with a CNN decoder.

## Data and benchmarks
- Burn scars: ExEBench (HLS imagery over the US, 2018 to 2021).
- Floods: WorldFloods (509 Sentinel-2 L1C flood scenes 2016 to 2019, tiled to about 39k train and 1.9k test patches).
- Landslides: an event reference set of 28 global events (very small, 68 test patches).
- Metrics: risk-coverage curves and AURC, discard-performance curves, Risk at fixed coverage; averaged over many seeds.

## Key results
- Burn scars: Risk@0.5 of 0.090 vs 0.137 for the best single signal (mutual information).
- Floods: lowest AURC of 0.115 among compared scores.
- Ablation: removing the uncertainty signals sharply degrades flood failure detection, while input-space features alone help less than expected (the authors call this an input paradox).
- The tree gives readable thresholds, which the authors present as interpretable abstention.

## Limitations
- Output is binary accept or reject; the authors state the uncertainty scores are relative signals and not calibrated, so there is no probability to show a user.
- Needs access to the foundation model's pretraining data distribution, which many model providers do not release.
- Failure definitions, feature choice and tree settings are task-specific and sensitive in low-data settings; the authors note periodic recalibration may be needed under shift.
- Flood evaluation is optical Sentinel-2 only, not SAR, and tile-level rather than per-question.

## What it means for SatClip
- Adopt: the idea of an input-space OOD check using physical attributes. SatClip can flag districts or dates whose terrain, slope, or backscatter statistics fall outside the range where the Otsu threshold was validated, and feed that into abstention.
- Adopt: risk-coverage curves and AURC as the evaluation format for SatClip's abstain-below-threshold rule.
- Beat: SatClip should map its signals to a calibrated probability (entries 26, 126, 127) rather than a bare keep/reject, and show that number with the scene receipt.
- Novelty: weakens the claim modestly. It shows abstention for EO flood mapping is already published (CVPR EarthVision 2026), so SatClip cannot claim abstention for satellite flood products as new. It does not provide calibrated confidence, a question interface, scene receipts, live retrieval or SAR fallback, so the combination claim survives; SatClip should cite it as the nearest abstention prior art.
