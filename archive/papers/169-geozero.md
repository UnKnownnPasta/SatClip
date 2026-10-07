---
id: 169
title: "GeoZero: Incentivizing Reasoning from Scratch on Geospatial Scenes"
authors: "Di Wang, Shunyu Liu, Wentao Jiang, Fengxiang Wang, Yi Liu, Xiaolei Qin, Zhiming Luo, Chaoyang Zhou, Haonan Guo, Jing Zhang, Bo Du, Dacheng Tao, Liangpei Zhang"
year: 2025
venue: "arXiv preprint (arXiv:2511.22645, v1 27 November 2025, v3 13 March 2026); no peer-reviewed venue found on the arXiv record"
link: https://arxiv.org/abs/2511.22645
code: "https://github.com/MiliLab/GeoZero (stated in the arXiv comment; repo not fetched)"
category: rs-vlm
era: recent
tags: [reasoning, reinforcement-learning, grpo, a2grpo, qwen3-vl, scene-classification, visual-grounding, vqa, captioning, open-weights]
verified: "2026-10-07 via curl to https://export.arxiv.org/api/query (title, authors, dates, abstract, code link) and curl to https://arxiv.org/html/2511.22645v3 (dataset table, Tables II to IV, supplementary diagnostic); WebFetch permission request timed out"
takeaway: "RL can make an 8B RS VLM reason without hand-written chains of thought and its open data recipe is reusable, but it is RGB only and reports no confidence or abstention, so it is a parser or explainer candidate at most, not a measuring instrument"
---

# Wang et al. 2025, GeoZero (RS reasoning without cold-start chain of thought)

## Problem
Recent RS reasoning VLMs need curated chain-of-thought data for a cold start, which is costly and builds in human biases. The authors ask whether reasoning can emerge from RL alone.

## Approach
- Base model Qwen3-VL-8B-Instruct.
- GeoZero-Raw (754,749 samples aggregated from public RS sets such as VHM-Instruct, RESISC45, EuroSAT, fMoW, RSVG, DIOR-RSVG, RSVQA-HR/LR, VRS, SkyEye968k) is split into GeoZero-Instruct (about 610K, for SFT that teaches basic knowledge, not reasoning) and GeoZero-Hard (about 20K hard samples picked by a filtering model's mispredictions, for RL).
- Answer-Anchored GRPO (A2GRPO): the reasoning text is regularised by the model's own answers to keep thinking diverse but consistent with the final answer; a thinking mask is part of the recipe.

## Data and benchmarks
Scene classification (UCM, AID), visual grounding (RSVG, DIOR-RSVG), VQA (RSVQA-HR presence and compare) and captioning. Compared against GeoChat, VHM, ScoreRS, RingMo-Agent, TinyRS-R1 and GeoGround.

## Key results
- Classification: 93.81% on UCM and 92.55% on AID (base model 75.71% and 71.40%).
- Grounding: 37.16% on RSVG (base 26.41%, GeoGround 26.65%) and 75.67% on DIOR-RSVG (GeoGround 77.73% is higher).
- VQA on RSVQA-HR: 74.46% presence and 83.59% compare.
- Supplementary diagnostic: prompting the base model to reason did not help, and on RSVG it produced reasoning for only 1 of 1,227 test samples, while GeoZero reasons on all of them.

## Limitations
- RGB, mostly high-resolution aerial imagery; no SAR, no multispectral, no temporal change.
- Grounding still below 40% on RSVG, so boxes from text are unreliable.
- No calibration, confidence, abstention or link to scene IDs; reasoning traces are not checked for faithfulness.
- 8B parameters is heavy for CPU-only deployment.

## What it means for SatClip
- Adopt: the hard-sample mining idea (keep only items a cheaper model gets wrong) is a cheap way to build SatClip's LoRA training set for the intent parser from Indian question logs.
- Adopt carefully: answer-anchored RL rewards could also reward the parser for emitting a correct abstain or clarify intent, which GeoZero does not do.
- Beat: GeoZero is a good example for the comparison table of RS VLMs that reason fluently but give no confidence, no abstention and no scene provenance.
