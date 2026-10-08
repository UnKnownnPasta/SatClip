---
id: 190
title: "UrbanSARFloods: Sentinel-1 SLC-Based Benchmark Dataset for Urban and Open-Area Flood Mapping"
authors: "Jie Zhao, Zhitong Xiong, Xiao Xiang Zhu"
year: 2024
venue: "CVPR 2024 Workshops (EarthVision), per arXiv comment and the authors' repository; arXiv 2406.04111"
link: https://arxiv.org/abs/2406.04111
code: "https://github.com/jie666-6/UrbanSARFloods (README fetched; data on Hugging Face S1Floodbenchmark/UrbanSARFloods_v1; no training code, baselines used segmentation_models_pytorch)"
category: change-detection
era: recent
tags: [sentinel-1, slc, interferometric-coherence, pre-post-event, urban-flood, flood-mapping, bitemporal, class-imbalance, benchmark]
verified: "2026-10-08 via curl to export.arxiv.org/api/query (title, three authors, abstract, comment 'Accepted by CVPR 2024 EarthVision Workshop') and the GitHub README (CVF open access link, data location); WebFetch permission prompt timed out so curl was used; the README mentions corrections to the paper which were not reviewed; no IoU values quoted"
takeaway: "Pre- and during-flood Sentinel-1 intensity plus interferometric coherence over 18 events shows urban flooding is still largely missed by CNNs; SatClip should say plainly that its SAR intensity water mask does not cover flooded towns"
---

# Zhao, Xiong and Zhu 2024, UrbanSARFloods

## Problem
Most SAR flood datasets (Sen1Floods11, entry 022) label open-area floods, where water is dark. In towns, floodwater between buildings can make the radar return brighter (double bounce), so intensity thresholds miss it. Detecting it needs change in intensity and in interferometric coherence between a pre-event and an in-event acquisition.

## Approach
- Processes Sentinel-1 Single Look Complex data into intensity and interferometric coherence for pairs acquired before and during each flood.
- Labels three classes: non-flood, flooded open area and flooded urban area.
- Benchmarks standard CNN segmenters, including weighted cross entropy and pretrained-backbone transfer.

## Data and benchmarks
- 8,879 chips of 512 by 512 pixels, 807,500 km2, 20 land cover classes, 5 continents, 18 flood events, in GeoTIFF.

## Key results
- Weighted cross entropy and transfer learning did not overcome class imbalance and the small training set.
- Urban flood detection remained the hardest case. Exact scores were not read and are not quoted.

## Limitations
- Requires SLC processing for coherence, which is heavier than the GRD backscatter SatClip uses.
- Few events; urban flood class is small and imbalanced.
- The authors' repository notes corrections to the paper; these were not checked.

## What it means for SatClip
- Adopt now: in the answer card, state that the SAR water mask covers open ground and fields, and that flooding inside built-up areas may be missed; lower confidence or abstain for urban-majority areas of interest (mask with a built-up layer).
- Later: a coherence-drop instrument (pre versus co-event coherence from SLC pairs) is the established route to urban floods; adding it would also give a second, independent change signal next to the log-ratio.
- Use the dataset's urban test events to measure how often SatClip's open-water instrument misses urban floods before claiming coverage.
