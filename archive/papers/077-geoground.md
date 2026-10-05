---
id: 077
title: "GeoGround: A Unified Large Vision-Language Model for Remote Sensing Visual Grounding"
authors: "Yue Zhou, Mengcheng Lan, Xiang Li, Litong Feng, Yiping Ke, Xue Jiang, Qingyun Li, Xue Yang, Wayne Zhang"
year: 2024
venue: "arXiv preprint (arXiv:2411.11904, v3); no peer-reviewed venue found"
link: https://arxiv.org/abs/2411.11904
code: https://github.com/zytx121/GeoGround
category: rs-vlm
era: recent
tags: [vlm, visual-grounding, referring-segmentation, obb, text-mask, llava, dataset, optical-rgb]
verified: "2026-10-05 via https://arxiv.org/abs/2411.11904, https://arxiv.org/html/2411.11904 and https://github.com/zytx121/GeoGround README"
takeaway: "Shows masks can be emitted as compact text by a plain LLaVA, so even a small VLM could point at regions; but its masks are coarse and need SAM to be competitive, so keep instrument masks as the truth"
---

# GeoGround: A Unified Large Vision-Language Model for Remote Sensing Visual Grounding

## Problem
RS visual grounding (find the object a sentence describes) comes in three output forms: horizontal boxes, oriented boxes and masks. Specialist models handle one form each, and general VLMs struggle to produce dense outputs like masks without bolting on an extra decoder.

## Approach
GeoGround keeps a plain LLaVA-1.5-7B architecture (CLIP ViT encoder, two-layer MLP connector, Vicuna 1.5) with 336x336 input, adding no new encoders or decoders. All outputs are turned into text: boxes as normalized integer coordinates, oriented boxes with an angle, and masks via a "Text-Mask" scheme that downsamples the mask to an N x N grid of 0/1 labels and compresses it with row-wise run-length encoding. Hybrid supervision adds prompt-assisted learning (one signal given as a hint for another) and geometry-guided learning (boxes derived from masks must agree), and a box consistency score measures agreement across output types. Coarse masks can optionally be refined by prompting SAM.

## Data and benchmarks
refGeo: about 161k image-text pairs over 80k images, merging RSVG, DIOR-RSVG, GeoChat and VRSBench grounding data with a new aerial vehicle set (AVVG, 0.007 to 0.04 m GSD drone imagery). Images overlapping the DIOR-RSVG val and test splits were removed from training sources to prevent leakage. Training used 8 V100 GPUs. Evaluation covers box grounding on seven test sets (Acc@0.5), oriented-box grounding, and referring segmentation on RRSIS-D.

## Key results
From the paper's tables:
- Box grounding average Acc@0.5 of 52.44 across seven benchmarks (N=16), versus 43.91 for LLaVA-1.5 fine-tuned on the same data and 12.44 for original GeoChat; DIOR-RSVG test 77.73, slightly above the specialist MGVLF (76.78).
- Small-object sets remain hard: RSVG test 26.65 and AVVG 21.58.
- RRSIS-D segmentation: GeoGround alone (N=32) test mIoU 54.92; with SAM refinement 60.50, close to but below the specialist RMSIN (64.20).
- A 32x32 Text-Mask takes about 316 tokens; finer grids improve shape but slow inference and training.

## Limitations
Unpublished at verification time (no venue found). RGB optical only, low 336 px input, which the authors' own small-object numbers show is a bottleneck. Text-Mask resolution caps shape detail. No uncertainty output, no handling of absent targets is described, and no SAR or temporal input.

## What it means for SatClip
- Useful trick: a VLM can return a region as a short run-length string with no extra decoder. If SatClip ever lets the VLM select a sub-region from a user phrase ("the area near the river"), this is a cheap, CPU-feasible output format.
- Avoid treating that region as measurement. Even with SAM refinement, mask mIoU is about 60; SatClip's flood extent must come from SAR thresholding, with the VLM only choosing which instrument mask to show.
- Borrow the box consistency score idea for SatClip tests: check that different representations of the same answer (mask, area in hectares, bounding district) agree, and lower confidence when they do not.
- GeoGround does not measure, date, cite scenes or abstain, so it does not challenge SatClip's evidence-card claim.
