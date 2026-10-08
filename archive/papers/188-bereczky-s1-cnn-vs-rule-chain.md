---
id: 188
title: "Sentinel-1-Based Water and Flood Mapping: Benchmarking Convolutional Neural Networks Against an Operational Rule-Based Processing Chain"
authors: "Max Bereczky, Marc Wieland, Christian Krullikowski, Sandro Martinis, Simon Plank"
year: 2022
venue: "IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing, 15, 2023-2036"
link: https://doi.org/10.1109/JSTARS.2022.3152127
code: "Not verified (no repository found in the sources read)"
category: sar-optical-fusion
era: recent
tags: [sentinel-1, flood-mapping, water-mapping, cnn, u-net, deeplabv3plus, vv-vh, dual-polarisation, rule-based-baseline, s-1fs, dlr, sen1floods11, augmentation]
verified: "2026-10-08 via curl to api.crossref.org (title, five authors, volume 15, pages 2023-2036, 2022) and api.openalex.org (abstract); WebFetch permission prompt timed out so curl was used; numbers below are from the abstract only"
takeaway: "A dual-polarised (VV+VH) CNN beat DLR's operational Sentinel-1 rule chain by about 5 IoU points, and geometric augmentation hurt; SatClip should keep VH in its SAR water inputs and benchmark any learned model against its own threshold baseline"
---

# Bereczky et al. 2022, CNNs versus an operational Sentinel-1 flood chain

## Problem
Operational services such as DLR's Sentinel-1 Flood Service (the chain described in entry 083) use thresholds plus fuzzy rules. Do CNNs actually beat them on a fair, global test, and which design choices matter?

## Approach
- Compares AlbuNet-34, FCN, DeepLabV3+, U-Net and U-Net++ on Sentinel-1 amplitude against the rule-based S-1FS processor.
- Ground truth water masks come from near-coincident Sentinel-2 data over a globally distributed set of scenes.
- Tests single versus dual polarisation, weighted cross entropy plus Lovasz loss, and geometric versus radiometric augmentation.
- Generalisation check on two extra flood events and on Sen1Floods11 (entry 022).

## Data and benchmarks
- Global Sentinel-1 scenes with Sentinel-2 derived water labels; two independent flood events; Sen1Floods11.

## Key results
(From the abstract.)
- Dual-polarisation model beat S-1FS by about 5% IoU; adding Lovasz loss gave about 2% more.
- Geometric augmentation lowered performance; radiometric augmentation helped.
- Architectures performed about the same as AlbuNet-34.
- Models trained on scenes without visible floods still reached IoU 0.96 and 0.94 on two flood events, and did comparatively well on Sen1Floods11.

## Limitations
- Labels from Sentinel-2 restrict training to cloud-free moments and timing gaps can mislabel moving water.
- Gains are averaged; no per-pixel uncertainty or calibration is reported in the abstract.
- No Indian monsoon events named in the abstract.

## What it means for SatClip
- Adopt: keep both VV and VH as instrument inputs; the dual-polarisation gain is the clearest single lever.
- Adopt: avoid flip and rotate augmentation if SatClip ever fine-tunes a SAR water model, since SAR geometry (look direction, layover) is not rotation invariant.
- Beat: a learned model is only worth adding if it beats SatClip's Otsu plus terrain-mask chain on Indian chips; keep the rule chain as the default, transparent baseline.
