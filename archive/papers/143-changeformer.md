---
id: 143
title: "A Transformer-Based Siamese Network for Change Detection"
authors: "Wele Gedara Chaminda Bandara, Vishal M. Patel"
year: 2022
venue: "IGARSS 2022, IEEE International Geoscience and Remote Sensing Symposium, pp. 207-210"
link: https://arxiv.org/abs/2201.01293
code: "https://github.com/wgcban/ChangeFormer (stated in the arXiv abstract; not opened, GitHub access blocked in this session)"
category: change-detection
era: recent
tags: [changeformer, transformer, siamese, levir-cd, dsifn-cd, learned-difference, very-high-resolution]
verified: "2026-10-07 via arXiv export API for 2201.01293 (title, authors, IGARSS 2022 acceptance comment, code link), Crossref 10.1109/IGARSS46834.2022.9883686 (venue, pages 207-210, July 2022), and the arXiv PDF for Table 1 numbers"
takeaway: "A widely used learned CD baseline whose large DSIFN gain comes from a 192-patch test set on very high resolution imagery; a reminder that benchmark F1 says little about 10 m Sentinel change and cannot stand in for SatClip's calibrated instruments"
---

# Bandara and Patel 2022, ChangeFormer

## Problem
Most change detection networks at the time were convolutional, with limited long-range context. The authors asked whether a hierarchical transformer encoder with a light decoder could do better on bitemporal change maps.

## Approach
- Siamese hierarchical transformer encoder (shared weights) extracts multi-scale features from the pre- and post-change images.
- A difference module (convolution, ReLU, batch norm over concatenated features) learns the comparison at each scale instead of using absolute feature differences.
- A lightweight MLP decoder fuses the multi-scale difference features into a change mask.

## Data and benchmarks
- LEVIR-CD (very high resolution building change, already in this archive as entry 037), cut into 256 by 256 patches with a random 7120/1024/2048 train/val/test split.
- DSIFN-CD (general land-cover change), 256 by 256 patches giving 14400/1360/192 train/val/test samples.

## Key results
- LEVIR-CD: F1 90.40 and IoU 82.48, versus 89.31 and 80.68 for BIT (entry 038).
- DSIFN-CD: F1 86.67 and IoU 76.48, versus 69.26 and 52.97 for BIT, a jump of about 17 F1 points.
- Trained from random initialisation for 200 epochs on a single NVIDIA Quadro RTX 8000.

## Limitations
- The DSIFN test set is only 192 patches, so the very large gain carries wide uncertainty that the paper does not quantify.
- LEVIR-CD was split randomly at patch level, which can inflate scores relative to scene-level splits.
- RGB, sub-metre imagery only; no Sentinel-2 bands, no SAR, no calibration or abstention.

## What it means for SatClip
- Do not port headline F1 claims from VHR benchmarks into SatClip's documentation of what change detection can do at 10 m.
- If a learned model is added as a cross-check, ChangeFormer is a reasonable candidate, but it would need retraining on Sentinel data and a reliability diagram before any of its output reaches a card.
- The learned difference module is the opposite of SatClip's design goal: SatClip keeps the difference explicit (log-ratio, NDVI difference) so the receipt can show it.
