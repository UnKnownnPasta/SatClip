---
id: 183
title: "FloodReasonBench: Benchmarking VLM Reasoning Segmentation for Embodied Flood Response at the Edge"
authors: "Rajat Bhattacharjya, Yoomee Jung, Minwoo Kim, Sing-Yao Wu, Eli Bozorgzadeh, Nalini Venkatasubramanian, Nikil Dutt"
year: 2026
venue: "arXiv preprint (arXiv:2608.15410, v1 15 August 2026); under review per the arXiv comment"
link: https://arxiv.org/abs/2608.15410
code: "Not yet released; code and dataset promised upon acceptance"
category: upcoming
era: upcoming
tags: [flood, reasoning-segmentation, lisa, mobilesam, lora, edge, jetson, split-computing, uav, benchmark]
verified: "2026-10-08 via curl to https://export.arxiv.org/api/query (title, authors, date, abstract, comment) and https://arxiv.org/html/2608.15410 (introduction, dataset curation, split-inference design); WebFetch permission request timed out; the source of the flood images is not named in the text read"
takeaway: "Upcoming flood benchmark where a responder's plain-language request returns a pixel mask (people, buildings, vehicles), with flood fine-tuning lifting LISA from 0.72 to 0.84 gIoU and Jetson latency and energy measured; useful edge-deployment pattern for SatClip, but it uses close-range imagery not satellites and has only 100 test samples"
---

# Bhattacharjya et al. 2026, FloodReasonBench

## Problem
Flood responders want to ask a drone or robot in words (for example, find partly submerged vehicles) and get the matching pixels back. Generic reasoning-segmentation benchmarks do not reflect flood scenes, and the heavy SAM encoder is costly on embedded hardware.

## Approach
- FloodResponseSeg: collect real-world flood images, filter with CLIP, inspect manually, localise targets with Grounding DINO, make masks with SAM2, reject poor masks, then hand-write a responder-style query per target.
- Model: LISA with the SAM encoder swapped for MobileSAM (TinyViT), LoRA on the multimodal LLM, flood-specific fine-tuning.
- Systems study: split the TinyViT backbone at different blocks, compress the intermediate features with a learned encoder, and measure accuracy, edge latency, energy and bytes sent on an NVIDIA Jetson AGX Xavier across power modes. Users set a minimum gIoU and the benchmark lists operating points that meet it.

## Data and benchmarks
Three target classes (people, buildings, vehicles). 532 annotated training samples, expanded to 2,128 with photometric augmentation; 100 un-augmented evaluation samples. Metrics gIoU and cIoU plus latency, energy and transmitted size. Generic ReasonSeg used for the pre-adaptation comparison.

## Key results
- Off-the-shelf LISA on the flood workload: 0.7223 gIoU and 0.7385 cIoU; after flood adaptation 0.8423 and 0.9013.
- Accuracy varies strongly with split point on generic data but much less after flood adaptation, so more partitions become viable.
- Power mode and split point jointly set the cost of meeting a given quality target.

## Limitations
- Close-range or aerial platform imagery; not satellite, not SAR, and not flood extent mapping. Image source not stated in the text read.
- Very small test set (100 samples) and three classes; labels partly produced by Grounding DINO and SAM2.
- No confidence, calibration or abstention; data and code not yet public.

## What it means for SatClip
- Adopt: the quality-constrained operating-point idea (pick the cheapest configuration that still meets a stated accuracy floor) fits SatClip's offline laptop target; apply it to choosing quantisation level and instrument resolution.
- Adopt: evidence that a small in-domain LoRA set (hundreds of samples) moves a VLM a lot, supporting SatClip's small LoRA parser.
- Watch: if the dataset is released, its responder-style queries are a source of realistic flood phrasing for SatClip's intent tests; it does not compete with SatClip's satellite-scale flood extent answers.
