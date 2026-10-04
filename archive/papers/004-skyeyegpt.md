---
id: 004
title: "SkyEyeGPT: Unifying Remote Sensing Vision-Language Tasks via Instruction Tuning with Large Language Model"
authors: "Yang Zhan, Zhitong Xiong, Yuan Yuan"
year: 2025
venue: "ISPRS Journal of Photogrammetry and Remote Sensing, vol. 221, pp. 64-77 (2025); arXiv 2024"
link: https://arxiv.org/abs/2401.09712
code: https://github.com/ZhanYang-nwpu/SkyEyeGPT
category: rs-vlm
era: recent
tags: [vlm, instruction-tuning, visual-grounding, captioning, video-captioning, vqa, llama2, minigpt-v2]
verified: "2026-10-04 via https://arxiv.org/abs/2401.09712 and https://github.com/ZhanYang-nwpu/SkyEyeGPT"
takeaway: "Lean frozen-encoder plus linear-projector design suits a CPU-first prototype; expect degradation from aerial to 10 m Sentinel resolution"
---

# SkyEyeGPT: Unifying Remote Sensing Vision-Language Tasks via Instruction Tuning with Large Language Model

## Problem
Multimodal LLMs had been extended to many vision-language tasks, but remote sensing lagged. Prior RS models usually handled one task at a time, and there was no unified instruction dataset covering both image-level and region-level RS tasks plus conversation.

## Approach
SkyEyeGPT keeps the design simple: a frozen EVA-CLIP vision encoder, a single linear alignment layer (with token concatenation that cuts visual tokens by 4x) and a LLaMA2-chat 7B decoder, following the MiniGPT-v2 style. Training is two-stage: first multi-task instruction tuning, then tuning on conversation data to strengthen instruction following and dialogue.

## Data and benchmarks
The authors curate SkyEye-968k, about 968k instruction samples covering image captioning, video captioning, VQA, visual grounding and multi-task conversations, mixing existing datasets with new ones. Evaluation uses 8 datasets including UCM-captions, CapERA (aerial video), RSVG, DIOR-RSVG and RSVQA.

## Key results
From the PDF: CIDEr 236.75 on UCM-captions (RSGPT reports higher, 309.64), CIDEr 91.90 on CapERA video captioning, 70.50% accuracy on RSVG and 88.59% on DIOR-RSVG grounding. On RSVQA-LR it reaches 84.19% average, behind RSGPT. The abstract claims competitive results against GPT-4V.

## Limitations
The authors note a gap on RSVQA linked to satellite versus aerial modality differences. Only RGB optical imagery is covered (no SAR or multispectral). There is no confidence estimate or abstention. Weights were only released in May 2025 per the repo.

## What it means for SatClip
- Its lean projector design (frozen encoder, one linear layer) is the right shape for a CPU-first prototype: keep the vision side frozen and train only small adapters.
- Token concatenation to shrink visual tokens 4x is a cheap speed trick worth testing on our tiles.
- Grounding accuracy on DIOR-RSVG is notably better than GeoChat's referring detection, so compare both before choosing a grounding backbone.
- Its admitted aerial-to-satellite gap warns us: Sentinel 10 m pixels are far coarser than its training data, so expect degradation and measure it.
- Cite as journal work (ISPRS 2025), not just arXiv, in our references.
