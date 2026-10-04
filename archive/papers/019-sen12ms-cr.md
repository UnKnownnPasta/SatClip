---
id: 019
title: "Multisensor Data Fusion for Cloud Removal in Global and All-Season Sentinel-2 Imagery"
authors: "Patrick Ebel, Andrea Meraner, Michael Schmitt, Xiao Xiang Zhu"
year: 2021
venue: "IEEE Transactions on Geoscience and Remote Sensing (TGRS), DOI 10.1109/TGRS.2020.3024744 (online 2020, issue 2021)"
link: https://arxiv.org/abs/2009.07683
code: none found (dataset SEN12MS-CR at https://mediatum.ub.tum.de/1554803)
category: sar-optical-fusion
era: recent
tags: [cloud-removal, sentinel-1, sentinel-2, sen12ms-cr, cyclegan, s2cloudless, gan, global, all-season]
verified: "2026-10-04 via https://arxiv.org/abs/2009.07683, https://ar5iv.labs.arxiv.org/html/2009.07683 and https://patrickTUM.github.io/cloud_removal/"
takeaway: "SEN12MS-CR is the monsoon cloud-gap test set; use cloud masks to choose between optical, SAR and abstaining, never present filled pixels as observed"
---

# Multisensor Data Fusion for Cloud Removal in Global and All-Season Sentinel-2 Imagery

(arXiv lists the title with the spelling "Multi-Sensor".)

## Problem
Clouds hide a large share of optical satellite views at any time. Earlier cloud removal methods were trained on synthetic clouds or limited to scenes under a fixed cloud fraction, which real imagery often exceeds. There was no global, all-season dataset pairing SAR with real cloudy and cloud-free optical images.

## Approach
The paper introduces SEN12MS-CR: co-registered triplets of a Sentinel-1 SAR patch, a cloudy Sentinel-2 patch and a cloud-free Sentinel-2 reference. The model is a cycle-consistent GAN adapted for clouds. The SAR-to-optical generator is an encoder-decoder with a long skip connection, so it learns a residual edit of the cloudy input, and it also regresses a cloud probability mask. Cloud masks come from s2cloudless. Discriminators are PatchGAN style with spectral normalisation. Cycle and identity losses are weighted by the cloud mask, plus an auxiliary loss that keeps edits sparse in clear areas.

## Data and benchmarks
- 169 globally distributed regions, all seasons; 114,325 training and 7,893 test patches of 256x256 px from 10 separate test regions (as read on ar5iv).
- Mean cloud coverage about 48% with very wide spread, from clear to fully overcast.
- Evaluation uses generative precision and recall on real data, and MAE, RMSE, PSNR, SSIM and SAM on synthetic-cloud experiments.

## Key results
The abstract reports that training on real cloudy data beats training on synthetic clouds, and that the model handles both nearly clear and heavily clouded scenes. Exact metric values could not be confirmed from the fetched pages.

## Limitations
Output under thick cloud is a plausible reconstruction guided by SAR, not an observation. Single-date setup ignores multitemporal context (addressed later in SEN12MS-CR-TS and UnCRtainTS). Precision and recall metrics are hard to relate to downstream task accuracy.

## What it means for SatClip
- SEN12MS-CR is the reference dataset for monsoon-season optical gaps; use it to test any cloud handling we add.
- Use s2cloudless-style probability masks in the pipeline to decide per region whether to answer from optical, SAR or abstain.
- Never present GAN-filled pixels as observed evidence; mark reconstructed areas in the region mask and lower confidence there.
- Prefer SAR-native answers (flood extent, change) over cloud-filled optical when cloud fraction is high.
- Watch follow-up UnCRtainTS for per-pixel uncertainty, which fits SatClip's calibration goal.
