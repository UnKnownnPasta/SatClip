---
id: 080
title: "Falcon: A Remote Sensing Vision-Language Foundation Model (Technical Report)"
authors: "Kelu Yao, Nuo Xu, Rong Yang, Yingying Xu, Zhuoyan Gao, Titinunt Kitrungrotsakul, Yi Ren, Pu Zhang, et al."
year: 2025
venue: "arXiv preprint (technical report, arXiv:2503.11070, v2); no peer-reviewed venue found"
link: https://arxiv.org/abs/2503.11070
code: https://github.com/TianHuiLab/Falcon
category: rs-vlm
era: recent
tags: [vlm, small-model, 0.7b, florence-2, multi-task, change-detection, segmentation, grounding, dataset, cpu-friendly]
verified: "2026-10-05 via https://arxiv.org/abs/2503.11070, https://arxiv.org/html/2503.11070 and https://github.com/TianHuiLab/Falcon README"
takeaway: "A 0.7B RS model that does grounding, segmentation and bitemporal change detection is the most CPU-plausible RS VLM to date; worth testing as SatClip's parser/explainer or as a cross-check, never as the measuring instrument"
---

# Falcon: A Remote Sensing Vision-Language Foundation Model (Technical Report)

## Problem
RS VLMs such as GeoChat cover a narrow set of tasks, are mostly 7B decoder-only LLaVA variants, and cannot do pixel-level work like segmentation or change detection.

## Approach
Falcon is initialized from Florence-2 (image encoder plus transformer encoder-decoder, 0.7B parameters in total) and trained with plain cross-entropy to answer every task as text: class names, box coordinates, polygons for masks, and polygons of changed areas when given an image pair. The output token length was raised to 4096 for dense outputs. An ablation in the appendix favours the encoder-decoder over a decoder-only design for these tasks. A 0.3B variant is also compared and generalizes worse.

## Data and benchmarks
Falcon_SFT: about 78 million instruction samples over 5.6 million images, built by merging 67 public RS datasets and rewriting their labels into 14 tasks (classification, VQA, captioning, detailed captioning, grounding, region captioning, counting, region classification and detection with horizontal and oriented boxes, pixel classification, semantic segmentation, change detection). Sources are overwhelmingly RGB optical; a few include multispectral, infrared or SAR (for example GEONRW and a SAR ship set). The authors report manual sample checks.

## Key results
From the paper's tables:
- RSVQA-HR: 0.927 (compare) and 0.931 (presence), slightly above LHRS-Bot (0.922 / 0.928) at one tenth the size.
- Box grounding AP@0.5: 87.5 on DIOR-RSVG and 56.9 on RSVG, versus 21.0 and 0.7 for GeoChat.
- Change detection mIoU ranges from 0.341 (HRSCD) to 0.699 (LEVIR-CD) across nine datasets; semantic segmentation mIoU 0.435 to 0.754.
- Human caption ratings favour Falcon overall, although the paper notes Qwen received more top ratings on the hallucination dimension.

## Limitations
Technical report, not peer reviewed at verification time. Many comparisons are against general or RS VLMs that were never trained for those tasks, so large margins partly reflect task coverage rather than skill. Evaluation is largely on in-distribution test splits of the same 67 datasets used for training. Nearly all imagery is optical; there is no evidence of Sentinel-1 flood or Sentinel-2 crop condition performance. No confidence, abstention, provenance or measurement output. No CPU latency figures were found in the paper.

## What it means for SatClip
- Most relevant small model so far: at 0.7B with a Florence-2 base, Falcon could plausibly run on a laptop CPU. Benchmark it against SatClip's current parser/explainer for latency and against the NDVI or log-ratio instrument as an independent change "second opinion".
- Do not let it produce the reported number. Change detection mIoU of 0.34 to 0.70 on curated bitemporal sets is well below what a district-level flood or crop figure needs, and it gives no confidence to gate on.
- Reuse the idea of converting existing labelled datasets into instruction format: SatClip can build an Indian question set by templating questions over existing flood masks (for example Sen1Floods11) and district boundaries.
- Falcon does not challenge the evidence-card claim: no scene IDs, dates, calibrated confidence or abstention.
