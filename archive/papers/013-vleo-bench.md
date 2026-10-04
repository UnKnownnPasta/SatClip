---
id: 013
title: "Good at captioning, bad at counting: Benchmarking GPT-4V on Earth observation data"
authors: "Chenhui Zhang, Sherrie Wang"
year: 2024
venue: "CVPR 2024 Workshops (EarthVision), pp. 7839-7849; also presented at ICLR 2024 ML4RS workshop"
link: https://arxiv.org/abs/2401.17600
code: https://github.com/Earth-Intelligence-Lab/vleo-bench
category: rs-benchmark
era: recent
tags: [gpt-4v, vleo-bench, counting, localization, change-detection, xbd, disaster, evaluation]
verified: "2026-10-04 via https://arxiv.org/abs/2401.17600, https://vleo.danielz.ch/ and https://openaccess.thecvf.com/content/CVPR2024W/EarthVision/html/Zhang_Good_at_Captioning_Bad_at_Counting_Benchmarking_GPT-4V_on_Earth_CVPRW_2024_paper.html"
takeaway: "Let the VLM caption and explain but route counts, boxes and damage to dedicated instruments; GPT-4V got about 0.16 mIoU on localization"
---

# Good at captioning, bad at counting: Benchmarking GPT-4V on Earth observation data

## Problem
General-purpose VLMs such as GPT-4V were being proposed for Earth observation work without a clear picture of what they can and cannot do on real EO tasks.

## Approach
The authors assemble VLEO-Bench from existing datasets and group tasks into three capability areas: scene understanding, localization and counting, and change detection. They prompt GPT-4V and open models and score them against labels.

## Data and benchmarks
Per the project page: aerial landmark recognition, RSICD captioning, BigEarthNet land cover, fMoW-WILDS and PatternNet land use; DIOR-RSVG referring expressions; counting on NEON-Tree, COWC, xBD and aerial animal imagery; xBD before/after damage assessment. Data is on Hugging Face (mit-ei collection).

## Key results
From the project page: GPT-4V reaches about 0.67 accuracy on landmark recognition and a RefCLIPScore of about 0.75 on captioning, but only about 0.16 mean IoU on referring-expression localization, performs poorly on small-object counting, and systematically fails at damage categorization on xBD. Per-dataset numbers for open models were not verified here.

## Limitations
Mostly very high resolution optical imagery, no SAR. Closed model behaviour may drift across API versions. The arXiv version is labelled work in progress. The code repo has no README.

## What it means for SatClip
- The title is our design rule: let the VLM caption and describe, but never let it produce counts or boxes directly; use a detector or segmenter and attach confidence.
- Damage assessment from before/after pairs is exactly where general VLMs fail, so our change detection should be a dedicated model with the VLM only explaining its output.
- Reuse the three-way capability split (understanding, localization/counting, change) for our own evaluation report to judges.
- Add xBD-style disaster questions to our test suite, since district disaster officials are a core user.
- Abstain by default on counting questions when detector confidence is low.
