---
id: 014
title: "GEOBench-VLM: Benchmarking Vision-Language Models for Geospatial Tasks"
authors: "Muhammad Sohail Danish, Muhammad Akhtar Munir, Syed Roshaan Ali Shah et al."
year: 2024
venue: "ICCV 2025 (per official GitHub README)"
link: https://arxiv.org/abs/2411.19325
code: https://github.com/The-AI-Alliance/GEO-Bench-VLM
category: rs-benchmark
era: recent
tags: [benchmark, mcq, counting, segmentation, temporal, multi-task, open-vlm, gpt-4o]
verified: "2026-10-04 via https://arxiv.org/abs/2411.19325 and https://github.com/The-AI-Alliance/GEO-Bench-VLM"
takeaway: "Best open VLM reaches only about 42% MCQ accuracy on geospatial tasks, which justifies tool grounding plus abstention; reuse its task taxonomy"
---

# GEOBench-VLM: Benchmarking Vision-Language Models for Geospatial Tasks

## Problem
General VLM benchmarks do not test the skills geospatial work needs (counting small objects, fine-grained categories, localization, temporal change), and existing remote sensing benchmarks cover few tasks each.

## Approach
The authors (eight in total, including Fahad Shahbaz Khan, Paolo Fraccaro, Alexandre Lacoste and Salman Khan) build a broad benchmark with manually verified instructions, mostly in multiple-choice form, and evaluate generic open, closed, and remote sensing specific VLMs under a common protocol.

## Data and benchmarks
- Over 10,000 manually verified instructions.
- 8 broad categories and 31 sub-tasks per the README, spanning scene classification, counting, detection, fine-grained categorization, segmentation, captioning, event detection and temporal understanding.
- 13 models evaluated per the README, including LLaVA-OneVision, GPT-4o, Qwen2-VL and EarthDial.

## Key results
The best model, LLaVA-OneVision, reaches about 41.7% accuracy on the multiple-choice questions, slightly ahead of GPT-4o, and the authors describe this as roughly double random guessing. Per-task numbers were not verified here.

## Limitations
Multiple-choice scoring can overstate ability compared with free-form answers. The arXiv listing itself does not state a venue; ICCV 2025 is taken from the README. Coverage of SAR and Indian geography was not confirmed from the pages fetched.

## What it means for SatClip
- Even the best open VLM is weak on geospatial tasks, so the VLM must not be our only source of truth; tool-grounded pipelines plus abstention are justified.
- LLaVA-OneVision and Qwen2-VL are strong open candidates for our LoRA base model; check CPU feasibility of small variants.
- Adopt the task taxonomy to structure our evaluation table, and report against a random-guess baseline as they do.
- Beat it on our narrow scope: a few task types on Sentinel data, with calibrated confidence, rather than broad coverage.
- Use the temporal sub-tasks as an external sanity check for our change detection answers.
