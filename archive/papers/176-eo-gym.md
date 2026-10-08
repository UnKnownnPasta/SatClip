---
id: 176
title: "EO-Gym: A Multimodal, Interactive Environment for Earth Observation Agents"
authors: "Sai Ma, Zhuang Li, Sichao Li, Xinyue Xu, Ruibiao Zhu, Tony Boston, John A. Taylor"
year: 2026
venue: "arXiv preprint (arXiv:2605.01250, v1 2 May 2026); no peer-reviewed venue found"
link: https://arxiv.org/abs/2605.01250
code: "https://huggingface.co/datasets/paperuploadacount/EO-Gym (dataset link given in the paper; not fetched)"
category: rs-benchmark
era: upcoming
tags: [eo-agents, tool-use, benchmark, gymnasium, sar-optical-switching, temporal-retrieval, lora, qwen3-vl-4b, pass-at-k, xbd]
verified: "2026-10-08 via curl to https://export.arxiv.org/api/query (title, authors, date, abstract) and curl to https://arxiv.org/html/2605.01250 (full text: Sections 3 to 8, Tables 2 to 7); WebFetch permission request timed out"
takeaway: "Executable EO agent benchmark where a LoRA-tuned 4B VLM learns to fetch history and switch optical to SAR and reaches 0.74 Pass@3 (base 0.49) beating Gemini-2.5-Pro; validates SatClip's small-model-plus-tools design but scores only answer correctness with no confidence or abstention"
---

# Ma et al. 2026, EO-Gym interactive environment for EO agents

## Problem
Most EO benchmarks hand the model one fixed image and one question. Real analysts reduce uncertainty by widening the area, pulling older scenes, or switching from optical to radar when clouds block the view. No reproducible, training-scale benchmark tested that evidence-gathering loop for vision-language agents.

## Approach
- A Gymnasium-style local workspace backed by more than 660k files indexed by location, time and sensor, built from eight public datasets (for example FAIR1M, xBD, fMoW, M4-SAR) plus Landsat and Sentinel-2.
- 35 EO tools grouped into three data-access paradigms: spatial planning (pan, zoom), temporal fetching (historical scenes) and cross-modal switching (aligned optical and SAR views). Tools return crops, boxes, masked images and indices such as NDVI and NDWI. All lookups are local, so runs are reproducible without cloud APIs.
- Three evaluation axes: Verified versus Unverified tool outputs (verified replaces noisy detectors with ground-truth-checked outputs), Simple versus Detailed prompt, and task-relevant (Skill) versus full (All) tool list.
- Trajectories are synthesised, audited by an LLM committee for unsupported conclusions (for example directional claims from tools that give no coordinates), converted from multiple choice to open text, and the test set is human verified. A rewrite step also flags questions the sensor cannot answer, such as counting small vehicles in 30 m Landsat.
- Reference model EO-Gym-4B: LoRA fine-tune of Qwen3-VL-4B-Instruct for three epochs.

## Data and benchmarks
EO-Gym-Data: 9,078 trajectories and 34,604 reasoning steps over six task families and 18 question types (including temporal reasoning, disaster impact, geospatial reasoning, spatial navigation, object counting). Ten function-calling VLMs evaluated (Qwen3-VL 4B to 32B, GPT-4.1-mini, GPT-4.1, GPT-5.1, Gemini-2.5-Flash and Pro). Answers judged by GPT-4.1-mini against ground truth, with a human-checked agreement study.

## Key results
- Main setting (Verified, Simple, Skill): EO-Gym-4B reaches 0.65 Pass@1 and 0.74 Pass@3 versus 0.49 Pass@3 for its base model; its Pass@3 interval [0.71, 0.76] sits above Gemini-2.5-Pro at 0.67.
- Largest gains on temporal reasoning (0.69 vs 0.29) and disaster impact (0.68 vs 0.30). Closed models stay ahead on perception-heavy tasks (Gemini-2.5-Pro 0.86 on spatial navigation, GPT-4.1-mini 0.80 on counting).
- With raw, unverified tool outputs and all tools exposed, EO-Gym-4B still leads (0.69 Pass@3) but tool-use fidelity drops for every model.
- GPT-5.1 often skipped tools and answered from memory (tool-any rate 0.368).
- Renaming every tool at inference left scores essentially unchanged, suggesting the fine-tune learned tool function rather than names.

## Limitations
- Sources are mostly very-high-resolution aerial and commercial imagery; Sentinel-1 is not a named data source and flood extent is not a task family.
- Verified mode replaces detector noise with ground-truth-backed outputs, so the headline numbers overstate end-to-end reliability.
- Correctness is judged by an LLM; no calibration, confidence or abstention metric; a wrong but confident answer and a refusal score the same.
- Fixed tool set; transfer across data-access paradigms only partly tested.

## What it means for SatClip
- Adopt: independent evidence that a LoRA-tuned 4B VLM can learn when to fetch an older scene or switch to SAR, which is exactly the routing SatClip needs when Sentinel-2 is clouded. Reuse the Verified versus Unverified split in SatClip's own eval to separate routing errors from instrument errors.
- Adopt: the sensor-limits rewrite (refuse counting cars at 30 m) is a cheap, concrete abstention rule SatClip's intent parser should encode per instrument.
- Beat: EO-Gym rewards any correct final answer; SatClip should add a selective-risk metric (accuracy at a given coverage) and credit correct abstentions, which this benchmark cannot express.
