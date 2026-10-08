---
id: 177
title: "TerraBench: Can Agents Reason Over Heterogeneous Earth-System Data?"
authors: "Dat Tien Nguyen, Thao Nguyen, Fadillah Adamsyah Maani, Huy M. Le, Muhammad Umer Sheikh, Numan Saeed, Muhammad Haris Khan, Salman Khan"
year: 2026
venue: "arXiv preprint (arXiv:2606.13148, v1 11 June 2026, v2 1 July 2026); no peer-reviewed venue found"
link: https://arxiv.org/abs/2606.13148
code: "No code or data link found in the arXiv text read"
category: rs-benchmark
era: upcoming
tags: [eo-agents, tool-use, benchmark, numeric-tolerance, provenance, sentinel-2, era5, simulation, react]
verified: "2026-10-08 via curl to https://export.arxiv.org/api/query (title, authors, dates, abstract) and curl to https://arxiv.org/html/2606.13148 (introduction, framework, benchmark construction, failure analysis); WebFetch permission request timed out; per-track and per-model tables beyond those quoted were not checked"
takeaway: "403-task Earth-science agent benchmark that scores numbers against tolerances and audits provenance; best model Claude Sonnet 4.6 gets 59.2 on tool use but only 22.9% of numeric answers within tolerance, so tool access alone does not give correct quantities and SatClip must validate tool arguments in code"
---

# Nguyen et al. 2026, TerraBench

## Problem
Earth-science questions mix satellite imagery, gridded reanalysis, GIS layers and simulators. Existing agent benchmarks mostly check whether the agent called the right tools in the right order, which hides cases where the trace looks fine but the final number is wrong.

## Approach
- TerraAgent: a ReAct-style executable framework with 77 sub-tools (reanalysis and forecasts such as ERA5, Pangu-Weather and Aurora wrappers; Sentinel-2 retrieval and index computation through Google Earth Engine; OpenStreetMap and GIS operations; deterministic simulators; web search; a code execution server).
- Design rule: the LLM plans, but every quantity must come from retrieval, processing, simulation or explicit computation. Outputs are artifacts (NetCDF, GeoTIFF, CSV, PNG) plus a provenance-bearing trace.
- Each item is a question with a structured output schema, a canonical trace, tool observations, artifacts and a verified answer. Items are tagged with reasoning levels 0 to 3 (observational grounding up to counterfactual).
- Semi-automated, human-in-the-loop annotation: 792 candidates filtered to 403 items; most accepted items needed several execution passes.
- Scoring separates process (ToolUseScore) from outcome (NumScore and Hit@tol, a tolerance-aware numeric match).

## Data and benchmarks
403 tasks, about 24,500 verified execution steps, three tracks (Fundamentals, Simulator-Grounded, Document-Grounded Verification) and eight domains including emergency response, water resources, agriculture and cyclones. Many traces run 50 to 60 steps over 5 to 6 tool groups.

## Key results
- Claude Sonnet 4.6: 59.22 ToolUseScore, 28.44 NumScore, 22.88 Hit@tol. Best open model Qwen3.5-35B: 39.95, 7.49, 5.89.
- Large process-versus-outcome gap: a model can choose tools well and still miss the number.
- Dominant failures: wrong argument values (69.5% to 96.8% across models), wrong tool order and numeric misses beyond tolerance. Simulator-grounded tasks are hardest.
- Bootstrap intervals show the benchmark separates models despite its small size.

## Limitations
- Small (403 items) and expensive to build; inter-annotator agreement was audited only on a subset, and an independent expert audit is described as future work.
- Imagery is a minor component (Sentinel-2 indices via Earth Engine); no SAR, flood mapping or change detection workflow is described in the parts read.
- No calibration, confidence or abstention scoring.
- Depends on Earth Engine and online services, unlike an offline deployment.

## What it means for SatClip
- Adopt: score SatClip's eval on numeric tolerance (flooded hectares within a stated band) and on provenance completeness, not just tool choice; TerraBench shows the two diverge sharply.
- Adopt: wrong argument values are the top failure, so SatClip's parsed intent (district, date window, instrument) must pass a code-side validator against the scene catalog before any tool runs, rather than trusting the VLM's arguments.
- Beat: TerraBench never asks whether the agent should have declined; SatClip's abstention on low instrument confidence is a dimension this benchmark does not measure.
