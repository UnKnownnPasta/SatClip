---
id: 021
title: "SARChat-Bench-2M: A Multi-Task Vision-Language Benchmark for SAR Image Interpretation"
authors: "Zhiming Ma, Xiayang Xiao, Sihao Dong, Peidong Wang, HaiPeng Wang, Qingyun Pan"
year: 2025
venue: "arXiv preprint (arXiv:2502.08168, v5 March 2025)"
link: https://arxiv.org/abs/2502.08168
code: https://github.com/JimmyMa99/SARChat
category: rs-vlm
era: recent
tags: [sar, vlm, benchmark, instruction-tuning, grounding, counting, sentinel-1-adjacent]
verified: "2026-10-04 via https://arxiv.org/abs/2502.08168 and https://github.com/JimmyMa99/SARChat"
takeaway: "About 2M SAR image-text pairs and released checkpoints give a SAR baseline, but imagery is mostly high-res targets, so test on Indian Sentinel-1"
---

# SARChat-Bench-2M: A Multi-Task Vision-Language Benchmark for SAR Image Interpretation

## Problem
General vision-language models are trained almost entirely on optical photos, so they read synthetic aperture radar (SAR) imagery poorly: speckle, layover and backscatter semantics look nothing like RGB. There was no large SAR image-text corpus to train or fairly compare VLMs on radar.

## Approach
The authors convert existing annotated SAR target datasets into roughly 2 million image-text pairs with templated and detailed descriptions, then fine-tune and evaluate a range of open VLMs on them. They position the pipeline as a recipe for building multimodal datasets in other remote sensing niches.

## Data and benchmarks
The README lists six task benchmarks with train/test splits: scene classification (91,812 items), fine-grained description (52,173), instance counting (107,197), spatial grounding (106,064), cross-modal identification (about 1.6 million) and referring expressions (107,189). Text totals about 43.9M words, with an average caption length near 10.7 words. Licence is CC BY-NC 4.0. The source imagery is mainly target-centric SAR chips (ships, aircraft, infrastructure), not Sentinel-1 IW scenes over land.

## Key results
The abstract reports experiments on 16 mainstream VLMs (families include Qwen2-VL, InternVL2.5, LLaVA, DeepSeek-VL, mPLUG-Owl3, 1B to 8B parameters), and 16 fine-tuned SARChat checkpoints are published on Hugging Face and ModelScope. Per-model accuracy figures were not visible on the pages fetched, so no numbers are quoted here.

## Limitations
Captions are largely template-derived, so language diversity is limited. The domain skews toward military and maritime targets at high resolution, with little land cover, flood or crop content. Non-commercial licence restricts some deployments. Still a preprint, not peer reviewed.

## What it means for SatClip
- Use the six task taxonomy (classify, describe, count, ground, identify, refer) as a checklist for our SAR query types, but add flood extent and crop moisture tasks that SARChat lacks.
- Evaluate a released small SARChat checkpoint (1B to 2B class) as a SAR captioning baseline before investing in our own LoRA.
- Do not assume transfer to 10 m Sentinel-1 GRD: run a small held-out Indian Sentinel-1 test before trusting any output.
- Copy the template-to-caption pipeline idea to generate cheap instruction data from Indian flood and land cover masks.
- Check the CC BY-NC licence before shipping weights in any government-facing product.
