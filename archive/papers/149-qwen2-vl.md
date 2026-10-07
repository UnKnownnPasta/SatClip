---
id: 149
title: "Qwen2-VL: Enhancing Vision-Language Model's Perception of the World at Any Resolution"
authors: "Peng Wang, Shuai Bai, Sinan Tan, Shijie Wang, Zhihao Fan, Jinze Bai, Keqin Chen, Xuejing Liu, Jialin Wang, Wenbin Ge, Yang Fan, Kai Dang, Mengfei Du, Xuancheng Ren, Rui Men, Dayiheng Liu, Chang Zhou, Jingren Zhou, Junyang Lin"
year: 2024
venue: "arXiv preprint (technical report, September 2024); no peer-reviewed venue found"
link: https://arxiv.org/abs/2409.12191
code: https://github.com/QwenLM/Qwen2-VL
category: efficient-inference
era: recent
tags: [qwen2-vl, vlm, small-vlm, 2b, dynamic-resolution, m-rope, open-weights, lora-base-model]
verified: "2026-10-07 via curl to https://export.arxiv.org/api/query (WebFetch permission request timed out); title, full author list, code URL, model sizes and claims from arXiv metadata and abstract; peer-reviewed venue not checked beyond arXiv; licence of the 2B weights not verified"
takeaway: "A strong open 2B VLM base whose dynamic-resolution input suits Sentinel chips of varying size, but SatClip should use it only for intent parsing and explanation, never for the numbers"
---

# Qwen2-VL technical report

## Problem
Most VLMs resize images to a fixed resolution, which wastes compute on small images and loses detail on large ones. The report also studies how VLM performance scales with model size and data.

## Approach
- Naive Dynamic Resolution: images of different sizes become different numbers of visual tokens instead of being resized to one shape.
- Multimodal Rotary Position Embedding (M-RoPE) to encode position across text, images and video.
- One paradigm for images and video; a model family at 2B, 8B and 72B parameters (sizes as named in the abstract).

## Data and benchmarks
General multimodal benchmarks (document, chart, OCR, VQA, video and agent style tasks, per the report). No remote sensing benchmark is highlighted in the abstract; specific scores were not re-checked here.

## Key results
- The 72B model is reported to be comparable to GPT-4o and Claude 3.5 Sonnet on various multimodal benchmarks and ahead of other generalist open models.
- Smaller sizes, including 2B, are released with open weights and code (per the report and repo link).

## Limitations
- Technical report, not peer reviewed; comparisons are vendor-run.
- Headline claims are for 72B; 2B quality on SatClip-style tasks is unknown and must be measured.
- Trained on RGB natural imagery; SAR and multispectral bands are out of distribution, and the model cannot be trusted to produce areas, counts or indices.
- Licence terms for each size were not verified here and must be checked before government deployment.

## What it means for SatClip
- Candidate base for the 2B LoRA model alongside SmolVLM (entry 063): compare both on question-to-intent exact-match, CPU latency after 4-bit quantization (entries 146, 061) and licence.
- Dynamic resolution lets SatClip feed a preview chip at native size when explaining a result, but the explanation must cite numbers computed by the classical instruments.
- A later Qwen2.5-VL release exists; if adopted instead, add it as a separate archive entry after verification.
