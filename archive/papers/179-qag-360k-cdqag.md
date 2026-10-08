---
id: 179
title: "Show Me What and Where has Changed? Question Answering and Grounding for Remote Sensing Change Detection"
authors: "Ke Li, Fuyu Dong, Di Wang, Shaofeng Li, Quan Wang, Xinbo Gao, Tat-Seng Chua"
year: 2024
venue: "arXiv preprint (arXiv:2410.23828, v2 13 November 2024); no peer-reviewed venue stated on arXiv or in the official README"
link: https://arxiv.org/abs/2410.23828
code: "https://github.com/like413/VisTA (README fetched; QAG-360K released November 2024, VisTA code June 2025; test set by request, research use only)"
category: rs-benchmark
era: recent
tags: [change-vqa, grounding, cdqag, qag-360k, change-masks, visual-evidence, empty-mask, cdvqa, benchmark]
verified: "2026-10-08 via curl to https://export.arxiv.org/api/query (title, authors, abstract), https://arxiv.org/html/2410.23828 (dataset, method, Tables 2 and 3 text) and the GitHub README at raw.githubusercontent.com/like413/VisTA; WebFetch permission request timed out"
takeaway: "First change-QA benchmark that pairs every textual answer with a pixel mask of where the change is (360K triplets, 8 question types) and requires an empty mask when nothing changed; closest public benchmark to SatClip's answer-plus-mask output, though optical only and without confidence"
---

# Li et al. 2024, change detection question answering and grounding (QAG-360K, VisTA)

## Problem
Change VQA (entry 178) gives text answers with no visual proof, so users cannot check where the model looked. The authors argue answers should come with the change mask that supports them.

## Approach
- New task CDQAG: input two dated images and a question; output a textual answer and a pixel-level mask of the referenced change.
- QAG-360K is generated automatically from Hi-UCD, SECOND and LEVIR-CD semantic or binary change labels using rule-based answer and mask generation; LLM-drafted question templates were manually pruned to five per type.
- Eight question types: change or not, change to what, change from what, increase or not, decrease or not, largest change, smallest change, change ratio.
- When the queried class did not change or is absent, the target is an empty mask, so models are pushed not to guess a region.
- Baseline VisTA: CLIP-pretrained text encoder and twin ResNet-101 image encoders, a multi-stage reasoning decoder with a question-answer selector, and a decoder that turns text features into convolution kernels so the mask and the answer stay consistent.

## Data and benchmarks
6,810 image pairs (0.1 to 3.0 m, 24 regions in Estonia, China and the USA), 10 land-cover classes, over 360K question-answer-mask triples (about 53 per pair). Split 70/10/20 by image. Metrics: average and overall accuracy for text; mIoU and oIoU for masks. Also evaluated on CDVQA.

## Key results
- VisTA on QAG-360K: 73.03% average accuracy and 77.35% overall accuracy; masks 82.6% mIoU and 84.8% oIoU, ahead of adapted VQA and referring-segmentation baselines (for example +5.37 OA over SOBA).
- On CDVQA: 73.1% OA on test 1 and 69.5% OA on test 2, above the original CDVQA baseline.
- Failure cases include over-smooth masks for discrete buildings and faded features mistaken for land-cover change.

## Limitations
- Very-high-resolution optical only; no SAR, no Sentinel-1/2, no flood class.
- Answers and masks come from one learned model, so a wrong mask still looks authoritative; no confidence score or abstention beyond the empty-mask convention.
- Labels are rule-generated from existing change datasets, inheriting their label noise and urban bias. Test set is not openly downloadable.

## What it means for SatClip
- Adopt: the output contract (answer plus supporting mask, empty mask when nothing changed) matches SatClip's evidence card; use the eight question types and the empty-mask rule as acceptance tests.
- Adopt: report both text accuracy and mask IoU in SatClip's eval so that a right answer from the wrong pixels is caught.
- Beat: SatClip's masks come from a calibrated instrument (SAR thresholding or a segmenter) with scene IDs and dates, and it abstains when confidence is low; VisTA always answers.
- Novelty note: this is the strongest prior work for answer-plus-mask change QA, so SatClip should claim novelty on calibration, abstention, Sentinel provenance and plain-language delivery for officials, not on grounded change answers alone.
