---
id: 094
title: "Earth-Agent: Unlocking the Full Landscape of Earth Observation with Agents"
authors: "Peilin Feng, Zhutao Lv, Junyan Ye, Xiaolei Wang, Xinjie Huo, Jinhua Yu, Wanghan Xu, Wenlong Zhang, et al."
year: 2025
venue: "ICLR 2026"
link: https://arxiv.org/abs/2509.23141
code: https://github.com/opendatalab/Earth-Agent
category: eo-agents
era: recent
tags: [mcp, tool-use, spectral, ndvi, ndwi, landsat, modis, benchmark, parameter-accuracy, tool-hallucination]
verified: "2026-10-05 via https://export.arxiv.org/api/query?id_list=2509.23141 (comment: published at ICLR 2026), https://arxiv.org/html/2509.23141 and the ICLR 2026 virtual poster listing found by web search"
takeaway: "Most capable EO tool agent to date (104 MCP tools, spectral indices, GEE products) and the closest competitor to SatClip's instrument idea, yet GPT-5 matches tool parameters only about 26% of the time and there is no calibration, abstention or receipt"
---

# Earth-Agent: Unlocking the Full Landscape of Earth Observation with Agents

## Problem
Multimodal LLMs answer RGB perception questions but cannot do quantitative, multi-step Earth science (computing indices, retrieving geophysical parameters, analysing time series). Earlier EO agents are RGB-only, shallow, and lack systematic evaluation.

## Approach
An agent framework that exposes 104 specialised tools through the Model Context Protocol (MCP), grouped into five kits: Index, Inversion, Perception, Analysis and Statistics. The LLM plans and calls tools across raw spectral data, processed products and RGB imagery. Two regimes are tested: Auto-Planning (the model plans freely) and Instruction-Following (the task gives step hints).

## Data and benchmarks
- Earth-Bench: 248 expert-curated tasks over 13,729 images in three modalities (Spectrum, Products, RGB).
- Sources: mainly Landsat 8/9 and MODIS (plus ASTER), Google Earth Engine products (LST, NDVI, NDWI, GPM precipitation, VIIRS, GHSL, fire, QA bands), and RGB sets such as AID, DOTA, NWPU-VHR-10 and xBD.
- Dual-level evaluation. End-to-end: answer accuracy and trajectory efficiency versus the expert path. Step-by-step: Tool-Any-Order (all needed tools used), Tool-In-Order (correct sequence), Tool-Exact-Match (exact prefix match with the expert trajectory) and Parameter Accuracy (tool and arguments both match).
- Earth-Bench-Lite (60 questions) for comparing against general agents (GPT-Agent, MGX, Manus).

## Key results
- Auto-Planning answer accuracy: GPT-5 65.99, Gemini-2.5 52.23, GPT-4o 43.72.
- Parameter Accuracy is far lower than answer accuracy: GPT-5 26.11, Gemini-2.5 17.26 under Auto-Planning, meaning many correct-looking answers come from trajectories whose arguments do not match the expert's.
- Error taxonomy: not recognising when to stop (repeating calls to the step limit), tool hallucination (calling tools that do not exist), file hallucination (invalid paths), invalid parameters, and system errors. The authors suggest open models trained with RL are more exploratory and hallucinate more.
- On Earth-Bench-Lite the general agents lag (GPT-Agent averages 40.42 and Manus 26.14), with latencies of hours.

## Limitations
- Answers have no confidence, no abstention, and no stated provenance record for end users; evaluation assumes every task is answerable.
- No SAR modality, which matters for monsoon cloud cover.
- Low parameter accuracy means results can be right for the wrong reasons; reruns may not reproduce.

## What it means for SatClip
- This is the work that most challenges SatClip's novelty claim: it grounds numbers in real spectral instruments (NDVI, NDWI and others) rather than LLM guesses. SatClip's claim should be narrowed to the combination Earth-Agent lacks: SAR-first flood instruments, calibrated confidence, abstention below threshold, and a re-runnable receipt with scene IDs.
- Adopt its four trajectory metrics, especially Parameter Accuracy, for SatClip's router evaluation; with a small fixed instrument set SatClip should aim far above 26%.
- Its failure taxonomy (tool, file and parameter hallucination, no stop condition) is a ready checklist of things SatClip's typed router and schema validation must make impossible, and our evaluation should count each one.
