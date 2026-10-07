---
id: 131
title: "Local Temperature Scaling for Probability Calibration"
authors: "Zhipeng Ding, Xu Han, Peirong Liu, Marc Niethammer"
year: 2021
venue: "ICCV 2021 (arXiv comment: Accepted by ICCV-2021; first posted August 2020)"
link: https://arxiv.org/abs/2008.05105
code: "not verified (a repository is commonly linked from the paper; GitHub was not reachable from this session)"
category: trust-calibration
era: recent
tags: [semantic-segmentation-calibration, temperature-scaling, spatially-varying-calibration, per-pixel-calibration, post-hoc-calibration]
verified: "2026-10-07 via arXiv API export.arxiv.org/api/query?id_list=2008.05105 (title, authors, first posted 2020-08-12, comment Accepted by ICCV-2021, abstract); WebFetch was refused, curl used; summary based on the abstract, full text not fetched, numeric results not confirmed"
takeaway: "Calibration for SatClip's flood masks should be allowed to vary across the tile (river channels, hill shadow, urban areas), not a single global temperature, and must leave the mask itself unchanged"
---

# Ding et al. 2021, Local Temperature Scaling (LTS)

## Problem
Semantic segmentation models produce per-pixel label probabilities that are rarely calibrated, because training and evaluation focus on IoU or Dice. Classic calibration methods target image-level classification and use one global parameter, which ignores the fact that miscalibration varies across an image.

## Approach
- A small convolutional network predicts a temperature value per pixel (a temperature map) from the image and logits.
- Logits are divided by this local temperature before the softmax.
- Because temperature scaling does not change the argmax, segmentation accuracy is unchanged, so LTS is a pure post-processing step.
- Designed for multi-label semantic segmentation.

## Data and benchmarks
COCO, CamVid and LPBA40 (brain MRI), plus a multi-atlas brain segmentation application, per the abstract.

## Key results
- Improved calibration over global and other baselines on several calibration metrics across the three datasets (per the abstract; exact numbers not confirmed here).
- Prediction accuracy is preserved by construction.

## Limitations
- Requires a labelled calibration set with dense masks to train the temperature network.
- Tested on natural, road-scene and medical images, not satellite imagery; transfer to SAR speckle statistics is untested.
- Calibrates pixels; it does not by itself give a calibrated confidence on an aggregated area.

## What it means for SatClip
- SatClip's per-pixel flood probability (from a calibrated threshold score) is likely miscalibrated in different ways in different places: radar shadow in hills, permanent river water, built-up double bounce. A spatially varying correction, conditioned on auxiliary layers such as slope, HAND and land cover, follows the LTS idea without needing a deep segmenter.
- The accuracy-preserving property fits SatClip's rule that classical instruments decide the mask: calibration may only change confidence, never the flooded pixels.
- Tile-level confidence still needs an aggregation step (for example conformal risk control on area error, entry 133).
