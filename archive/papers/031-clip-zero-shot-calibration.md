---
id: 031
title: "Enabling Calibration In The Zero-Shot Inference of Large Vision-Language Models"
authors: "Will LeVine, Benjamin Pikus, Pranav Raja, Fernando Amat Gil"
year: 2023
venue: "arXiv preprint (arXiv:2303.12748, v2 April 2023)"
link: https://arxiv.org/abs/2303.12748
code: none
category: trust-calibration
era: recent
tags: [clip, zero-shot, calibration, temperature-scaling, ece, vlm]
verified: "2026-10-04 via https://arxiv.org/abs/2303.12748"
takeaway: "CLIP zero-shot scores are miscalibrated; one temperature learned per CLIP model on an auxiliary set transfers across prompts and datasets, so calibrate RemoteCLIP once and reuse"
---

# Enabling Calibration In The Zero-Shot Inference of Large Vision-Language Models

## Problem
CLIP-style models are used zero-shot: class names are turned into text prompts and the highest image-text similarity wins. Standard calibration needs labelled data from the target task, which zero-shot use by definition lacks, and the paper shows that zero-shot CLIP is miscalibrated across prompts, datasets and architectures.

## Approach
Zero-shot-enabled temperature scaling: learn a single temperature per CLIP model (architecture plus pretraining set) on an auxiliary labelled dataset, ImageNet-1k with the prompt "a photo of {}", then freeze it and divide logits by it for any new downstream task and prompt, with no retraining.

## Data and benchmarks
Temperature fitted on ImageNet-1k; evaluation on CIFAR-10, CIFAR-100 and SUN397. Architectures include ViT-B-16, ViT-B-32, ViT-L-14, ViT-H-14 and ResNet-50, pretrained on LAION-400M, LAION-2B, YFCC15M or Conceptual Captions.

## Key results
Selected ECE values reported in Table 1 of the arXiv HTML (baseline, then their method, then supervised temperature scaling as an oracle): ViT-B-16 LAION-400M 6.34% to 2.22% (oracle 0.91%); ViT-L-14 LAION-400M 6.68% to 1.36% (oracle 0.72%); ResNet-50 YFCC15M 26.69% to 7.60% (oracle 2.61%). Which evaluation dataset or aggregate each row refers to was not confirmed from the fetched page. The main claim is that one temperature generalises across inference datasets and prompts for a given model.

## Limitations
No peer-reviewed venue was shown on the abstract page. Evaluation datasets are natural-image benchmarks; transfer of the temperature to very different domains such as satellite imagery is untested. A gap to supervised (in-domain) temperature scaling remains. No code link was given on the abstract page.

## What it means for SatClip
- RemoteCLIP and GeoRSCLIP similarity scores must not be shown raw as confidence; at minimum apply one learned temperature per backbone.
- Do not borrow an ImageNet-fitted temperature for satellite tiles: fit the auxiliary temperature on a remote sensing set (for example EuroSAT or a small Indian Sentinel-2 labelled set), since the paper's own gap to in-domain calibration suggests domain matters.
- The finding that one temperature transfers across prompts is useful operationally: SatClip's query router can rephrase class prompts without recalibrating, but the evaluation should still verify ECE per prompt family.
- Pair this with conformal sets [A028] for formal coverage on top of better-calibrated scores.
