---
id: 007
title: "TEOChat: A Large Vision-Language Assistant for Temporal Earth Observation Data"
authors: "Jeremy Andrew Irvin, Emily Ruoyu Liu, Joyce Chuyi Chen, et al."
year: 2025
venue: "ICLR 2025"
link: https://arxiv.org/abs/2410.06234
code: https://github.com/ermongroup/TEOChat
category: rs-vlm
era: recent
tags: [temporal, change-detection, damage-assessment, vlm, instruction-tuning, llama-2, multi-image, vqa]
verified: "2026-10-04 via https://arxiv.org/abs/2410.06234 and https://github.com/ermongroup/TEOChat"
takeaway: "Use its temporal task taxonomy for before/after queries; too heavy for CPU and has no SAR or calibration, which SatClip adds"
---

# TEOChat: A Large Vision-Language Assistant for Temporal Earth Observation Data

Full author list: Jeremy Andrew Irvin, Emily Ruoyu Liu, Joyce Chuyi Chen, Ines Dormoy, Jinyoung Kim, Samar Khanna, Zhuo Zheng, Stefano Ermon.

## Problem
Earlier Earth observation assistants (for example GeoChat) take a single image, yet many practical questions (what flooded, which buildings were damaged, how land use changed) need a time series of images of the same place.

## Approach
TEOChat pairs a vision encoder with a LLaMA 2 language model through an MLP projector and accepts sequences of images. It is instruction-tuned on a curated mix of single-image and temporal tasks so that one conversational model handles both spatial and temporal reasoning.

## Data and benchmarks
- TEOChatlas: 554,071 instruction-following examples spanning dozens of tasks (README).
- Temporal tasks include building change detection, building damage assessment, semantic change detection and temporal scene classification; single-image tasks include scene classification, VQA and captioning.

## Key results
From the abstract and README (no exact figures were shown on the fetched pages):
- Substantially beats prior vision-language assistants, including GeoChat and Video-LLaVA, on temporal tasks.
- Comparable to or better than several task-specific specialist models.
- Strong zero-shot results on a change detection and change question answering dataset.
- Outperforms GPT-4o and Gemini 1.5 Pro on multiple temporal tasks.
Exact metric values could not be confirmed from the pages fetched.

## Limitations
- 7B-class LLaMA 2 backbone: heavy for CPU-only deployment.
- Training imagery is mainly high-resolution optical; no SAR support described.
- Licence stack is mixed (Apache 2.0 code, plus LLaMA licence and OpenAI/ShareGPT terms on parts of the data).
- No calibrated confidence or abstention mechanism is described.

## What it means for SatClip
- Adopt its task taxonomy (change detection, damage assessment, temporal classification) as the schema for our before/after query templates.
- Reuse TEOChatlas task formats when building our LoRA instruction set, filtered to licence-compatible subsets.
- Avoid running it live on CPU; use it, if at all, as an offline teacher or GPU-side baseline.
- Beat it on grounding and trust: output change masks with dates and scene IDs, plus calibrated confidence and abstention, which TEOChat does not provide.
- Extend to Sentinel-1 SAR change (cloud-penetrating flood mapping), a gap TEOChat leaves open and one that matters during the Indian monsoon.
