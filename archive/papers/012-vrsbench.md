---
id: 012
title: "VRSBench: A Versatile Vision-Language Benchmark Dataset for Remote Sensing Image Understanding"
authors: "Xiang Li, Jian Ding, Mohamed Elhoseiny"
year: 2024
venue: "NeurIPS 2024 Datasets and Benchmarks Track"
link: https://arxiv.org/abs/2406.12384
code: https://github.com/lx709/VRSBench
category: rs-benchmark
era: recent
tags: [captioning, visual-grounding, vqa, human-verified, dota, dior, lora-finetune]
verified: "2026-10-04 via https://arxiv.org/abs/2406.12384 and https://github.com/lx709/VRSBench"
takeaway: "Reference LoRA recipe and human-verified QA design, but VHR optical only and grounding about 57% at IoU 0.5, so masks need a dedicated segmenter"
---

# VRSBench: A Versatile Vision-Language Benchmark Dataset for Remote Sensing Image Understanding

## Problem
Earlier remote sensing vision-language datasets tend to have short captions, a single task each, and limited human checking. That makes it hard to train and compare general remote sensing VLMs on several tasks at once.

## Approach
The authors build one dataset that supports captioning, visual grounding and VQA on the same images. Annotations are produced with model assistance and then verified by humans, giving detailed captions, object references with boxes, and diverse question/answer pairs.

## Data and benchmarks
- 29,614 images, 29,614 human-verified detailed captions, 52,472 object references, 123,221 QA pairs (from the abstract).
- Images come from the DOTA-v2 and DIOR object detection datasets (very high resolution optical aerial and satellite imagery).
- VQA categories include presence, quantity, color, shape and reasoning.
- Text annotations are CC-BY-4.0; DOTA images are restricted to academic, non-commercial use (per the README).

## Key results
From the GitHub README: all baselines (LLaVA-1.5, MiniGPT-v2, Mini-Gemini, GeoChat) were LoRA fine-tuned (rank 64, 5 epochs). LLaVA-1.5 led captioning with BLEU-4 of 14.7; GeoChat led grounding with 57.4% accuracy at IoU 0.5 on unique objects; Mini-Gemini led VQA at 77.8%. Other per-metric numbers were not checked.

## Limitations
Optical only, very high resolution, and no SAR or multispectral bands, so it does not match Sentinel-1/2 scale. No temporal or change questions. Image licensing limits commercial reuse. Grounding scores remain modest, showing localization is still hard.

## What it means for SatClip
- Use the LoRA recipe in the README (rank 64, short schedule) as a reference starting point for our planned VLM fine-tune.
- Adopt the human-verification step for any Indian QA set we generate; a small verified set beats a large noisy one for evaluation.
- Do not assume VRSBench scores transfer to 10 m Sentinel-2 imagery; keep a separate Sentinel-based test split.
- Grounding at about 57% (IoU 0.5) shows region masks from a VLM alone are unreliable; pair VLM answers with segmentation or detection for the region mask we return.
- Check licenses before mixing DOTA-derived data into anything beyond the academic prototype.
