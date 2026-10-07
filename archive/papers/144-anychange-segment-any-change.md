---
id: 144
title: "Segment Any Change"
authors: "Zhuo Zheng, Yanfei Zhong, Liangpei Zhang, Stefano Ermon"
year: 2024
venue: "NeurIPS 2024 (Advances in Neural Information Processing Systems 37, pp. 81204-81224)"
link: https://arxiv.org/abs/2402.01188
code: "https://github.com/Z-Zheng/pytorch-change-models (stated in the arXiv abstract; not opened, GitHub access blocked in this session)"
category: change-detection
era: recent
tags: [anychange, sam, foundation-model, zero-shot, training-free, bitemporal-latent-matching, point-query]
verified: "2026-10-07 via arXiv export API for 2402.01188 (title, authors, NeurIPS 2024 comment), Crossref 10.52202/079017-2581 (NeurIPS 37, pages 81204-81224), and the arXiv PDF for Table 1 numbers and the limitations appendix"
takeaway: "Zero-shot foundation-model change detection is real but low precision (roughly 4 to 31 percent pixel precision across four benchmarks, with high recall); SatClip could use it to propose candidate change regions, never to report a changed area"
---

# Zheng et al. 2024, AnyChange (Segment Any Change)

## Problem
Foundation models do zero-shot classification and segmentation, but change detection still needed labelled pairs for each new change type and region. Can a frozen segmentation model detect arbitrary changes without training?

## Approach
- Builds on SAM without retraining: SAM proposes object masks on each date.
- Bitemporal latent matching: for each mask, compare SAM embeddings of the same region at both dates; the negative cosine similarity (an angle) is the change confidence, matched in both directions.
- Changes are selected by top-k ranking or an angle threshold.
- Point query: a user clicks a few example points to filter the class-agnostic change masks to one object type.

## Data and benchmarks
LEVIR-CD, S2Looking and xView2 (building-centric, very high resolution) and SECOND (multi-class), all used in binary mode for zero-shot evaluation. Baselines include DINOv2 plus change vector analysis and SAM with simpler mask matching.

## Key results
- Zero-shot, ViT-B backbone, pixel-level F1/precision/recall: LEVIR-CD 23.4/13.7/83.0; SECOND 44.6/30.5/83.2.
- Reported new unsupervised record of 48.2 percent F1 on SECOND, beating the earlier I3PE method.
- A supervised "Oracle" (LoRA-tuned SAM plus trained confidence network) reaches F1 near 73 to 76 on LEVIR-CD, showing how much the zero-shot version leaves on the table.
- Training a small detector on AnyChange pseudo-labels is reported to work with very little manual annotation (one point per image).

## Limitations
- Precision is low: the zero-shot mode flags many unchanged regions as changed.
- The authors note SAM's biases can produce physically impossible changes, and coverage of change types and geometries is limited by available datasets.
- RGB, very high resolution evaluation only; no Sentinel-1 or Sentinel-2, and the change score is a ranking, not a calibrated probability.

## What it means for SatClip
- A good fit for an optional "where should I look?" layer: propose candidate change regions that SatClip's measured instruments (log-ratio, NDVI difference) then confirm or reject.
- Its high-recall, low-precision profile is exactly why a foundation model must not supply the number on a card; area statistics should come from the calibrated instruments.
- The angle threshold is another uncalibrated score; if used, fit it on Indian labelled pairs and report its error-reject curve like any other confidence.
