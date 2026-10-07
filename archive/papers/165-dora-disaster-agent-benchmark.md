---
id: 165
title: "Can LLM Agents Respond to Disasters? Benchmarking Heterogeneous Geospatial Reasoning in Emergency Operations"
authors: "Junjue Wang, Weihao Xuan, Heli Qi, Pengyu Dai, Kunyi Liu, Hongruixuan Chen, Zhuo Zheng, Junshi Xia, Stefano Ermon, Naoto Yokoya"
year: 2026
venue: "arXiv preprint (arXiv:2605.11633, May 2026); no peer-reviewed venue listed"
link: https://arxiv.org/abs/2605.11633
code: "Not verified (no repository named in the arXiv metadata)"
category: eo-agents
era: upcoming
tags: [disaster-response, benchmark, tool-agents, mcp, sar, multi-temporal, argument-grounding, long-horizon, dora]
verified: "2026-10-07 via curl to https://export.arxiv.org/api/query?id_list=2605.11633 (title, authors, date, comment, abstract); numbers from the abstract only"
takeaway: "The first end-to-end disaster-operations agent benchmark finds frontier LLMs fail on sensor-modality mismatch and long tool chains, and that tool-order hints barely help; this backs SatClip's fixed, sensor-aware recipes over open-ended planning for flood questions"
---

# Wang et al. 2026, DORA (disaster operations agent benchmark)

## Problem
Disaster response needs more than damage maps: responders combine sensors, roads, population and facilities, plan evacuation and write reports. Existing work tests perception alone or generic tool use, not the full operational chain.

## Approach
- Builds DORA, a benchmark of expert-written tasks with replayable expert-verified gold trajectories.
- Agents call tools from a 108-tool MCP library over optical, SAR and multispectral imagery (single, bi- and multi-temporal), elevation and social vector layers.
- Five task dimensions: disaster perception, spatial relations, rescue and evacuation planning, temporal evolution, and multimodal report writing.

## Data and benchmarks
- 515 tasks from 45 real disaster events of 10 types; about 3,500 gold tool-call steps; imagery from 0.015 to 10 m GSD.
- 13 frontier LLMs evaluated.

## Key results
- Disaster-specific failure modes: wrong damage semantics, **sensor-modality mismatch**, and wrong pipeline composition.
- Agents are limited by both tool selection and argument grounding: giving the gold tool order improves accuracy by only 1.08 to 4.40%, and alternative scaffolds add at most 3.24%.
- The gap to gold grows from 7% to 56% as pipelines get longer.

## Limitations
- A benchmark, not a deployable system; it scores task success, not calibration or abstention (as far as the abstract states).
- Disaster events and regions are not listed in the abstract; Indian monsoon floods may or may not be included.
- Very high resolution imagery dominates some tasks that SatClip scopes out.

## What it means for SatClip
- **Cite as evidence** that even frontier models choose the wrong sensor for disaster questions; SatClip makes the optical versus SAR choice in code from cloud cover, never in the language model.
- The finding that longer chains fail far more supports SatClip's one-question, one-recipe design (with GeoLLM-Engine, entry 024).
- **Adopt** its replayable gold-trajectory idea for SatClip's own evaluation: each benchmark question stores the expected instrument call, which the receipt can be compared against exactly.
- Possible external test: run SatClip's flood subset against DORA's SAR flood tasks once the data are public, reporting abstentions separately.
