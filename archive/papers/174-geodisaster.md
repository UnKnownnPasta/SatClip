---
id: 174
title: "GeoDisaster: Benchmarking Orchestrated Agents for Operational Disaster Geo-Intelligence"
authors: "Maram Hasan, Aman Verma, Savitra Roy, Hariseetharam Gunduboina, Daksh Jain, Muhammad Haris Khan, Subhasis Chaudhuri, Biplab Banerjee"
year: 2026
venue: "arXiv preprint (arXiv:2606.17246, v1 15 June 2026); no peer-reviewed venue found"
link: https://arxiv.org/abs/2606.17246
code: "https://github.com/VIMAGE-IITB/GeoDisaster (linked in the HTML full text; not fetched)"
category: upcoming
era: upcoming
tags: [benchmark, eo-agents, disaster, sentinel-1, sar-flood, sen1floods11, tool-use, multi-agent, grpo, iit-bombay, executable-ground-truth]
verified: "2026-10-07 via curl to https://export.arxiv.org/api/query (title, authors, date, abstract) and curl to https://arxiv.org/html/2606.17246v1 (task table, metrics, main results text, conclusion, code link); WebFetch permission request timed out"
takeaway: "An Indian (IIT Bombay) 2026 benchmark whose answers come from executable geospatial workflows, including a 500-item Sentinel-1 SAR flood family; a ready external test for SatClip, and its own authors name uncertainty-aware reasoning as the open gap SatClip targets"
---

# Hasan et al. 2026, GeoDisaster benchmark and RCEA agents

## Problem
RS VLMs interpret images and follow instructions, but operational disaster work needs tool-grounded spatial reasoning and structured, evidence-backed decisions that current models do not deliver.

## Approach
- Benchmark: 2,921 verified instances, 43 question types, five families: deforestation monitoring, multi-hazard analysis, building damage, flood-safe routing, and Sentinel-1 SAR flood monitoring (500 instances built from Sen1Floods11, Sentinel-1/2 and JRC surface water).
- Inputs mix optical and SAR imagery, raster masks, vector geometries, road networks and exposure layers (WorldPop, WorldCover, OSM).
- Ground truth comes from executable geospatial workflows and deterministic consistency checks, not from LLM annotation.
- Agent system: role-specialised agents with 18 disaster tools coordinated through explicit execution contracts, aligned with RCEA (failure-aware SFT plus contract-grounded GRPO with dense step-level rewards). Default backbone Qwen2.5-7B-Instruct.

## Data and benchmarks
Metrics cover tool-sequence fidelity, task success, answer accuracy, contract satisfaction and step-wise quality, all scored by GPT-5.5 as judge. Baselines include open LLMs and VLMs, GPT-4o, GPT-5, GPT-5.5 and o4-mini.

## Key results
- Open-source LLMs prompted alone nearly fail (near-zero tool fidelity and answer accuracy).
- GPT-5.5 has the best single-model answer accuracy (61.99) but low tool-chain fidelity (ToolAnyOr 20.93), so correct answers often do not come from valid tool runs.
- Multi-agent plus SFT reaches 82.43 answer accuracy; adding GRPO reaches 90.11 answer accuracy and 94.24 task success.
- Remaining errors are linked to ambiguous evidence, wrong metric choice and constraint-aware synthesis.

## Limitations
- LLM-as-judge scoring for all metrics may reward fluent but subtly wrong reports.
- No calibrated confidence or abstention is evaluated; the authors list uncertainty-aware reasoning as future work.
- SAR flood items come from Sen1Floods11 chips, not live Indian scenes, and the agent stack (7B plus 18 tools) is GPU oriented.

## What it means for SatClip
- Adopt: run SatClip on the SAR flood monitoring family as an external, deterministic test; its executable answers fit SatClip's receipts well.
- Adopt: copy the idea of explicit execution contracts between the parser and instruments, so each step's inputs and outputs are checked and logged.
- Beat: add what GeoDisaster lacks: a calibrated confidence per answer and a scored abstain option, measured with a risk and coverage curve rather than an LLM judge.
- Watch: same Indian research community (IIT Bombay VIMAGE lab); a potential collaborator or a close competitor if they add abstention.
