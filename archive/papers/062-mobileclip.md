---
id: 062
title: "MobileCLIP: Fast Image-Text Models through Multi-Modal Reinforced Training"
authors: "Pavan Kumar Anasosalu Vasu, Hadi Pouransari, Fartash Faghri, Raviteja Vemulapalli, Oncel Tuzel"
year: 2024
venue: "CVPR 2024"
link: https://arxiv.org/abs/2311.17049
code: https://github.com/apple/ml-mobileclip
category: efficient-inference
era: recent
tags: [clip, mobileclip, efficient, knowledge-distillation, zero-shot, datacompdr, openclip, edge, cpu]
verified: "2026-10-04 via https://arxiv.org/abs/2311.17049 and https://github.com/apple/ml-mobileclip"
takeaway: "Small, fast CLIP models via reinforced training; a CPU-friendly alternative encoder for SatClip's zero-shot land cover instrument if licence and accuracy on Sentinel-2 check out"
---

# MobileCLIP: Fast Image-Text Models through Multi-Modal Reinforced Training

## Problem
CLIP models with large transformer encoders are accurate but too slow and large for phones and other limited hardware. Simply shrinking them loses much of their zero-shot accuracy.

## Approach
- A family of efficient image and text encoders designed for low latency (variants S0, S1, S2, B).
- Multi-modal reinforced training: knowledge from an image captioning model and an ensemble of strong CLIP teachers is stored once in the dataset (synthetic captions and teacher embeddings), so training a student needs no teacher forward passes.
- The reinforced dataset is called DataCompDR (built on DataComp); a later MobileCLIP2 release uses DFNDR.

## Data and benchmarks
Zero-shot evaluation on 38 benchmarks (ImageNet and the usual CLIP suite plus retrieval). Latency measured on an iPhone 12 Pro Max.

## Key results
- Per the abstract: MobileCLIP-S2 is 2.3 times faster than the previous best CLIP based on ViT-B/16 while being more accurate; reinforced training also adds 2.9% average across 38 benchmarks for a ViT-B/16 student, with 10 to 1000 times better learning efficiency than non-reinforced training.
- Per the repo table: MobileCLIP-S0 reaches 67.8% ImageNet zero-shot top-1 with about 11.4M image plus 42.4M text parameters; MobileCLIP-B (LT) reaches 77.2%.

## Limitations
- Trained on web image-text data; no remote sensing evaluation, so performance on 10 m Sentinel-2 chips is unknown and may be poor.
- Latency figures are for an iPhone neural engine, not a laptop CPU.
- Licences differ by part: code MIT, model weights under Apple's ML research terms of use, data CC-BY-NC-ND. We have not checked whether the weight terms allow use in a public government-facing tool.
- RGB only.

## What it means for SatClip
- Benchmark MobileCLIP-S0/S2 (loadable through OpenCLIP) against our current CLIP or RemoteCLIP backbone (entry 008) on CPU: measure milliseconds per chip and zero-shot accuracy on a small labelled Indian land cover set.
- Adopt it only if accuracy holds after calibration; speed is useless if the abstention rate rises to cover poor predictions.
- Copy the reinforced training idea for our own GPU pipeline: precompute captions and teacher embeddings for Indian Sentinel-2 chips once, then distil a small RS-specific CLIP cheaply.
- Resolve the weight licence before shipping; if unclear, keep it as an optional download rather than a bundled default.
