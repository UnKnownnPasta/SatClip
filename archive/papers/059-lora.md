---
id: 059
title: "LoRA: Low-Rank Adaptation of Large Language Models"
authors: "Edward J. Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen"
year: 2021
venue: "ICLR 2022 (arXiv June 2021)"
link: https://arxiv.org/abs/2106.09685
code: https://github.com/microsoft/LoRA
category: efficient-inference
era: recent
tags: [lora, parameter-efficient-fine-tuning, peft, low-rank, adapters, transformers, gpt-3]
verified: "2026-10-04 via https://arxiv.org/abs/2106.09685 and https://iclr.cc/virtual/2022/poster/6319"
takeaway: "The adapter method behind SatClip's VLM fine-tuning pipeline; merge adapters for zero-latency CPU inference and keep the base weights frozen and versioned"
---

# LoRA: Low-Rank Adaptation of Large Language Models

## Problem
Full fine-tuning of a large model updates every weight and produces a full copy per task, which is expensive to train and to store. Earlier adapter methods add layers that slow inference, and prompt-tuning methods use up sequence length and can be hard to optimise.

## Approach
Freeze all pretrained weights. For selected weight matrices (the paper focuses on attention projections), learn the update as a product of two small matrices of low rank r, so only those small matrices are trained. After training, the low-rank product can be added into the frozen weight, so the deployed model has exactly the original architecture and no extra latency. Different tasks can share one base model and swap small adapter files.

## Data and benchmarks
Experiments on RoBERTa and DeBERTa (GLUE), GPT-2 (E2E NLG and other generation tasks) and GPT-3 175B (WikiSQL, MultiNLI, SAMSum), comparing with full fine-tuning, adapters, prefix tuning and BitFit.

## Key results
Per the abstract, for GPT-3 175B LoRA cuts trainable parameters by about 10,000 times and GPU memory by about 3 times compared with full fine-tuning (Adam), while matching or beating fine-tuning quality, with higher training throughput and no added inference latency.

## Limitations
- Studied on language models; vision and VLM use came later through other work and libraries (for example Hugging Face PEFT).
- Rank and target modules are hyperparameters; the paper explores them but there is no universal choice.
- Batching inputs for different tasks with different adapters in one forward pass is not straightforward if adapters are merged.
- Still needs a GPU to train models of meaningful size.

## What it means for SatClip
- Use LoRA (via PEFT) as the default in our GPU fine-tuning pipeline: train only the question parsing and explanation behaviour of the VLM, never the instruments.
- Merge the adapter into the base weights before export so CPU users get no extra latency; ship the unmerged adapter too, so others can audit or retrain it.
- Record base model ID, revision, adapter hash, rank and target modules in the model card and in each evidence card's provenance field.
- Train the adapter to output structured instrument calls (tool name, AOI, dates) and to say it cannot answer when no instrument fits; this keeps numbers out of the VLM's mouth.
- Evaluate before and after LoRA on held-out questions, including abstention rate, so fine-tuning does not quietly make the model overconfident.
