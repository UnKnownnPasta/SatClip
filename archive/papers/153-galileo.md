---
id: 153
title: "Galileo: Learning Global & Local Features of Many Remote Sensing Modalities"
authors: "Gabriel Tseng, Anthony Fuller, Marlena Reil, Henry Herzog, Patrick Beukema, Favyen Bastani, James R. Green, Evan Shelhamer, Hannah Kerner, David Rolnick"
year: 2025
venue: "arXiv preprint (v1 February 2025, v3 June 2025); arXiv lists no venue; reported as ICML 2025 from general knowledge, not verified"
link: https://arxiv.org/abs/2502.09356
code: "https://github.com/nasaharvest/galileo (from general knowledge, not fetched)"
category: eo-foundation
era: recent
tags: [galileo, multimodal, sar, optical, elevation, weather, pixel-timeseries, masked-modeling, contrastive, flood-detection, crop-mapping]
verified: "2026-10-07 via curl to https://export.arxiv.org/api/query (title, authors, dates, abstract); Crossref search found no venue record; ICML claim and repo URL not verified"
takeaway: "One generalist encoder over optical, SAR, elevation and weather that handles both images and pixel time series and names flood detection and crop mapping as targets: the strongest learned second-opinion candidate for SatClip's two beachhead questions"
---

# Tseng et al. 2025, Galileo

## Problem
Remote sensing tasks such as crop mapping and flood detection benefit from many modalities, but objects vary hugely in scale and speed, from boats of one or two pixels to slow glaciers spanning thousands. Shared representations across these modalities and scales are hard to learn.

## Approach
- A highly multimodal transformer over multispectral optical, SAR, elevation, weather, pseudo-labels and more, across space and time.
- Self-supervised masked modelling with two contrastive losses: a global one targeting deep representations with structured masking, and a local one targeting shallow input projections with unstructured masking, to capture both large and small features.
- Flexible input set: modalities can be present or absent.

## Data and benchmarks
Eleven benchmarks spanning satellite images and pixel time series (names not re-checked here).

## Key results
- A single generalist model that outperforms specialist state-of-the-art models across the eleven benchmarks and multiple tasks (per the abstract; no numbers verified here).

## Limitations
- Larger and more complex than Presto; CPU cost for large districts was not checked.
- Gives features, not calibrated probabilities or provenance.
- Venue not verified.

## What it means for SatClip
- **Adopt for evaluation as the learned second opinion** on flood and crop questions, since it takes SAR and weather together and works when some inputs are missing (cloudy optical).
- Run it offline on a sample of calibration tiles (Sen1Floods11, Kuro Siwo) and compare against the Otsu SAR mask; use agreement only to adjust or veto confidence, never to produce the headline area.
- Check model size against the CPU budget before promising it on a district server; a smaller variant may be needed.
- Novelty: the strongest technical overlap in this batch with SatClip's beachhead, but it is a representation model with no question interface, receipt or abstention, so it does not threaten the answer-card claim.
