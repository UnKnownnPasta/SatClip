---
id: 079
title: "EarthMind: Leveraging Cross-Sensor Data for Advanced Earth Observation Interpretation with a Unified Multimodal LLM"
authors: "Yan Shu, Bin Ren, Zhitong Xiong, Danda Pani Paudel, Luc Van Gool, Begüm Demir, Nicu Sebe, Paolo Rota"
year: 2025
venue: "arXiv preprint (arXiv:2506.01667, v2); no peer-reviewed venue found"
link: https://arxiv.org/abs/2506.01667
code: https://github.com/shuyansy/EarthMind
category: rs-vlm
era: recent
tags: [vlm, sar, optical-sar-fusion, sentinel-1, pixel-grounding, segmentation, benchmark, internvl2, sam2, 4b]
verified: "2026-10-05 via https://arxiv.org/abs/2506.01667, https://arxiv.org/html/2506.01667 and https://github.com/shuyansy/EarthMind README"
takeaway: "Strongest evidence that plain VLMs ignore SAR when given SAR plus optical; supports SatClip's choice to read SAR with instruments, and EarthMind-Bench is a ready SAR-only test set"
---

# EarthMind: Leveraging Cross-Sensor Data for Advanced Earth Observation Interpretation with a Unified Multimodal LLM

Note: arXiv v1 used a different title ("EarthMind: Towards Multi-Granular and Multi-Sensor Earth Observation with Large Multimodal Models"); the entry uses the current v2 title.

## Problem
EO assistants take one sensor at a time. Optical imagery (for example Sentinel-2) is rich but blocked by cloud; SAR (for example Sentinel-1) sees through cloud but is noisy and unfamiliar to models pretrained on photos. Simply concatenating optical and SAR tokens does not work.

## Approach
EarthMind is a 4B model built on InternVL2 with a SAM2-based grounding encoder and a [SEG] token for masks. SAR is padded to pseudo-RGB (zero padding beat channel replication) and multispectral bands are grouped in triplets as video-like frames. The key module, Hierarchical Cross-modal Attention (HCA), first computes bidirectional attention between optical and SAR tokens to weight each, then applies text-guided attention to keep the query-relevant tokens. The authors measure a "modality attention" score and show that with naive concatenation the LLM attends far more to optical tokens than SAR, which they describe as being nearly blind to SAR. If no [SEG] token is generated, the model treats the queried object as absent.

## Data and benchmarks
- FusionEO: paired optical-SAR instruction data generated with GPT-4o from six public paired sets (BigEarthNet-MM, OpenEarthMap-SAR, DFC2023 Track2, WHU-OPT-SAR, MSAW, MultiResSAR). The abstract says 30K samples; the conclusion and appendix say 20K paired dialogues, an inconsistency in the paper itself.
- EarthMind-Bench: 2,841 expert-checked pairs, 10 tasks (scene classification, existence, hallucination detection, counting, captioning, referring segmentation, spatial relations, route planning and more), each evaluable as optical only, SAR only or fused.
- Also evaluated on AID, UC-Merced, RSVQA-HRBEN, VRSBench, DIOR-RSVG, RRSIS-D, RefSegRS, BigEarthNet and a SAR ship set.

## Key results
- Most models score much lower on SAR-only than optical-only inputs; GPT-4 class models given both images as pseudo-RGB did worse than with optical alone on fine-grained tasks.
- Training ablation on EarthMind-Bench: RGB-only training scores 68.4 (RGB), 30.1 (SAR), 28.4 (fused); paired RGB-SAR training scores 69.0, 67.5 and 70.6.
- Single-sensor: 55.6% Acc@0.5 on VRSBench grounding, 428.2 CIDEr on DIOR-RSVG region captions, RRSIS-D mIoU 82.2 in the joint-training table.

## Limitations
Unpublished preprint at verification time. The authors note heavy compute from multiple visual encoders. Optical and SAR inputs must be co-registered pairs; mixed-date pairs and Indian monsoon scenes are not studied. Training text is largely GPT-4o generated. No confidence output; the [SEG]-absent rule is the only abstention-like behaviour. Single time step, so no change detection.

## What it means for SatClip
- Strong citation for the design: a learned VLM, even a purpose-built one, tends to underuse SAR unless it is specially engineered. SatClip sidesteps this by reading Sentinel-1 with a transparent threshold and only asking the VLM to explain.
- Use EarthMind-Bench's SAR-only split (or its hallucination and existence tasks) as an external check of SatClip's explanation layer, if licences permit.
- Possible stretch baseline: run EarthMind (4B, weights released) on the same flood question and compare its answer with SatClip's evidence card; the expected gap is traceability (no scene ID, date, area or confidence), not fluency.
- Note for judges: this is one of the few RS assistants with real SAR input, so SatClip should not claim to be the only SAR-aware assistant; the distinctive part is measured, cited, abstaining output.
