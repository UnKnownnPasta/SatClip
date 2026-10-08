---
id: 194
title: "CangLing-KnowFlow: A Unified Knowledge-and-Flow-fused Agent for Comprehensive Remote Sensing Applications"
authors: "Zhengchao Chen, Haoran Wang, Jing Yao, Jianshe Zhang, Pedram Ghamisi, Jun Zhou, Peter M. Atkinson, Bing Zhang"
year: 2025
venue: "arXiv preprint (arXiv:2512.15231, v1 17 December 2025, v3 4 June 2026); no peer-reviewed venue listed"
link: https://arxiv.org/abs/2512.15231
code: "No code link found in the arXiv record or HTML full text"
category: rs-vlm
era: recent
tags: [agents, workflow-library, procedural-knowledge, gdal, replanning, memory, knowflow-bench, llm-backbones, hallucination]
verified: "2026-10-08 via curl to https://export.arxiv.org/api/query (title, authors, dates, abstract) and curl to https://arxiv.org/html/2512.15231v3 (GDAL toolset, metrics, ablation Table III with Claude 4 Sonnet backbone, per-backbone TSR values); WebFetch permission request timed out"
takeaway: "An RS agent that plans from 1,008 expert workflow templates over GDAL and deep-learning tools and replans on runtime failure, reaching up to 96% task success; it shows template-driven pipelines curb hallucination, but its answers carry no calibrated confidence or abstention, which SatClip adds"
---

# Chen et al. 2025, CangLing-KnowFlow (knowledge-and-flow agent for RS)

## Problem
Automated RS systems are usually built for one task. General LLM agents can chain tools but hallucinate steps and fail on long, data-heavy EO workflows that run from preprocessing to interpretation.

## Approach
- Procedural Knowledge Base: a tool library (the full GDAL algorithm set wrapped as tools plus task-level deep-learning tools) and 1,008 expert-validated workflow cases over 162 RS tasks, stored as directed acyclic graphs.
- Dynamic Workflow Adjustment: when a step fails (cloud cover, sensor noise, a model that does not converge, vague user extents) the agent diagnoses and replans.
- Evolutionary Memory Module: stores failure and recovery events to improve later runs.

## Data and benchmarks
KnowFlow-Bench: 324 workflows inspired by real applications, run with 13 LLM backbones (commercial and open, for example GPT-4, GPT-3.5-Turbo, Claude models, DeepSeek-V3.1, DeepSeek-R1, Llama3-70B). Metrics: task success rate (TSR, result must be semantically and numerically correct), first-pass accuracy, number of tool calls and number of human interactions.

## Key results
- Beats the Reflexion baseline by at least 4 points of TSR on all complex tasks (abstract).
- Ablation with a Claude 4 Sonnet backbone: full model TSR 96.1%, first-pass accuracy 79.2%, 6.8 tool calls; removing the workflow library drops TSR to 88.7% and raises tool calls to 13.2.
- With DeepSeek-R1, TSR is 93.1% for the full framework (from the per-backbone table; table layout made baseline columns hard to attribute, so only this value is cited).

## Limitations
- Success is judged against ground truth workflows, not against field truth, and outputs carry no uncertainty.
- Relies on large hosted or 70B-class LLMs; no small or CPU deployment.
- Benchmark and code not found as public releases.
- No Indian or flood-specific evaluation reported in the passages read.

## What it means for SatClip
- Adopt: the result that removing the workflow library is the biggest loss supports SatClip's fixed, templated flood and crop pipelines instead of free planning.
- Adopt: log runtime failures (no scene, cloud above limit, empty mask) as typed events; they become abstention reasons shown to the user.
- Beat: KnowFlow aims for task completion; SatClip's added value is telling an official how much to trust the number and declining when it should.
