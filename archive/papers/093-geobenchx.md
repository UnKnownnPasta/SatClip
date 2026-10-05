---
id: 093
title: "GeoBenchX: Benchmarking LLMs in Agent Solving Multistep Geospatial Tasks"
authors: "Varvara Krechetova, Denis Kochedykov"
year: 2025
venue: "1st ACM SIGSPATIAL International Workshop on Generative and Agentic AI for Multi-Modality Space-Time Intelligence (GeoGenAgent 2025)"
link: https://arxiv.org/abs/2503.18129
code: https://github.com/Solirinai/GeoBenchX
category: eo-agents
era: recent
tags: [benchmark, tool-calling, unsolvable-tasks, rejection, llm-as-judge, gis, abstention]
verified: "2026-10-05 via https://export.arxiv.org/api/query?id_list=2503.18129 and https://arxiv.org/html/2503.18129 (v2, October 2025, workshop header on the paper)"
takeaway: "Only geo-agent benchmark here that scores refusal on deliberately unsolvable tasks; shows models trade answering for refusing, which supports SatClip's explicit abstention and gives a test design to copy"
---

# GeoBenchX: Benchmarking LLMs in Agent Solving Multistep Geospatial Tasks

## Problem
Commercial GIS teams want to know which LLM to put behind a tool-calling geospatial assistant, and whether it will admit when a task cannot be done with the tools and data it has instead of producing a plausible but wrong answer.

## Approach
A deliberately simple tool-calling agent with 23 geospatial functions (loading data, joins, filters, buffers, maps and similar) so that the benchmark measures the LLM rather than an agent architecture. Tasks come in four groups of rising complexity. Some tasks are intentionally unsolvable with the given tools or data, and the correct behaviour is to reject. Evaluation compares the agent's sequence of tool calls with reference solutions using a panel of LLM judges (GPT-4.1, Claude Sonnet 3.5, Gemini 2.5 Pro Preview), scoring match, partial match or no match. The judges were tuned on 50 manually scored tasks, matching human scores 96%, 94% and 88% of the time respectively.

## Data and benchmarks
- 202 tasks, of which 79 are unsolvable.
- Eight commercial models: Claude Sonnet 3.5 and 4, Claude Haiku 3.5, Gemini 2.0 Flash, Gemini 2.5 Pro Preview, GPT-4o, GPT-4.1, o4-mini.
- Benchmark set, evaluator and task generation pipeline are open source.

## Key results
- The best success rates on solvable tasks are only about half (0.55 and 0.51); most models succeed in under half of cases.
- Clear trade-off between solving and rejecting: Claude Sonnet 4 had a solvable-task success rate more than three times its unsolvable-task (rejection) rate, preferring to give some answer; GPT-4o and o4-mini were better at rejecting than at solving.
- o4-mini and Claude 3.5 Sonnet were best overall.
- On unsolvable tasks, candidate solutions are much longer than references, showing models trying many calls before giving up.
- Common errors: misreading geometric relationships, relying on outdated world knowledge, inefficient data handling. Anthropic models used notably more tokens.

## Limitations
- Stated by the authors: no per-model prompt tuning, only the solution algorithm is judged (not the final numbers or the wording of a rejection), moderate set size, no measurement of response variance beyond binomial bounds.
- Vector and tabular GIS, not imagery.

## What it means for SatClip
- Copy the design: include deliberately unanswerable questions (outside India, no Sentinel-1 pass in the window, crop question in a non-crop district) and report rejection accuracy next to answer accuracy.
- The trade-off result supports moving abstention out of the LLM: SatClip abstains on calibrated instrument confidence, so the decision does not depend on a model's disposition to please.
- Note the gap SatClip addresses: GeoBenchX checks whether the plan was right but not whether the number was right. SatClip's receipts let us verify both.
