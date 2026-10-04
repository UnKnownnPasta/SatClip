---
id: 024
title: "GeoLLM-Engine: A Realistic Environment for Building Geospatial Copilots"
authors: "Simranjit Singh, Michael Fore, Dimitrios Stamoulis"
year: 2024
venue: "CVPR 2024 Workshops (EarthVision)"
link: https://arxiv.org/abs/2404.15500
code: none found
category: eo-agents
era: recent
tags: [geospatial-copilot, tool-augmented-agents, benchmark, function-calling, gpt-4, react, sar, sentinel-2]
verified: "2026-10-04 via https://arxiv.org/abs/2404.15500 and https://arxiv.org/html/2404.15500"
takeaway: "GPT-4 agent success fell as tool chains grew longer; keep SatClip plans short and fixed and track tool-call correctness"
---

# GeoLLM-Engine: A Realistic Environment for Building Geospatial Copilots

## Problem
Earlier geospatial agent benchmarks used single, template-like tasks, which say little about how agents cope with the long, multi-step requests analysts actually issue on remote sensing platforms.

## Approach
The authors build an environment with over 175 tools (vision models, Mapbox map and UI actions, rasterio and geopandas operations, databases, web and knowledge-base lookups). They use GPT-4-Turbo across 100 parallel nodes to generate and verify tasks at scale with little human curation, then test agents and prompting strategies on long-horizon prompts.

## Data and benchmarks
Imagery comes from seven public datasets, about 1.1 million images in total, including xView1-3, SARFish (Sentinel-1), FAIR1M, fMoW and BigEarthNet (Sentinel-2). The generator scales beyond half a million multi-tool tasks; an evaluation split called GeoLLM-Engine-10k holds 10,000 tasks. Metrics: success rate, correctness rate (share of tool calls without error), ROUGE-L on final answers and token usage.

## Key results
GPT-4-Turbo clearly beat GPT-3.5-Turbo. The best setup (ReAct with few-shot examples on GPT-4) reached about 84.3% correctness and 81.1% success. Success fell with task length: above 95% for single-call tasks, below 70% once eight or more calls were needed.

## Limitations
GPT-4 both generates and grades tasks, risking bias. Agents are evaluated without fine-tuning and there are no train/val/test splits for training. Cost is not optimised. The authors state an intent to release code and benchmark, but no public repository was found.

## What it means for SatClip
- Expect reliability to collapse with long tool chains; keep SatClip queries to short pipelines (ideally 1 to 4 calls).
- Adopt success rate and tool-call correctness as agent metrics in our evaluation sheet, alongside calibration.
- Its tool categories (map UI, raster ops, vision, knowledge base) are a good inventory for our tool registry.
- Avoid GPT-4 as both generator and judge; use human-checked Indian queries for the test set.
- Few-shot ReAct prompts are a cheap win worth trying with our open LLM.
