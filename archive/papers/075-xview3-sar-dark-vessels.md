---
id: 075
title: "xView3-SAR: Detecting Dark Fishing Activity Using Synthetic Aperture Radar Imagery"
authors: "Fernando Paolo, Tsu-ting Tim Lin, Ritwik Gupta, Bryce Goodman, Nirav Patel, Daniel Kuster, David Kroodsma, Jared Dunnmon"
year: 2022
venue: "NeurIPS 2022 (arXiv comment: accepted to NeurIPS 2022; track not confirmed by us)"
link: https://arxiv.org/abs/2206.00897
code: https://github.com/DIUx-xView/xview3-reference
category: object-detection
era: recent
tags: [sar, sentinel-1, ship-detection, dataset, ais, vh-vv, maritime, iuu-fishing]
verified: "2026-10-04 via https://arxiv.org/abs/2206.00897, https://ar5iv.labs.arxiv.org/html/2206.00897 and https://github.com/DIUx-xView/xview3-reference"
takeaway: "Large Sentinel-1 VV/VH ship detection benchmark (991 scenes, 243,018 labelled objects); the closest object-detection work to SatClip's own data, useful for SAR preprocessing and as a model for honest, partially reliable labels"
---

# xView3-SAR: Detecting Dark Fishing Activity Using Synthetic Aperture Radar Imagery

## Problem
Illegal, unreported and unregulated fishing is hard to monitor because many vessels switch off or never carry AIS transponders. SAR sees through cloud and at night, but there was no large, open, analysis-ready SAR benchmark for detecting and characterising vessels at scale.

## Approach
The authors built an analysis-ready dataset of full Sentinel-1 scenes with both VH and VV polarisations, plus ancillary rasters for bathymetry and surface wind. Labels combine automated matching of AIS tracks to SAR detections with expert manual review. They defined tasks and metrics and ran the xView3 Computer Vision Challenge, releasing data and reference code.

## Data and benchmarks
- 991 Sentinel-1 scenes, averaging about 29,400 by 24,400 pixels, covering 43.2 million square kilometres.
- 243,018 labelled maritime objects.
- Dual polarisation (VH, VV), about 20 m resolution at 10 m pixel spacing; bathymetry and wind at 500 m.
- Tasks: object detection, vessel versus fixed infrastructure, fishing versus non-fishing, and vessel length estimation.

## Key results
- Combined F1-based detection and classification scores with a length error term into one aggregate metric; the top challenge entry scored 0.6177 on it (as reported in the paper).
- Demonstrated that full-scene, large-area SAR detection is feasible with modern deep models, while small vessels and dark vessels remain difficult.

## Limitations
- Ground truth depends partly on AIS, and most illegal vessels do not broadcast, so labels are incomplete exactly where the task matters.
- Maritime and offshore focus; inland rivers, reservoirs and floodwater are not covered.
- Winning models are GPU-trained and heavy; CPU inference on full scenes was not a goal.

## What it means for SatClip
- Reuse the preprocessing know-how: their analysis-ready Sentinel-1 VV/VH handling (calibration, terrain correction, scene tiling) and use of wind rasters are directly relevant to our SAR Otsu water instrument, since wind roughening is a key false-negative source for water.
- Consider adding a wind-speed flag to the evidence card for SAR flood answers, lowering confidence or abstaining when wind is high, inspired by their ancillary layers.
- Learn from their label honesty: state on our validation page how flood labels were made and where they are known to be incomplete (for example flooded vegetation).
- Keep ship detection out of SatClip's core scope; if a coastal district asks about boats, abstain and point to dedicated maritime services.
- Their full-scene sizes show why SatClip must read only the region of interest via COG windows (entry 049) to stay within CPU and memory limits.
