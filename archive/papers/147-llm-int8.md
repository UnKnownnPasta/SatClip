---
id: 147
title: "LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale"
authors: "Tim Dettmers, Mike Lewis, Younes Belkada, Luke Zettlemoyer"
year: 2022
venue: "NeurIPS 2022"
link: https://arxiv.org/abs/2208.07339
code: "https://github.com/bitsandbytes-foundation/bitsandbytes (bitsandbytes library; repo URL from general knowledge, not fetched; the abstract only says the software is open-sourced)"
category: efficient-inference
era: recent
tags: [int8, quantization, outlier-features, mixed-precision, vector-wise-quantization, bitsandbytes, inference-memory]
verified: "2026-10-07 via WebFetch on https://arxiv.org/abs/2208.07339 (title, authors, NeurIPS 2022 camera-ready comment, abstract); NeurIPS proceedings page and code repo not fetched"
takeaway: "Explains why naive 8-bit quantization breaks transformers (rare large outlier features) and gives a safe 8-bit baseline that SatClip's quantized builds must match on intent accuracy"
---

# LLM.int8(), outlier-aware 8-bit inference

## Problem
Running large language models needs a lot of GPU memory. Simple 8-bit quantization degrades quality once models get large, because a few hidden dimensions carry very large values that dominate attention and prediction.

## Approach
- Vector-wise quantization: separate scaling constants for each inner product of the matrix multiplication, covering most features in Int8.
- Mixed-precision decomposition: the few outlier feature dimensions are pulled out and multiplied in 16-bit, while more than 99.9% of values stay in 8-bit (per the abstract).
- Applied to feed-forward and attention projection layers; a 16/32-bit checkpoint can be converted at load time without retraining.

## Data and benchmarks
Language models up to 175B parameters (OPT, BLOOM are named in the abstract); the paper measures perplexity and zero-shot task accuracy. Exact task list not re-checked here.

## Key results
- Halves inference memory for the covered layers while keeping full-precision performance, with no degradation up to 175B parameters (as claimed in the abstract).
- Makes OPT-175B or BLOOM usable on a single server with consumer GPUs.
- The analysis of systematic emergent outlier features became a reference point for later quantizers (GPTQ, AWQ, and the NF4 data type used by QLoRA, entry 060).

## Limitations
- Aims at memory, not speed: the mixed-precision decomposition adds overhead, and the original kernels target CUDA GPUs, not CPUs.
- 8-bit only; for a CPU deployment, 4-bit weight quantization usually matters more.

## What it means for SatClip
- Use 8-bit as the conservative reference: any 4-bit build (GPTQ entry 146, AWQ entry 061) must be compared against it on the intent-parsing test set.
- The outlier finding is a warning for small multimodal models too: check per-layer activation ranges before trusting an aggressive quantization recipe.
- For GPU-equipped on-prem servers, 8-bit loading is a low-effort way to fit the base model while training or evaluating adapters.
