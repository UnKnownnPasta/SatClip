---
id: 063
title: "SmolVLM: Redefining small and efficient multimodal models"
authors: "Andrés Marafioti, Orr Zohar, Miquel Farré, Merve Noyan, Elie Bakouch, Pedro Cuenca, Cyril Zakka, Loubna Ben Allal, Anton Lozhkov, Nouamane Tazi, Vaibhav Srivastav, Joshua Lochner, Hugo Larcher, Mathieu Morlon, Lewis Tunstall, Leandro von Werra, Thomas Wolf"
year: 2025
venue: "arXiv preprint (April 2025); peer-reviewed venue not confirmed"
link: https://arxiv.org/abs/2504.05299
code: https://github.com/huggingface/smollm
category: efficient-inference
era: recent
tags: [vlm, small-vlm, smolvlm, siglip, smollm2, pixel-shuffle, on-device, cpu, video, open-source]
verified: "2026-10-04 via https://arxiv.org/abs/2504.05299, https://arxiv.org/html/2504.05299v1 and https://github.com/huggingface/smollm"
takeaway: "Fully open 256M to 2.2B VLMs built for edge devices; the most realistic CPU base for SatClip's question parser and explainer, fine-tuned with LoRA"
---

# SmolVLM: Redefining small and efficient multimodal models

## Problem
Most vision-language models are scaled-down copies of large designs and spend many tokens per image, so even small ones need a lot of memory. This blocks deployment on phones, laptops and other edge hardware.

## Approach
- Three sizes: 256M, 500M and 2.2B parameters.
- Vision encoder SigLIP (a 93M B/16 variant for the small models, the 400M class SO-400M for 2.2B) paired with SmolLM2 language models (135M, 360M, 1.7B).
- Aggressive token reduction through pixel shuffle (space-to-depth), with a stronger compression ratio for the smaller models.
- Image splitting: large images are cut into sub-images plus a downsized overview, keeping token counts manageable; video is supported.
- Careful choice of training data mix, studied systematically in the paper.

## Data and benchmarks
Evaluated on standard image benchmarks (including OCR and document understanding) and video benchmarks (OpenCompass video suite), compared with larger open VLMs.

## Key results
Per the abstract: SmolVLM-256M uses under 1 GB of GPU memory at inference and outperforms Idefics-80B, a model about 300 times larger; SmolVLM-2.2B is competitive with state-of-the-art VLMs while using about half their GPU memory. The paper shows phone (HuggingSnap) and in-browser (WebGPU) demos. We did not re-verify per-benchmark scores.

## Limitations
- No remote sensing evaluation; satellite imagery understanding is unknown and likely weak out of the box.
- Small language models hallucinate and are weak at long reasoning, which is a risk if they are allowed to state numbers.
- CPU latency on a typical district office laptop is not reported; memory figures are for GPU.
- Preprint at time of writing.

## What it means for SatClip
- Use SmolVLM-256M or 500M as the default CPU VLM candidate for parsing questions into instrument calls and turning instrument outputs into plain language; the 2.2B model is the upgrade when RAM allows.
- Fine-tune with LoRA (entry 059), or QLoRA (entry 060) for 2.2B, on SatClip question and evidence card pairs; train it to copy numbers verbatim from instrument JSON and to abstain when confidence is below threshold.
- Add a guard that rejects any number in the VLM's explanation that is not present in the instrument output; small models make this check essential.
- Measure CPU latency and RAM ourselves (with and without 4-bit quantization, entry 061) and publish them, since the paper's figures are GPU-based.
- Keep the image path optional: the VLM rarely needs to see pixels, since the instruments already did the measurement.
