---
id: 180
title: "SARLANG-1M: A Benchmark for Vision-Language Modeling in SAR Image Understanding"
authors: "Yimin Wei, Aoran Xiao, Yexian Ren, Yuting Zhu, Hongruixuan Chen, Junshi Xia, Naoto Yokoya"
year: 2026
venue: "IEEE Transactions on Geoscience and Remote Sensing, vol. 64, 2026 (DOI 10.1109/TGRS.2026.3652099); arXiv:2504.03254 (April 2025); shown at the ICLR 2025 ML4RS workshop per the README"
link: https://arxiv.org/abs/2504.03254
code: "https://github.com/Jimmyxichen/SARLANG-1M (README fetched; dataset on Hugging Face YiminJimmy/SARLANG-1M)"
category: rs-benchmark
era: recent
tags: [sar, vqa, captioning, benchmark, vision-language, umbra, capella, sardet-100k, sentinel-1-partial]
verified: "2026-10-08 via curl to https://export.arxiv.org/api/query (title, authors, abstract), https://arxiv.org/html/2504.03254v1 (data sources, statistics, headline gains), the GitHub README (TGRS acceptance January 2026) and api.crossref.org (DOI, journal, volume 64); WebFetch permission request timed out; per-model tables not checked"
takeaway: "Largest SAR image-text benchmark (about 1.13M captions and QA over 118K SAR images, 0.1 to 25 m) showing generic VLMs read SAR poorly until fine-tuned; useful to test whether SatClip's explainer misdescribes radar, but it has no flood, water or change questions"
---

# Wei et al. 2026, SARLANG-1M

## Problem
General VLMs are trained on optical photos and misread SAR, where brightness reflects geometry and roughness rather than colour. There was no large SAR image-text corpus to train or test them.

## Approach
- Collect 118,331 SAR images from four public datasets: SpaceNet6 (aerial X-band, Rotterdam), DFC2023, OpenEarthMap-SAR (Umbra spotlight, 0.15 to 0.5 m) and SARDet-100k (aggregated from about seven satellites including Gaofen-3, Sentinel-1, TerraSAR-X, RadarSat-2).
- Two text pipelines: transfer captions from paired optical images (generated with GPT-4o, then manually filtered to drop colour words), and convert detection labels into templated questions.
- Two benchmarks: SARLANG-1M-Cap (concise and detailed captions) and SARLANG-1M-VQA (object identification, classification, instance counting, region referring, object positioning, other).

## Data and benchmarks
1,126,277 text samples, more than 59 cities, 1,696 object categories, 16 land-cover classes, 1,012 question types. Evaluated two traditional models and ten VLMs (for example DeepSeek-VL, Qwen2.5-VL) before and after fine-tuning.

## Key results
- Fine-tuning on SARLANG-1M raised captioning CIDEr by 67.20% and SAR VQA GPT-4-judged accuracy by 40.22% (relative gains as stated in the paper).
- Authors report fine-tuned VLMs approach human-expert level; the human baseline protocol was not checked here.
- Per-word Grad-CAM suggests better alignment of words to SAR regions after fine-tuning.

## Limitations
- Mostly very-high-resolution commercial or aerial SAR; Sentinel-1 at 10 to 20 m appears only through SARDet-100k object chips.
- Object-centric (ships, aircraft, buildings); no flood, water, crop or temporal change questions.
- Captions transferred from optical images can describe things SAR cannot show; accuracy partly judged by GPT-4.
- No calibration or abstention evaluation.

## What it means for SatClip
- Avoid: asking the VLM to interpret raw Sentinel-1 backscatter; this benchmark shows generic VLMs misread SAR without heavy SAR fine-tuning, and SatClip's 10 m flood questions are outside its distribution anyway.
- Adopt: a small SARLANG-style probe set to check that SatClip's explainer never uses optical words (colour, greenness) when the evidence is radar.
- Keep the design: SAR flood extent comes from a calibrated thresholding or segmentation instrument, and the VLM only verbalises its output.
