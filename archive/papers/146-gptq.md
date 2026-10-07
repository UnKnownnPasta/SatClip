---
id: 146
title: "GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers"
authors: "Elias Frantar, Saleh Ashkboos, Torsten Hoefler, Dan Alistarh"
year: 2023
venue: "ICLR 2023 (arXiv October 2022)"
link: https://arxiv.org/abs/2210.17323
code: https://github.com/IST-DASLab/gptq
category: efficient-inference
era: recent
tags: [gptq, post-training-quantization, weight-only, 4-bit, 3-bit, second-order, one-shot, llm-compression]
verified: "2026-10-07 via curl to https://export.arxiv.org/api/query (WebFetch permission request timed out); title, authors, ICLR 2023 comment, code URL and numbers from the arXiv abstract; ICLR proceedings page and GitHub repo not fetched; method details beyond the abstract summarized from general knowledge of the paper"
takeaway: "A one-shot, calibration-based 3 to 4-bit weight quantizer to benchmark against AWQ when shrinking SatClip's merged 2B intent model, judged on intent-JSON accuracy rather than perplexity"
---

# GPTQ, one-shot post-training weight quantization

## Problem
Large generative transformers are expensive to store and run. Earlier one-shot (no retraining) quantization methods either lost too much accuracy at low bit widths or did not scale to models with hundreds of billions of parameters.

## Approach
- Quantizes weights layer by layer after training, using a small calibration set and approximate second-order (Hessian-based) information to compensate for rounding error in the remaining weights.
- Engineered so the procedure runs quickly even on very large models, with weight-only output that inference kernels can dequantize on the fly.

## Data and benchmarks
Evaluated on OPT and BLOOM model families (language modelling perplexity and zero-shot tasks, per the paper); the abstract reports headline numbers for 175B-parameter models. Exact benchmark list not re-checked here.

## Key results
- Quantizes a 175B-parameter GPT model in about four GPU hours down to 3 or 4 bits per weight, with negligible accuracy loss versus the uncompressed baseline (as stated in the abstract).
- Claims more than double the compression gain of prior one-shot methods, and reasonable accuracy even at 2-bit or ternary levels.
- End-to-end inference speedups over FP16 of about 3.25x on A100 and 4.5x on A6000 GPUs.

## Limitations
- Results and speedups are GPU-centric; CPU speed depends on the runtime (for example llama.cpp style kernels), not on the paper.
- Weight-only; activations stay in higher precision.
- Needs calibration data, and quality at low bits is reported mostly for very large models; small (about 2B) models are typically more sensitive, which the abstract does not quantify.

## What it means for SatClip
- After LoRA training, merge the adapter and try GPTQ and AWQ (entry 061) at 4 bits for the on-prem CPU build; keep whichever loses less on a held-out set of district-official questions.
- Use real SatClip questions (multilingual, place names, dates) as the calibration set, not generic web text.
- Gate release on structured metrics: exact-match of intent JSON fields and abstention rate, not perplexity.
