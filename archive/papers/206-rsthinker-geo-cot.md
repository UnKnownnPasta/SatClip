---
id: 206
title: "Towards Faithful Reasoning in Remote Sensing: A Perceptually-Grounded GeoSpatial Chain-of-Thought for Vision-Language Models"
authors: "Jiaqi Liu, Lang Sun, Ronghao Fu, Bo Yang"
year: 2026
venue: "ICLR 2026 (listed in ML Anthology as liu2026iclr-faithful); arXiv:2509.22221 (v1 September 2025, v2 February 2026)"
link: https://arxiv.org/abs/2509.22221
code: "https://github.com/minglangL/RSThinker and model at https://huggingface.co/minglanga/RSThinker (both listed in the paper; not opened)"
category: rs-vlm
era: recent
tags: [geo-cot, rsthinker, chain-of-thought, grpo, verifiable-reasoning, visual-grounding, object-counting, glm-4.1v, geo-cot380k]
verified: "2026-10-09 via curl to https://export.arxiv.org/api/query?id_list=2509.22221 (title, authors, dates, abstract), curl of https://arxiv.org/html/2509.22221v2 (base model, Geo-CoT380k composition, reward design, counting table, conclusion, code links) and curl of https://mlanthology.org/iclr/2026/liu2026iclr-faithful/ (ICLR 2026 listing)"
takeaway: "RSThinker (GLM-4.1V-9B, SFT on 380k grounded rationales then GRPO) answers RS tasks with a trace whose each claim points to a box; it beats RS VLMs on counting and grounding, and makes errors visible, but verifiability here means boxes in a trace, not calibrated confidence or data provenance"
---

# Liu et al. 2026, Geo-CoT and RSThinker

## Problem
RS VLMs map pixels straight to answers, so a wrong count or a made-up object cannot be audited. The authors want reasoning where every step is tied to a location in the image.

## Approach
- Perceptually-grounded geospatial chain of thought (Geo-CoT): plan the task, gather evidence step by step with explicit spatial references (boxes), then synthesise the answer.
- Geo-CoT380k: rationales retrofitted onto existing ground-truth labels by a generator model, so each rationale is anchored to known answers.
- Two stages on GLM-4.1V-9B-Base: supervised fine-tuning on Geo-CoT380k, then GRPO with task metrics as rewards (classification correctness for VQA and scenes, IoU for grounding, mAP@0.5 for detection, a counting reward, a captioning reward).

## Data and benchmarks
- SFT data from VRSBench (VQA, captions, grounding), FIT-RS, NWPU-RESISC45, AID, DIOR-RSVG, DOTAv2 and HRRSD.
- Extra RL data: RSVQA-HR, NWPU-Captions, RSICD, RSTMD.
- Evaluated on grounding, counting, detection, classification, captioning and VQA against Claude, Gemini, GPT-5, Qwen2.5-VL, GLM-4.1V-Thinking, GeoChat, VHM, SkySenseGPT and EarthDial.

## Key results
- Counting on HRRSD: accuracy 85.26 (MAE 0.242) vs 61.45 for the best listed baseline (EarthDial); on DOTAv2-val 43.93 vs 36.20 for GPT-5.
- Large margins on the visual grounding table over RS VLMs; full per-benchmark numbers were not transcribed here and should be read from Table 4 of the paper.
- Qualitative example: when the model mislabels an object, the box in the trace exposes the error to a user.

## Limitations
- Authors note the generated rationales may carry stylistic bias from the generator.
- Optical high-resolution imagery only; no SAR, no multispectral, no multi-temporal change.
- No confidence, calibration or abstention; a confident wrong trace is still a confident wrong answer.
- GPU-scale 9B model.

## What it means for SatClip
- Adopt: the principle that each sentence in an explanation should point to evidence. For SatClip, every claim in the plain-language answer ("about 18% of the block is under water") should link to the mask and scene IDs in the receipt.
- Adopt: task-metric rewards are a reminder to evaluate SatClip's parser and explanations with the same metrics as the instruments (IoU for masks, absolute error for percentages).
- Avoid: treating a grounded trace as a trust signal by itself; it shows where the model looked, not how likely it is to be right.
- Novelty: does not materially weaken the claim. It establishes verifiable, grounded reasoning traces for RS VLMs (ICLR 2026), which overlaps with SatClip's "auditable answer" language, so SatClip should not claim auditability of reasoning as new. It has no calibrated confidence, abstention, scene-level provenance, live retrieval or SAR, which are SatClip's actual differentiators.
