---
id: 090
title: "GeoGPT: Understanding and Processing Geospatial Tasks through An Autonomous GPT"
authors: "Yifan Zhang, Cheng Wei, Shangyou Wu, Zhengting He, Wenhao Yu"
year: 2023
venue: "arXiv preprint"
link: https://arxiv.org/abs/2307.07930
code: none found
category: eo-agents
era: recent
tags: [gis-agent, langchain, react, tool-use, gpt-3.5, hallucinated-arguments, input-validation]
verified: "2026-10-05 via https://export.arxiv.org/api/query?id_list=2307.07930 and https://arxiv.org/html/2307.07930"
takeaway: "Early GIS tool agent that openly reports run-to-run instability and hallucinated file and tool arguments; its tool-side input validation is a cheap guard SatClip should copy for every instrument"
---

# GeoGPT: Understanding and Processing Geospatial Tasks through An Autonomous GPT

## Problem
Solving a GIS task (for example siting a facility) means chaining tools such as Buffer, Intersect and Erase in the right order. Professionals can do it; non-experts cannot. The authors ask whether an LLM can do the chaining from a plain-language request.

## Approach
GeoGPT uses LangChain to connect gpt-3.5-turbo (temperature 0) to a pool of hand-written GIS tools in an AutoGPT/ReAct style loop: think, choose a tool, call it, observe, repeat until the model decides it is done. Tools cover data collection (POI search for Chinese cities, road networks, remote sensing image download), processing and analysis (buffer, clip, intersect and similar), and visualisation. Each tool has a natural-language description telling the LLM what input string format it expects.

## Data and benchmarks
No benchmark. Four illustrative case studies: geospatial data crawling, facility siting, spatial query and mapping, using POI and road data (cases centred on Chinese cities, for example hotels near subway stations and a university in Wuhan).

## Key results
- The case studies complete successfully and are shown step by step.
- The Discussion is the most useful part: the authors report that identical settings can give different results or outright failure, and that adding or removing small words such as "the" or a digit can change the outcome.
- They describe hallucinated files and tools, for example passing the plain name "Subway Stations" instead of a file path to Buffer.
- Mitigation is a "protection mechanism": tools pre-check their inputs (for example geometry dimension rules for Clip) and return a structured error message prompting the LLM to recheck file existence, format, order or tool choice.

## Limitations
- No quantitative evaluation, no success rates, no comparison of models.
- Only a handful of tools and cases; results rely on prompt and tool-description tuning.
- Instability is acknowledged but not measured.

## What it means for SatClip
- Strong evidence for SatClip's design choice that the LLM must not produce numbers: even in simple vector GIS, the agent's output changed with trivial wording.
- Adopt the protection mechanism idea as strict schema validation: every instrument call (AOI, date window, polarisation, threshold) is validated before execution, and an invalid call becomes an abstention with a reason, not a retry loop that can drift.
- Measure what GeoGPT did not: run each evaluation question several times with paraphrases and report how often the routed instrument and parameters stay identical.
