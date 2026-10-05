---
id: 085
title: "A fully automated TerraSAR-X based flood service"
authors: "Sandro Martinis, Jens Kersten, André Twele"
year: 2015
venue: "ISPRS Journal of Photogrammetry and Remote Sensing 104, pp. 203-212"
link: https://doi.org/10.1016/j.isprsjprs.2014.07.014
code: none found
category: sar-optical-fusion
era: historical
tags: [flood-mapping, terrasar-x, automatic-thresholding, hierarchical-tiling, fuzzy-logic, operational-service, global-validation, thailand]
verified: "2026-10-05 via https://elib.dlr.de/96684 (bibliographic record and abstract); algorithm parameters cross-checked against https://extwiki.eodc.eu/GFM/PDD/GFM_algorithms/DLR_algo, which cites this paper; publisher full text not read (paywalled)"
takeaway: "Proof that unsupervised tile thresholding plus fuzzy refinement survives 175 real flood scenes worldwide, including tropical Thailand; the robustness tricks matter more than the threshold rule"
---

# A fully automated TerraSAR-X based flood service

## Problem
Earlier DLR flood mapping (see [[084-martinis-split-based-thresholding]]) worked well on curated scenes but needed robustness to varied terrain, sensors and acquisition modes before it could run unattended as a service.

## Approach
An end-to-end chain triggered when TerraSAR-X data arrive: SAR pre-processing, automatic computation and adaptation of global auxiliary data, unsupervised classification initialisation, and post-classification refinement with fuzzy logic, then online map delivery. The abstract describes it at this level only.

Per the GFM algorithm documentation that cites this paper as the initial description, the initialisation is a hierarchical tile scheme (parent tiles split into four children, selection by darker-than-mean and high spread of child means) with Kittler-Illingworth thresholding, and the refinement uses fuzzy memberships on backscatter, slope, a terrain height-above-drainage measure and object size. I could not confirm from the 2015 paper itself which of these exact values it used.

## Data and benchmarks
Validated on 175 TerraSAR-X scenes acquired during real flood events worldwide; detailed evaluation at three sites in Germany, Thailand, and Albania/Montenegro (abstract).

## Key results
The abstract reports that the service is effective and robust across these conditions. Specific accuracy numbers were not available in the pages I could read.

## Limitations
- Accuracy figures, failure rates and per-site results not confirmed (paywalled).
- X-band commercial tasking; the later Sentinel-1 port is [[083-twele-s1-flood-chain]].
- Open-water focus, like its successors.

## What it means for SatClip
- The Thailand site is the closest published analogue to Indian monsoon river floods in this DLR line; it supports using the same pipeline shape for SatClip's beachhead.
- The value is in the guard rails (tile selection, auxiliary terrain masks, fuzzy refinement, region growing), not the threshold formula; SatClip's Otsu step should be wrapped the same way.
- Use the scale of their validation (175 real scenes) as the bar SatClip's flood instrument should aim at: a validation set of many real events, not one demo flood.
