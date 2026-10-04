---
id: 006
title: "RSGPT: A Remote Sensing Vision Language Model and Benchmark"
authors: "Yuan Hu, Jianlong Yuan, Congcong Wen, Xiaonan Lu, Xiang Li"
year: 2025
venue: "ISPRS Journal of Photogrammetry and Remote Sensing, vol. 224, pp. 272-286 (2025); arXiv preprint 2307.15266 (2023)"
link: https://arxiv.org/abs/2307.15266
code: https://github.com/Lavender105/RSGPT
category: rs-vlm
era: recent
tags: [vlm, captioning, vqa, human-annotated, benchmark, rsicap, rsieval, instruction-tuning]
verified: "2026-10-04 via https://arxiv.org/abs/2307.15266 and https://github.com/Lavender105/RSGPT"
takeaway: "Copy RSICap's rich human-caption style and build a small Indian RSIEval-like test set; beat it on grounding and confidence"
---

# RSGPT: A Remote Sensing Vision Language Model and Benchmark

## Problem
General large vision-language models had advanced quickly, but remote sensing lacked high-quality image-text data for training and, just as importantly, for evaluating them. Existing captioning sets were short, templated and weak on object-level detail.

## Approach
The authors build RSICap, a small but carefully human-written caption set covering scene descriptions plus object attributes (type, colour, count, position). They fine-tune a general VLM on it to obtain RSGPT, showing that a modest amount of rich, human-quality supervision can steer a general model toward remote sensing description and question answering.

## Data and benchmarks
- RSICap: 2,585 image-text pairs with human-annotated captions (README and abstract).
- RSIEval: 100 human-annotated captions with 936 open-ended visual question-answer pairs, used as an evaluation benchmark (README).
- Images partly derive from DOTA; the README says this subset is for academic use only, commercial use prohibited. Both datasets require an access form.

## Key results
The fetched abstract and README do not state headline metric values. The README notes that manual scoring results for RSIEval were released (December 2024) and that training and test code followed in May 2025. Specific accuracy or caption scores could not be confirmed from the pages fetched.

## Limitations
- Very small training set; generalisation beyond the source imagery (largely high-resolution aerial/optical, DOTA-style) is unproven.
- Optical only; no SAR and no multi-temporal input.
- Open-ended VQA evaluation relies partly on manual scoring, which is costly and hard to reproduce.
- Licensing restrictions on DOTA-derived images limit downstream reuse.
- Model weight availability was not clear from the README.

## What it means for SatClip
- Adopt the RSICap annotation style (scene + object type, count, colour, position) as the template for our own small LoRA instruction set; quality beats quantity at our scale.
- Build a SatClip-style RSIEval: around 100 Indian Sentinel-2 scenes with officer-relevant open questions (flood extent, crop stress, new construction) and human-written reference answers.
- Avoid shipping any DOTA-derived data or weights in a public product, given the non-commercial restriction.
- Beat it on grounding: RSGPT answers are free text with no scene ID, date, mask or confidence, which is exactly SatClip's differentiator.
- Note that 10 m Sentinel imagery is far coarser than RSICap imagery, so object-level captions (counting cars) should be replaced by land-cover and change-level statements.
