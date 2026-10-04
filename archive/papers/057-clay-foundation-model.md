---
id: 057
title: "Clay Foundation Model"
authors: "Clay Foundation Model team (project initially sponsored by Radiant Earth Foundation; now a program of Renaissance Philanthropy)"
year: 2024
venue: "Technical documentation (no peer-reviewed paper found; docs describe release v1.5)"
link: https://clay-foundation.github.io/model/
code: https://github.com/Clay-foundation/model
category: eo-foundation
era: recent
tags: [foundation-model, embeddings, masked-autoencoder, vit, sentinel-1, sentinel-2, landsat, open-source, apache-2.0, source-cooperative]
verified: "2026-10-04 via https://clay-foundation.github.io/model/ and https://clay-foundation.github.io/model/release-notes/specification.html"
takeaway: "Apache-licensed multi-sensor embedding model with precomputed embeddings; useful for similarity search and change hints in SatClip, never as the source of reported numbers"
---

# Clay Foundation Model

## Problem
Most open Earth observation models are research artefacts tied to one sensor or one task. Clay aims to be a general, openly licensed model that turns any satellite image chip into an embedding that people can use for search, classification, regression and change detection.

## Approach
- A vision transformer trained as a masked autoencoder, with a teacher component, adapted for geospatial and temporal metadata.
- Per the v1.5 specification: about 632M parameters in total (311M encoder, 15M decoder, 304M teacher), patch size 8, input size 256; the encoder is about 1.25 GB on disk.
- Inputs include band central wavelengths, ground sampling distance, latitude and longitude, and time (week and hour), so it accepts any number of bands at any size.

## Data and benchmarks
- Trained on about 70 million chips sampled globally according to land use and land cover statistics.
- Sensors listed: Sentinel-2 (10 bands), Landsat 8/9 (6 bands), Sentinel-1 (2 bands), NAIP, LINZ and MODIS.
- Training: 20 AWS g6.48xlarge machines (8 L4 GPUs each), 100 epochs.
- Precomputed embeddings are published on Source Cooperative.
- Licences: code and weights Apache-2.0, docs CC-BY, embeddings ODC-BY.

## Key results
We found no peer-reviewed benchmark paper; the docs present use cases (finding features, classification, regression, change detection) rather than a standardised leaderboard. Treat performance claims as unverified.

## Limitations
- No paper, so methods and evaluation are less scrutinised than other entries.
- The 311M encoder is slow on CPU for many chips.
- Embeddings are not interpretable and carry no calibrated meaning on their own.
- The docs we read did not state embedding dimension or Indian evaluation.

## What it means for SatClip
- Apache-2.0 makes Clay the most permissive multi-sensor option; suitable for an optional similarity search feature (for example, find chips in the district that look like this flooded field).
- Use embedding distance between two dates as a change hint that can route the question to the right instrument (log-ratio for SAR, NDVI difference for optical), but never report it as a number.
- If we check Source Cooperative embeddings for Indian coverage, they could save CPU compute entirely; we have not confirmed coverage.
- Record model version (v1.5 at time of writing) in any card that used it, since releases change.
