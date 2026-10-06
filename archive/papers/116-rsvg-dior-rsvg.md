---
id: 116
title: "RSVG: Exploring Data and Models for Visual Grounding on Remote Sensing Data"
authors: "Yang Zhan, Zhitong Xiong, Yuan Yuan"
year: 2023
venue: "IEEE Transactions on Geoscience and Remote Sensing, 61: 1-13"
link: https://doi.org/10.1109/TGRS.2023.3250471
code: https://github.com/ZhanYang-nwpu/RSVG-pytorch
category: rs-benchmark
era: recent
tags: [visual-grounding, referring-expressions, dior, bounding-box, benchmark, transformer]
verified: "2026-10-06 via https://arxiv.org/abs/2210.12634, https://arxiv.org/html/2210.12634 (v1), Crossref record for 10.1109/tgrs.2023.3250471 and https://raw.githubusercontent.com/ZhanYang-nwpu/RSVG-pytorch/main/README.md; results quoted from arXiv v1 and may differ slightly from the TGRS version; README names the model MGVLF while arXiv v1 calls the module MLCM"
takeaway: "DIOR-RSVG is the standard test for pointing at a named object in a scene, and its failure modes (clutter, ambiguous phrases) show why SatClip should ground questions to an administrative polygon, not to a model-predicted box"
---

# RSVG / DIOR-RSVG

## Problem
RS language tasks (captioning, VQA, retrieval) were well studied, but object-level grounding, finding the box that a sentence refers to, had no large RS benchmark. RS scenes add strong scale variation and cluttered backgrounds that natural image grounding methods were not built for.

## Approach
- Builds the dataset (called RSVGD in the paper, released as DIOR-RSVG) from DIOR boxes with an automatic expression generator plus manual checking: it removes faulty boxes, samples objects, and writes expressions from class, attributes, geometry and relations to other objects.
- Benchmarks one-stage and transformer natural image grounding methods on it.
- Proposes a transformer model with multi-level cross-modal feature learning: multi-scale visual features plus sentence and word level text embeddings, filtering background noise.

## Data and benchmarks
- 17,402 images (800 x 800 pixels, 0.5 m to 30 m from DIOR) and 38,320 image-expression-box triplets; mean expression length 7.47 words.
- Split 40% train, 10% validation, 50% test.
- Metrics: precision at IoU 0.5 to 0.9, mean IoU and cumulative IoU.

## Key results
- Proposed model: 76.78% Pr@0.5, 68.04 mean IoU, 78.41 cumIoU (arXiv v1 Table II), ahead of TransVG (72.41% Pr@0.5) and VLTVG with ResNet-101 (75.79%).
- Precision falls steeply at tight thresholds (35.07% at Pr@0.9), so boxes are often roughly right but not tight.
- Ablation: multi-level cross-modal learning adds 4.37 points Pr@0.5 over the TransVG-like base.
- Failure cases come from cluttered scenes with look-alike regions and from vague or incomplete expressions.

## Limitations
- Optical RGB only, single date, 20 DIOR object classes; no SAR, no land-cover regions or amorphous targets such as flood extents.
- Expressions are template-generated, so language variety is limited compared with real user questions.
- Axis-aligned boxes only.

## What it means for SatClip
- SatClip's questions name districts, not objects, so grounding should come from an authoritative boundary (district mask) recorded on the evidence card, never from a VLM box; DIOR-RSVG's failure modes are a reason to keep it that way.
- If SatClip later supports "this village" or "that embankment" style follow-ups, DIOR-RSVG plus GeoGround and GeoPixel (already archived) are the baselines; report Pr@0.5 and mean IoU and abstain when the expression is ambiguous.
- The steep drop at high IoU is a reminder to show users the mask overlay so they can judge spatial fit themselves.
