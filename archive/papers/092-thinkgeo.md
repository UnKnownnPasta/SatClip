---
id: 092
title: "ThinkGeo: Evaluating Tool-Augmented Agents for Remote Sensing Tasks"
authors: "Akashah Shabbir, Muhammad Akhtar Munir, Akshay Dudhane, Muhammad Umer Sheikh, Muhammad Haris Khan, Paolo Fraccaro, Juan Bernabe Moreno, Fahad Shahbaz Khan, Salman Khan"
year: 2025
venue: "arXiv preprint (GitHub README lists CVPR 2026 MONTI workshop; not confirmed on a proceedings page)"
link: https://arxiv.org/abs/2505.23752
code: https://github.com/mbzuai-oryx/ThinkGeo
category: eo-agents
era: recent
tags: [benchmark, tool-use, react, step-wise-evaluation, argument-accuracy, sar, flood, failure-analysis]
verified: "2026-10-05 via https://export.arxiv.org/api/query?id_list=2505.23752, https://arxiv.org/html/2505.23752 (v3, April 2026) and https://raw.githubusercontent.com/mbzuai-oryx/ThinkGeo/main/README.md"
takeaway: "RS tool-agent benchmark where even GPT-4o gets tool arguments right only about a third of the time and final answers right under 10% end to end; the strongest published case for SatClip's fixed instruments and exact tool-call scoring"
---

# ThinkGeo: Evaluating Tool-Augmented Agents for Remote Sensing Tasks

## Problem
General tool-use benchmarks (ToolBench, API-Bank, GTA) do not test remote sensing, and earlier RS agents (Remote Sensing ChatGPT, RS-Agent) report mostly final-answer accuracy with no step-level attribution of where the agent went wrong.

## Approach
A benchmark of human-curated queries grounded in real optical and SAR imagery, solved by an agent in a ReAct loop over 14 executable tools: perception (object detection, pixel segmentation, change detection), logic and numeric tools (calculator, solver, plot) and drawing tools. Two evaluation modes:
- Step-by-step, adopted from GTA: instruction following (InstAcc), tool selection (ToolAcc), argument correctness (ArgAcc) and summary quality (SummAcc), checked against expert annotated chains.
- End-to-end: final answer accuracy, judged by GPT-4o-mini against curated check questions because exact string matching misjudged paraphrases, plus a variant with image-grounded answers.

## Data and benchmarks
- 486 tasks, 1,778 expert-verified reasoning steps; 436 optical RGB tasks and 50 SAR tasks.
- Use cases: urban planning, disaster assessment and change analysis, environmental monitoring, transport, aviation, recreational and industrial sites.
- Image sources include DOTA, NWPU-VHR-10, UCAS-AOD, iSAID, FloodNet, xBD, AID and a global dumpsite dataset.

## Key results
- GPT-4o: ToolAcc 67.73, ArgAcc 34.75, end-to-end answer accuracy 9.78 (20.40 with image grounding). GPT-4-1106: ArgAcc 36.96, answer 5.16.
- Open 7B to 8B models do worse; for example LLaMA3.1-8B and Qwen1.5-7B show "Invalid JSON" error rates of 82.36% and 92.52% in the paper's format-error analysis, and several small models skip reasoning and jump to a final answer.
- Even the best proprietary models carry tool-call error rates the paper reports as about 44% (GPT-4o) and 31% (GPT-4-1106), which the authors still call relatively low.
- Tool selection accuracy correlates most strongly with final answer accuracy.
- Related work it cites: UnivEARTH reports over 58% of generated Google Earth Engine code failing to run.

## Limitations
- Mostly high-resolution object-centric optical imagery; SAR is a small subset and flood content is drawn from FloodNet and xBD rather than Sentinel-1.
- LLM-as-judge for final answers adds its own error.
- No measurement of calibration or of an agent's ability to decline.

## What it means for SatClip
- Adopt the step-wise protocol directly: score SatClip's router on tool selection and on exact argument match (AOI, dates, polarisation, threshold), separately from the final number. This is cheap because SatClip's arguments are typed.
- Strong evidence for not letting the LLM choose free parameters: argument errors, not tool choice, are where frontier agents fail most.
- Gap SatClip can fill: ThinkGeo never asks whether the agent knows when it is wrong. Add an abstention track (unanswerable or cloudy-scene questions) and report calibration error.
