---
id: 181
title: "When Large Vision-Language Model Meets Large Remote Sensing Imagery: Coarse-to-Fine Text-Guided Token Pruning"
authors: "Junwei Luo, Yingying Zhang, Xue Yang, Kang Wu, Qi Zhu, Lei Liang, Jingdong Chen, Yansheng Li"
year: 2025
venue: "ICCV 2025 (per the official README and CVF open access link); arXiv:2503.07588, v3 24 July 2025"
link: https://arxiv.org/abs/2503.07588
code: "https://github.com/VisionXLab/LRS-VQA (README fetched; benchmark March 2025, code and weights February 2026)"
category: rs-benchmark
era: recent
tags: [lrs-vqa, large-images, token-pruning, high-resolution, vqa, benchmark, efficiency, coarse-to-fine]
verified: "2026-10-08 via curl to https://export.arxiv.org/api/query (title, authors, abstract), https://arxiv.org/html/2503.07588 (benchmark construction and evaluation setup) and the GitHub README (ICCV 2025 acceptance); WebFetch permission request timed out; leaderboard numbers in Table 2 were not extracted, so no accuracy figures are given"
takeaway: "LRS-VQA tests VLMs on huge scenes (up to 27,328 px across, 7,333 QA in 8 types) and the paper prunes vision tokens by zooming coarse to fine on text-relevant tiles; relevant to SatClip only as a reason to crop to the district AOI in code before any model sees pixels"
---

# Luo et al. 2025, LRS-VQA and coarse-to-fine token pruning

## Problem
Satellite scenes are far larger than VLM input grids. Downsampling loses small targets; tiling everything creates millions of vision tokens. Existing large-image RS benchmarks (the MME-RealWorld RS subset) have few question types and smaller images.

## Approach
- Benchmark LRS-VQA: from FAIR1M-1.0, GLH-Bridge and STAR, pick uniquely referable targets (for example the top-most ship), crop them, and have GPT-4V draft questions about colour, shape, status and so on; filter with Qwen2-VL by keeping question types whose accuracy rises with input resolution; manual review.
- Method: a Dynamic Image Pyramid plus a Region Focus Module distilled from the LLM's attention selects text-relevant tiles and prunes vision tokens, zooming in step by step instead of encoding the full image.

## Data and benchmarks
7,333 QA pairs in three parts (LRS-FAIR 2,272, LRS-Bridge 1,062, LRS-STAR 3,999) and eight types: count, colour, category, shape, status, reasoning, rural or urban, target background. Short open answers scored with a WordNet similarity threshold of 0.8. Also evaluated on MME-RealWorld-RS (1,298 images).

## Key results
- The authors report their pruning beats existing high-resolution strategies on four datasets under the same training data and is more efficient than prior token-reduction methods at high resolution. Exact accuracies were not extracted for this entry.
- Accuracy on both LRS-VQA and MME-RealWorld-RS rises with input resolution, supporting the benchmark's purpose.

## Limitations
- Very-high-resolution optical object questions; no SAR, multispectral, temporal or change content.
- Questions drafted by GPT-4V around single objects; no grounding output is scored and no calibration or abstention.
- Efficiency targets server GPUs rather than offline laptops.

## What it means for SatClip
- Avoid: feeding whole Sentinel tiles to the VLM. SatClip already clips to the district or block AOI and runs instruments on pixels, so the VLM sees only small previews and the evidence card.
- Adopt (minor): the resolution-sensitivity filter is a useful sanity check for any SatClip probe set: if accuracy does not change with resolution, the question is answerable from priors and should be dropped.
