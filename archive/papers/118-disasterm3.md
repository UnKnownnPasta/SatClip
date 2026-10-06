---
id: 118
title: "DisasterM3: A Remote Sensing Vision-Language Dataset for Disaster Damage Assessment and Response"
authors: "Junjue Wang, Weihao Xuan, Heli Qi, Zhihao Liu, Kunyi Liu, Yuhan Wu, Hongruixuan Chen, Jian Song, Junshi Xia, Zhuo Zheng, Naoto Yokoya"
year: 2025
venue: "NeurIPS 2025 (acceptance stated in the project README)"
link: https://arxiv.org/abs/2505.21089
code: https://github.com/Junjue-Wang/DisasterM3
category: rs-benchmark
era: recent
tags: [disaster, vlm-benchmark, sar, optical, bi-temporal, damage-counting, referring-segmentation, reports]
verified: "2026-10-06 via https://arxiv.org/abs/2505.21089, https://arxiv.org/html/2505.21089 (v2, 20 Oct 2025) and https://raw.githubusercontent.com/Junjue-Wang/DisasterM3/master/README.md; NeurIPS 2025 acceptance only from the README, track and proceedings page not checked"
takeaway: "The closest benchmark to SatClip's use case: general and RS VLMs score barely above chance on disaster damage counting and degrade on SAR, which is direct support for SatClip's instrument-first, SAR-first, VLM-explains-only design"
---

# DisasterM3

## Problem
Disaster response needs fast answers from pre and post event imagery, but disaster scenes vary by hazard, region and sensor, and clouds during storms and floods often force SAR for the post-event view. VLMs had no benchmark covering this mix.

## Approach
- Curates bi-temporal pairs (optical pre-event, optical or SAR post-event) from 36 major events across 10 hazard types on five continents, standardised to 0.8 m.
- Nine tasks across five capabilities: recognition, counting, localisation (referring segmentation), relational reasoning, and long-form report generation with restoration advice.
- Counting answers come from annotated building damage and road damage masks (roads labelled intact, flooded or debris covered); distractor options are set at plus or minus 20% and 40%.
- Reports are drafted by experts following UNITAR and FEMA style, then polished by GPT-4o; the Bench set is multiple choice, the Instruct set is for fine-tuning.

## Data and benchmarks
- 26,988 bi-temporal images and about 123k instruction pairs in total; Bench set has 5,024 optical and 976 SAR images with 30,042 pairs.
- 14 VLMs evaluated, including GPT-4o, GPT-4.1, Qwen2.5-VL (3B to 72B), InternVL3, GeoChat, TEOChat and EarthDial.
- Fine-tunes Qwen2.5-VL-7B, InternVL3-8B, LISA and PSALM on the Instruct set.

## Key results
- Optical-optical setting: best average QA accuracy is 42.3% (GPT-4.1); Qwen2.5-VL-72B 40.5%, GPT-4o 39.3%; RS models are far lower (GeoChat 10.7%, EarthDial 22.9%, TEOChat 23.0%).
- Building damage counting is near chance (20% for five options): GPT-4o 24.2%, GPT-4.1 25.5%, best open model 34.8%. Open-ended counting RMSE for GPT-4o is 127.5 buildings.
- GPT models get worse as building density rises; fine-tuned InternVL3-8B improves on sparse scenes but degrades elsewhere, which the authors call overfitting.
- Fine-tuning gives up to 10.4 points QA and 40.8 points on referring segmentation; SAR-post tracks stay clearly below optical.

## Limitations
- Stated by the authors: fixed 0.8 m resolution (no Sentinel-2 or Landsat scale), SAR is single polarisation only, a persistent optical-SAR gap, and counting overfitting.
- Very high resolution commercial imagery, unlike the free 10 m Sentinel data SatClip uses.
- Multiple choice grading can hide how wrong a count is; the RMSE appendix shows the gap is large.

## What it means for SatClip
- Cite this as the main external evidence for SatClip's thesis: VLMs cannot be trusted to produce disaster numbers, especially counts and especially from SAR.
- Adopt the plus or minus 20% and 40% idea for SatClip's own eval: score flooded-area answers by relative error bands against NRSC or Sen1Floods11 style references, and log abstentions separately.
- The authors' wish list (Sentinel-1 VV+VH, 10 m scale) is exactly SatClip's data layer, so SatClip can position itself as filling that gap for Indian floods with measured, receipt-backed answers.
- Keep the report-writing role for the VLM, fed with instrument outputs, mirroring DisasterM3's report task but grounded in SatClip's evidence card.
