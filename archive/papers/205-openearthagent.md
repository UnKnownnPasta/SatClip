---
id: 205
title: "OpenEarthAgent: A Unified Framework for Tool-Augmented Geospatial Agents"
authors: "Akashah Shabbir, Muhammad Umer Sheikh, Muhammad Akhtar Munir, Hiyam Debary, Mustansar Fiaz, Muhammad Zaigham Zaheer, Paolo Fraccaro, Fahad Shahbaz Khan, Muhammad Haris Khan, Xiao Xiang Zhu, Salman Khan"
year: 2026
venue: "ECCV 2026 (per arXiv comment); arXiv:2602.17665 (v1 February 2026, v4 July 2026)"
link: https://arxiv.org/abs/2602.17665
code: "https://github.com/mbzuai-oryx/OpenEarthAgent (stated in the paper as code, data and models; repository not inspected)"
category: eo-agents
era: recent
tags: [tool-registry, deterministic-replay, trajectory-sft, qwen3-4b, ndvi, nbr, ndbi, google-earth-engine, gis-tools, sar, agent-benchmark]
verified: "2026-10-09 via curl to https://export.arxiv.org/api/query?id_list=2602.17665 (title, authors, dates, ECCV 2026 comment, abstract) and curl of https://arxiv.org/html/2602.17665v4 (tool categories, replay validation, data sources, Tables 3, 4 and 6 numbers, conclusion, tool memory footprint); WebFetch of arxiv.org was rate limited"
takeaway: "A 4B agent (Qwen3-4B fine-tuned on 14.5k replay-validated tool trajectories) that runs NDVI/NBR/NDBI change, GIS and detection tools through one executable schema; end-to-end answer accuracy 45.26 vs 13.72 for its base model and 39.22 for GPT-4o; its replayable tool traces are close to SatClip's receipts, but there is no confidence, abstention or live scene retrieval"
---

# Shabbir et al. 2026, OpenEarthAgent

## Problem
EO agents (ThinkGeo, entry 92; Earth-Agent, entry 94) plan tool chains but mis-order calls, pass wrong arguments and give outputs that cannot be re-run. The authors want a trainable agent whose every step executes and can be replayed.

## Approach
- A unified tool registry with one callable schema for perception tools (detection, text-to-box, counting), GIS tools (area boundary, POI layers, distance), spectral tools (AddIndexLayer, ComputeIndexChange for NDVI, NBR, NDBI), georeferenced raster tools and utilities (calculator, solver, search).
- A tool execution cache stores intermediate layers so a trajectory can be deterministically replayed.
- Every training trajectory is re-executed before use to check argument format, coordinates, geometry and full-chain executability.
- Supervised fine-tuning of Qwen3-4B-Instruct-2507 on the validated trajectories (four A100 40 GB GPUs, one epoch); tool observations are masked from the loss.

## Data and benchmarks
- 14,538 training and 1,169 evaluation instances, over 107k reasoning steps, across urban, environmental, disaster, transport and infrastructure themes.
- Sources: DOTA, DIOR, xBD, AID, NWPU-VHR-10, FloodNet, Global-Dumpsite, plus Sentinel collections and Google Earth Engine archives; index samples are mined from temporal changes in vegetation, burn severity or flooding.
- Two protocols: step-by-step (no execution) and end-to-end with live tool calls; answers judged by gpt-4o-mini with 10% numeric tolerance or IoU thresholds.

## Key results
- Step-by-step: instruction, tool, argument-name and argument-value accuracy 99.51 / 97.18 / 96.08 / 62.10, the best in the table, though frontier models score higher on final summary accuracy (o4-mini 89.48).
- End-to-end answer accuracy 45.26 vs 13.72 for the Qwen3-4B base, 39.22 for GPT-4o and 43.88 for GPT-5; tool-order accuracy about 67 to 72%.
- On a 60-query subset vs a general GPT agent: 60.04 vs 21.75 overall, about 22 s per query vs about 934 s.
- Full tool stack needs about 45 GB of runtime memory during evaluation.

## Limitations
- Still under half of end-to-end answers correct on its own benchmark.
- Training data and questions are synthesised by an LLM pipeline from existing datasets; image chips rather than live scene search by date and place.
- No confidence, calibration or abstention; the judge scores fabricated or missing outputs as zero but the agent never declines.
- Deterministic replay checks that a trajectory runs, not that its answer is right (a point also made by the survey in entry 209).
- The memory footprint and Qwen3-VL-7B dependency make CPU-only deployment unlikely without trimming.

## What it means for SatClip
- Adopt: the single executable tool schema plus a cache of intermediate layers is a good pattern for SatClip's receipt: store the STAC item IDs, the threshold, the mask hash and the computed numbers so the answer replays exactly.
- Adopt: validate each answer path by re-execution in CI, as they do for training data.
- Beat: SatClip's fixed instrument chain avoids the tool-ordering errors that dominate their failure analysis, and adds calibrated confidence and abstention, which they lack.
- Novelty: weakens the claim a little. Replayable, tool-grounded NDVI and index-change answers from a small open agent (ECCV 2026) mean "re-runnable receipt" and "index-change instruments" are not new alone. It has no calibrated confidence, abstention, live date-aware Sentinel retrieval, SAR fallback or non-expert Indian delivery, so the combination claim stands.
