---
id: 017
title: "BigEarthNet-MM: A Large Scale Multi-Modal Multi-Label Benchmark Archive for Remote Sensing Image Classification and Retrieval"
authors: "Gencer Sumbul, Arne de Wall, Tristan Kreuziger et al."
year: 2021
venue: "IEEE Geoscience and Remote Sensing Magazine (GRSM), 2021 (venue as given in brief; not shown on the fetched arXiv page)"
link: https://arxiv.org/abs/2105.07921
code: https://bigearth.net (data portal; links to bigearthnet-pipeline, ConfigILM and pretrained models)
category: rs-benchmark
era: recent
tags: [sentinel-1, sentinel-2, multi-label, land-cover, corine, retrieval, europe, pretraining, benchmark]
verified: "2026-10-04 via https://arxiv.org/abs/2105.07921, https://ar5iv.labs.arxiv.org/html/2105.07921 and https://bigearth.net/"
takeaway: "Use BigEarthNet-pretrained S1/S2 encoders next to RemoteCLIP, expose only labels separable at 10 m, and measure the Europe-to-India domain gap"
---

# BigEarthNet-MM: A Large Scale Multi-Modal Multi-Label Benchmark Archive for Remote Sensing Image Classification and Retrieval

## Problem
Deep models for Earth observation were often pretrained on ImageNet, which has neither SAR nor multispectral bands and uses single labels. There was no large paired Sentinel-1/Sentinel-2 archive with multi-label land-cover annotations for training and benchmarking multi-modal classification and retrieval.

## Approach
The authors extend the original BigEarthNet (Sumbul et al., IGARSS 2019, which released 590,326 Sentinel-2 patches) by pairing every patch with a co-located Sentinel-1 patch. Labels come from CORINE Land Cover 2018. Because some of the 43 CLC Level-3 classes cannot be told apart in a single-date image, they propose a 19-class nomenclature: 10 classes kept, 22 merged into 9 new ones, 11 dropped. Patches fully covered by snow, cloud or cloud shadow (70,987) are flagged for exclusion. They release fixed train, validation and test splits.

## Data and benchmarks
- 590,326 Sentinel-1/Sentinel-2 pairs from 10 European countries (including Austria, Finland, Portugal, Serbia), acquired June 2017 to May 2018.
- Splits as read: 269,695 train, 123,723 validation, 125,866 test pairs.
- Baselines: VGG16/19 and ResNet50/101/152.
- A refined v2.0 (reBEN, IGARSS 2025) now lists 549,488 pairs on bigearth.net.

## Key results
The abstract states that models trained from scratch on BigEarthNet-MM beat ImageNet-pretrained ones, most clearly for complex classes such as agriculture and natural vegetation. One per-class example read from the ar5iv table: urban fabric F2 about 56.3 (ImageNet transfer) versus about 72.0 (trained on BigEarthNet-MM). Aggregate S1 vs S2 vs S1+S2 scores could not be confirmed from the fetched pages.

## Limitations
Europe only, so climates, crops and settlement patterns differ sharply from India. Labels inherit CORINE errors and its 2018 timing. One image per location, so no seasonality per sample.

## What it means for SatClip
- Use BigEarthNet-pretrained S1/S2 encoders (Hugging Face BIFOLD models) as a CPU-friendly multispectral classifier alongside RemoteCLIP, which only sees RGB.
- Adopt the 19-class idea: only expose land-cover labels that are separable at 10 m in one acquisition, and abstain on the rest.
- Expect a domain gap over Indian paddy, plantations and informal settlements; measure it on a small Indian labelled set before trusting confidence.
- Reuse the cloud and snow flagging step in the STAC pipeline so scenes are filtered before any answer.
- Multi-label output maps well to "what is in this area" queries, with per-label calibrated scores.
