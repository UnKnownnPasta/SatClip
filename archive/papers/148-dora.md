---
id: 148
title: "DoRA: Weight-Decomposed Low-Rank Adaptation"
authors: "Shih-Yang Liu, Chien-Yi Wang, Hongxu Yin, Pavlo Molchanov, Yu-Chiang Frank Wang, Kwang-Ting Cheng, Min-Hung Chen"
year: 2024
venue: "ICML 2024 (Oral)"
link: https://arxiv.org/abs/2402.09353
code: https://github.com/NVlabs/DoRA
category: efficient-inference
era: recent
tags: [dora, lora, peft, weight-decomposition, magnitude-direction, fine-tuning, vlm-instruction-tuning, llava]
verified: "2026-10-07 via curl to https://export.arxiv.org/api/query (WebFetch permission request timed out); title, authors, ICML 2024 Oral comment and code URL from arXiv metadata and abstract; ICML proceedings page and repo not fetched; no numeric gains are quoted because the abstract gives none"
takeaway: "A drop-in LoRA variant with no extra inference cost; worth an A/B run against plain LoRA on SatClip's question-to-intent training set before committing to one"
---

# DoRA, weight-decomposed low-rank adaptation

## Problem
LoRA (entry 059) is cheap and adds no inference cost, but it often trails full fine-tuning in accuracy. Why, and can the gap be closed without losing LoRA's efficiency?

## Approach
- A weight decomposition analysis splits each weight matrix into a magnitude and a direction, and compares how full fine-tuning and LoRA change each.
- DoRA fine-tunes the magnitude directly and uses a LoRA low-rank update only for the direction.
- After training, the update can be merged back into the weights, so inference cost equals the base model.

## Data and benchmarks
Per the abstract: LLaMA (commonsense reasoning), LLaVA (visual instruction tuning) and VL-BART (image and video text understanding). Specific scores are in the paper and were not re-checked here.

## Key results
- Reported to consistently outperform LoRA across those models and tasks, with better learning capacity and training stability.
- No additional inference overhead once merged.

## Limitations
- Gains are reported as consistent but their size varies by task; no numbers are quoted here because they were not verified.
- Training is somewhat heavier than plain LoRA (an extra magnitude parameter and normalization per adapted layer), which matters on limited government GPUs; exact overhead not verified.
- Not specific to structured output; benefits on short JSON intent outputs are untested.

## What it means for SatClip
- The intent parser is a narrow task where plain LoRA may already be enough; run DoRA as one controlled ablation (same rank, data and seed) and keep it only if intent exact-match or abstention quality improves.
- Since the adapter merges, DoRA does not change the offline CPU serving path or the quantization step (entries 146, 061).
- Its LLaVA results are the most relevant evidence because SatClip adapts a VLM, not a text-only LLM.
