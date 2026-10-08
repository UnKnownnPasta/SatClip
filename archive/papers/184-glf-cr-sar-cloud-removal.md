---
id: 184
title: "GLF-CR: SAR-enhanced cloud removal with global-local fusion"
authors: "Fang Xu, Yilei Shi, Patrick Ebel, Lei Yu, Gui-Song Xia, Wen Yang, Xiao Xiang Zhu"
year: 2022
venue: "ISPRS Journal of Photogrammetry and Remote Sensing, 192, 268-278"
link: https://doi.org/10.1016/j.isprsjprs.2022.08.002
code: "https://github.com/xufangchn/GLF-CR (README fetched; states it holds the code for this paper)"
category: sar-optical-fusion
era: recent
tags: [cloud-removal, sar-optical-fusion, sentinel-1, sentinel-2, sen12ms-cr, speckle, dynamic-filtering, monsoon-cloud, arxiv-2206.02850]
verified: "2026-10-08 via curl to export.arxiv.org/api/query (id 2206.02850: title, seven authors, abstract) and api.crossref.org (journal, volume 192, pages 268-278, October 2022 issue); code README fetched from raw.githubusercontent.com; WebFetch permission prompt timed out so curl was used; only the 1.7 dB PSNR gain from the abstract is quoted, no table values"
takeaway: "Uses co-registered Sentinel-1 to fill cloudy Sentinel-2 pixels with about 1.7 dB PSNR gain on SEN12MS-CR; useful as a context image for SatClip, but synthesized pixels must never feed NDVI or water masks as if they were observed"
---

# Xu et al. 2022, GLF-CR (SAR-enhanced cloud removal)

## Problem
Monsoon cloud blocks Sentinel-2 for weeks. SAR sees through cloud, but SAR and optical look very different and SAR speckle can inject noise when it is used to rebuild optical pixels, so naive fusion can make cloud removal worse rather than better.

## Approach
- Two fusion paths. Global fusion relates every local optical window to every other, so the rebuilt region stays structurally consistent with the cloud-free parts of the image.
- Local fusion transfers SAR detail into the cloudy windows to recover texture, using dynamic (content-adaptive) filtering to damp speckle effects.
- Successor in spirit to the residual SAR-optical network of entry 020 and the fusion work of entry 019; sits before the uncertainty-aware UnCRtainTS (entry 088).

## Data and benchmarks
- SEN12MS-CR: paired Sentinel-1, cloudy Sentinel-2 and cloud-free Sentinel-2 patches (the mono-temporal sibling of SEN12MS-CR-TS, entry 087).

## Key results
- The abstract reports about 1.7 dB PSNR improvement over the prior state of the art on SEN12MS-CR. Other metrics and per-condition breakdowns were not read and are not quoted.

## Limitations
- Output is a plausible image, not a measurement. Under thick cloud the optical content is invented from SAR plus context.
- No per-pixel uncertainty in the base method, so a user cannot tell which pixels are trustworthy.
- Trained on global, mostly non-Indian scenes; monsoon paddy and flooded fields were not a stated focus.

## What it means for SatClip
- Avoid for measurement: SatClip's NDVI difference and NDWI instruments must use only observed, cloud-masked pixels; reconstructed pixels would silently corrupt crop change and flood numbers.
- Adopt narrowly: a GLF-CR style fill could be shown as a clearly labelled "illustration only" background to help officials orient themselves, with the measured mask drawn on top.
- Beat: if reconstruction is ever used for numbers, prefer an uncertainty-aware method (entry 088) and abstain where predicted variance is high.
