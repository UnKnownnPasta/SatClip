---
id: 011
title: "RSVQA: Visual Question Answering for Remote Sensing Data"
authors: "Sylvain Lobry, Diego Marcos, Jesse Murray, Devis Tuia"
year: 2020
venue: "IEEE Transactions on Geoscience and Remote Sensing (TGRS), DOI 10.1109/TGRS.2020.2988782"
link: https://arxiv.org/abs/2003.07333
code: https://github.com/syvlo/RSVQA
category: rs-benchmark
era: recent
tags: [vqa, sentinel-2, openstreetmap, auto-generated-qa, counting, presence, language-bias]
verified: "2026-10-04 via https://arxiv.org/abs/2003.07333 and https://rsvqa.sylvainlobry.com/"
takeaway: "Sentinel-2 VQA baseline to evaluate on first; copy OSM-template QA generation and always run a blind (no-image) baseline to expose language bias"
---

# RSVQA: Visual Question Answering for Remote Sensing Data

## Problem
Extracting information from satellite imagery usually needs task-specific models and GIS expertise. The authors propose visual question answering (VQA) as a generic interface, so a non-expert can ask a free-form question about an image and get an answer.

## Approach
Questions and answers are generated automatically from OpenStreetMap vector data (roads, buildings, water, land use) using templates. The baseline model encodes the image with an ImageNet-pretrained ResNet-152 and the question with a Skip-thoughts encoder, fuses the two by point-wise multiplication, and classifies over a fixed answer vocabulary with a small MLP.

## Data and benchmarks
- Low resolution (LR): 772 Sentinel-2 tiles (256x256 px, 10 m) over the Netherlands with about 77k question/answer triplets.
- High resolution (HR): 10,659 tiles from USGS aerial orthophotos (15 cm) with about 1.07M triplets and two test sets, one being a held-out city (Philadelphia).
- Question types: presence, counting, comparison, area, and rural/urban.
- Data on Zenodo, linked from https://rsvqa.sylvainlobry.com/.

## Key results
As read from the paper (ar5iv render): LR test overall accuracy about 79.1%, HR test set 1 about 83.2%, HR test set 2 (Philadelphia) about 78.2%. Counting is the weakest type (roughly 61 to 69%). The authors also report that the model still scores about 73.8% when given random images, which signals strong language bias.

## Limitations
OSM labels are incomplete, so ground truth is noisy. Templates limit linguistic diversity. Counting is treated as classification, and the drop on the unseen city shows weak geographic transfer. No calibration or abstention.

## What it means for SatClip
- RSVQA-LR is one of the few public VQA sets built on Sentinel-2, so it is a natural first evaluation for our optical VQA path.
- Adopt the OSM-to-template idea to auto-generate Indian question sets (e.g. from OSM plus Bhuvan layers) for district-level fine-tuning of the LoRA VLM.
- Always run a blind-image (question-only) baseline: if the model scores well without the image, our confidence is meaningless.
- Avoid answering counts from 10 m imagery as if they were exact; route counts through detection with explicit uncertainty or abstain.
- Report per-question-type accuracy and a held-out-region split, not a single headline number.
