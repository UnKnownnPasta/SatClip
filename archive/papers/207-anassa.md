---
id: 207
title: "ANASSA: An Agentic AI Orchestration Framework for Spatial Intelligence"
authors: "Constantinos Papantoniou, Brian Hilton"
year: 2026
venue: "arXiv preprint arXiv:2609.14824 (v1 13 September 2026); no venue stated; first author affiliated with Anassa.ai (a company of the same name)"
link: https://arxiv.org/abs/2609.14824
code: "None; architecture specification only"
category: eo-agents
era: upcoming
tags: [agentic-gis, architecture-spec, provenance, uncertainty-states, human-in-the-loop, governance, authoritative-data, insufficient-evidence, no-evaluation]
verified: "2026-10-09 via curl to https://export.arxiv.org/api/query?id_list=2609.14824 (title, authors, date, abstract) and curl of https://arxiv.org/html/2609.14824v1 (affiliations, contributions, validation output states, conclusion, statement that empirical evaluation is deferred)"
takeaway: "A design-only specification for agentic GIS (eleven components, a six-step cognitive loop) that requires provenance, uncertainty propagation and explicit outcome states such as validated-with-uncertainty and insufficient-evidence; no implementation or results, but it names SatClip's trust features as requirements, so SatClip's claim must rest on a working, measured system"
---

# Papantoniou and Hilton 2026, ANASSA

## Problem
Agentic GIS systems connect LLM reasoning to geospatial tools, but reasoning, execution, validation, governance and provenance are built as separate pieces. The authors argue this leaves no consistent way to make agent outputs traceable and accountable.

## Approach
- An architecture of eleven components in four layers, plus a six-step Geospatial AI Cognitive Loop: sensing, reasoning, planning, decision with hallucination validation, execution, learning.
- A spatial validation stage checks outputs against authoritative sources, with checks for data freshness and staleness, uncertainty propagation from data through models to outputs, jurisdiction and source authority, and conflicting sources.
- Validation does not return just pass or fail: possible states are validated, validated with uncertainty, conflicting authoritative evidence, insufficient evidence, or rejected, each carrying the evidence and checks behind it.
- Human decision authority and governance controls sit over execution.
- The authors explicitly do not claim novelty for orchestration, human approval, feedback loops or authoritative-data checks individually, only for their integration.

## Data and benchmarks
- None. The paper synthesises prior agentic GIS frameworks and benchmarks and states that empirical evaluation is left to later implementation studies.

## Key results
- No quantitative results. Contributions are the architecture, the loop, interface contracts and a list of research questions and requirements.

## Limitations
- No implementation, no data, no measurements; all claims are design intentions.
- Company-affiliated position paper, not peer reviewed as of the verification date.
- Uncertainty handling is described at the level of requirements; no calibration method is specified.
- Not specific to satellite imagery; EO is one data source among many.

## What it means for SatClip
- Adopt: the outcome states are a good vocabulary for SatClip's answer card. Mapping SatClip's outputs to answered, answered-with-low-confidence (below display threshold but above abstain), insufficient evidence (no usable scene), and conflicting evidence (optical and SAR disagree) would make abstentions more informative to a district official.
- Adopt: data staleness as an explicit check; SatClip should state the age of the newest usable scene in every answer and abstain when it exceeds the question's window.
- Novelty: weakens the claim only on paper. It shows that provenance, uncertainty and insufficient-evidence outcomes are already proposed as design goals for geospatial agents, so SatClip should not present the idea of combining them as new. Because ANASSA has no implementation or evaluation, SatClip's novelty shifts to being a working, measured system with calibrated confidence on real Sentinel scenes; SatClip should cite it as a design-level precursor.
