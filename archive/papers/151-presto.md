---
id: 151
title: "Lightweight, Pre-trained Transformers for Remote Sensing Timeseries"
authors: "Gabriel Tseng, Ruben Cartuyvels, Ivan Zvonkov, Mirali Purohit, David Rolnick, Hannah Kerner"
year: 2023
venue: "arXiv preprint (v1 April 2023, v4 February 2024); no journal or conference listed on arXiv; peer-reviewed venue not verified"
link: https://arxiv.org/abs/2304.14065
code: "https://github.com/nasaharvest/presto (from general knowledge, not fetched)"
category: eo-foundation
era: recent
tags: [presto, pixel-timeseries, lightweight, self-supervised, sentinel-1, sentinel-2, crop-mapping, cpu-friendly, feature-extractor]
verified: "2026-10-07 via curl to https://export.arxiv.org/api/query (title, authors, dates, abstract); Crossref title search found no venue record; repo URL not fetched; no numbers quoted because the abstract gives none"
takeaway: "A small pixel-timeseries encoder that runs cheaply and feeds simple heads: the best fit among foundation models for a CPU-side crop-condition second opinion, but it outputs embeddings, not calibrated answers"
---

# Tseng et al. 2023, Presto (Pretrained Remote Sensing Transformer)

## Problem
Labels for satellite tasks are scarce, and earlier self-supervised EO models were built like image models. They ignored the time dimension (central for crop growth) and the gain from combining several complementary sensors, and they were large and costly to run.

## Approach
- Pretrains a transformer on per-pixel time series rather than image patches, combining several remote sensing inputs (the paper covers multiple sensors; the exact list was not re-checked here beyond the abstract's "many complementary sensors").
- Designed for remote sensing from the start, which lets the model be much smaller than image-based foundation models.
- Usable for fine-tuning or as a frozen feature extractor for simple downstream models such as random forests or linear heads.

## Data and benchmarks
Evaluated on a range of globally distributed remote sensing tasks, including crop-related ones. Dataset names and scores were not re-checked here.

## Key results
- Performs competitively with much larger models while needing far less compute (no figures verified here).
- Positioned explicitly for efficient deployment at scale.

## Limitations
- Pixel-level time series ignore spatial context, so object shape and neighbourhood cues are lost.
- Gives embeddings or task-head predictions, with no built-in uncertainty, provenance or abstention.
- Venue and exact benchmark numbers not verified in this pass.

## What it means for SatClip
- **Adopt as a candidate second opinion for crop condition.** A Presto embedding plus a small logistic head can run on CPU per pixel over a block, next to the NDVI-difference instrument, and disagreement between the two can lower card confidence.
- Any head on top must be calibrated (temperature or isotonic) on Indian crop labels before its probability appears on a card; raw head scores are not confidences.
- It does not threaten the novelty claim: it is a representation, not an answer, and carries no scene ID, receipt or abstention.
