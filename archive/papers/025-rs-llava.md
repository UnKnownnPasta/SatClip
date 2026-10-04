---
id: 025
title: "RS-LLaVA: A Large Vision-Language Model for Joint Captioning and Question Answering in Remote Sensing Imagery"
authors: "Yakoub Bazi, Laila Bashmal, Mohamad Mahmoud Al Rahhal, Riccardo Ricci, Farid Melgani"
year: 2024
venue: "Remote Sensing (MDPI), 16(9), 1477"
link: https://www.mdpi.com/2072-4292/16/9/1477
code: https://github.com/BigData-KSU/RS-LLaVA
category: rs-vlm
era: recent
tags: [vlm, llava, lora, captioning, vqa, instruction-tuning, optical]
verified: "2026-10-04 via https://www.mdpi.com/2072-4292/16/9/1477 and https://github.com/BigData-KSU/RS-LLaVA"
takeaway: "LoRA recipe and released 7B checkpoint are a fine-tune starting point; its ungrounded, confidence-free output is the gap SatClip fills"
---

# RS-LLaVA: A Large Vision-Language Model for Joint Captioning and Question Answering in Remote Sensing Imagery

## Problem
Remote sensing captioning and VQA were usually handled by separate task-specific models. The authors ask whether one LLaVA-style model, adapted cheaply, can do both well on aerial imagery.

## Approach
A CLIP ViT-L encoder at 336 px feeds a Vicuna-v1.5 LLM (7B and 13B) through a projector, fine-tuned with LoRA (rank 64, alpha 16, learning rate 1e-4) on a multi-task instruction set. (The released repo names Intel neural-chat-7b-v3-3 as a base, which differs from the paper; check before reuse.)

## Data and benchmarks
They assemble an RS-instructions dataset from UCM-Captions, a UAV captioning set, RSVQA-LR and RSIVQA-DOTA, reported as 7,058 samples (5,506 train, 1,552 test). Captioning uses BLEU, METEOR, ROUGE and CIDEr; VQA uses accuracy, F1 for presence and RMSE for counting.

## Key results
Joint training: UCM-Captions BLEU-4 72.84 (7B) and 76.03 (13B), CIDEr 349.43 and 355.61. UAV CIDEr 404.54 (7B) and 390.30 (13B). RSVQA-LR average accuracy about 88.1% for both sizes, which the authors report as beating prior methods. On RSIVQA-DOTA presence F1 was about 85.7 to 85.8.

## Limitations
Small, mostly optical RGB benchmarks with saturated, template-style language. No SAR, no multispectral bands, no georeferencing or dates, and no confidence output. The authors note heavy compute needs and suggest distillation or pruning, plus future grounding and change detection.

## What it means for SatClip
- Their LoRA recipe (r 64, alpha 16) is a reasonable starting point for our planned open VLM fine-tune.
- A released 7B LoRA checkpoint exists; test it as a captioning and VQA baseline, but expect it to be too slow for CPU without quantisation.
- Do not treat high CIDEr on UCM as evidence of field usefulness; build an Indian Sentinel-2 test set with officials' real questions.
- Add what it lacks: Sentinel-1 input, scene ID and date grounding, and calibrated abstention.
- Joint multi-task training worked better than isolated tasks here, supporting one shared adapter for caption plus VQA.
