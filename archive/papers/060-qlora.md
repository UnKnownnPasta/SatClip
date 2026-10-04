---
id: 060
title: "QLoRA: Efficient Finetuning of Quantized LLMs"
authors: "Tim Dettmers, Artidoro Pagnoni, Ari Holtzman, Luke Zettlemoyer"
year: 2023
venue: "NeurIPS 2023"
link: https://arxiv.org/abs/2305.14314
code: https://github.com/artidoro/qlora
category: efficient-inference
era: recent
tags: [qlora, lora, quantization, 4-bit, nf4, double-quantization, paged-optimizers, bitsandbytes, peft, guanaco]
verified: "2026-10-04 via https://arxiv.org/abs/2305.14314, https://proceedings.neurips.cc/paper_files/paper/2023/hash/1feb87871436031bdc0f2beaa62a049b-Abstract.html and https://github.com/artidoro/qlora"
takeaway: "4-bit base plus LoRA adapters makes VLM fine-tuning fit on one consumer or free-tier GPU; SatClip's LoRA pipeline should offer a QLoRA mode"
---

# QLoRA: Efficient Finetuning of Quantized LLMs

## Problem
Even with LoRA (entry 059), the frozen base model must sit in GPU memory in 16-bit precision, so fine-tuning tens of billions of parameters still needs several large GPUs.

## Approach
Keep the frozen base model in 4-bit precision and backpropagate through it into LoRA adapters that stay in higher precision. Three memory techniques make this work:
- 4-bit NormalFloat (NF4), a data type suited to normally distributed weights.
- Double quantization: the quantization constants are themselves quantized to save more memory.
- Paged optimizers, which move optimizer state between GPU and CPU memory to survive memory spikes.

## Data and benchmarks
More than 1,000 fine-tuned models across 8 instruction datasets and several model families and sizes; chatbot quality judged with the Vicuna benchmark using both human and GPT-4 evaluation.

## Key results
Per the abstract: a 65B model can be fine-tuned on a single 48 GB GPU while keeping full 16-bit fine-tuning task performance; the resulting Guanaco model reaches 99.3% of ChatGPT's level on the Vicuna benchmark after 24 hours on one GPU. Authors also note that GPT-4 evaluation is a reasonable but imperfect substitute for humans, and that current chatbot benchmarks are not fully trustworthy.

## Limitations
- Relies on bitsandbytes CUDA kernels; training is GPU-only.
- The 4-bit training format is not the same as fast CPU inference formats, so a separate export step is needed.
- Chatbot evaluation via GPT-4 is itself biased; quality claims are benchmark-specific.
- Guanaco weights depend on LLaMA licence terms (code is MIT).

## What it means for SatClip
- Add a QLoRA option to our fine-tuning pipeline so users with a single 16 to 24 GB GPU, or a free cloud notebook, can adapt a 2B to 8B VLM.
- After training, merge the adapter into a 16-bit copy of the base and then quantize for CPU (for example GGUF or AWQ, entry 061); do not ship the bitsandbytes 4-bit checkpoint as the CPU artefact.
- Use the paper's warning about automated judges: evaluate our VLM on fixed SatClip question sets with exact checks on parsed instrument calls, not only with an LLM judge.
- Log quantization settings (NF4, double quant, compute dtype) in the model card so results can be reproduced.
