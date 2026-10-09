---
id: 209
title: "From Perception to Reasoning in Remote Sensing: A Survey and Outlook"
authors: "Jiancheng Pan, Liang Yao, Zilun Zhang, Yijie Zheng, Jiahao Li, Xiao He, Wenjia Xu, Yuqian Fu, Fan Liu, Zhaojun Liu, Jianwei Yin, Xiaomeng Huang"
year: 2026
venue: "Preprints.org preprint, posted 26 August 2026, v1, not peer reviewed; DOI 10.20944/preprints202608.1840.v1"
link: https://www.preprints.org/manuscript/202608.1840
code: "Companion list https://github.com/ML4Sustain/Awesome-RS-Reasoning-Models (linked in the abstract; not opened)"
category: rs-vlm
era: upcoming
tags: [survey, rs-reasoning, agentic-reasoning, rl-reasoning, calibrated-uncertainty, provenance, evaluation-gaps, earth-ai, openearthagent, terraagent]
verified: "2026-10-09 via WebFetch of https://www.preprints.org/manuscript/202608.1840 (title, authors, posting date, abstract, coverage of uncertainty, provenance, agents and benchmarks; the last 2.6k characters and Sections 7 and 8 were truncated) and curl to https://api.crossref.org/works/10.20944/preprints202608.1840.v1 (title, authors, posted date 2026-08-26, preprint type)"
takeaway: "An August 2026 survey that defines RS reasoning as multi-step inference backed by traceable evidence and finds that calibration, abstention and validated operational use are still missing in RS VLMs and EO agents (it cites no work that evaluates them); a useful third-party statement of the gap SatClip fills"
---

# Pan et al. 2026, RS reasoning survey

## Problem
Many recent RS VLM papers claim reasoning, but the term is loose and evaluation mostly checks final answers. The survey sets out what should count as reasoning in remote sensing and what is missing.

## Approach
- Defines RS reasoning as multi-step inference supported by traceable visual, temporal, spatial or tool-derived evidence, judged on more than final-answer accuracy.
- Groups work into three overlapping paradigms: supervised reasoning (CoT fine-tuning), reinforcement-learning-driven reasoning, and agentic or tool-augmented reasoning.
- Separates genuine reasoning methods from models that mainly do alignment, generation or grounding.

## Data and benchmarks
- Reviews agentic systems including Earth AI (entry 95), Earth-Agent (entry 94), OpenEarthAgent (entry 205), TerraAgent, GeoMMAgent, MAP-Agent, VRA and RemoteAgent, and benchmarks including ThinkGeo (entry 92), TerraBench (entry 177), Earth-Bench, GeoMMBench, GeoPlan-bench and VagueEO.
- Covers SAR resources (SAR-TEXT, SARLANG-1M, entry 180) and multi-sensor disaster data (DisasterM3, entry 118).

## Key results
- Four persistent gaps: synthetic training data with unclear provenance, outcome-only evaluation, weak checking of cross-modal evidence, and brittle long-horizon tool use.
- Calibrated uncertainty is listed as a requirement and research agenda item; in the text read, no RS reasoning model or EO agent is cited as having evaluated calibration, abstention or refusal.
- Credits TerraAgent and OpenEarthAgent with exposing intermediate artifacts and replay, but cautions that replay validation does not make planning correct.
- States that current evidence does not establish validated operational deployment, describing Earth AI's case study as a targeted demonstration.
- Research agenda: process-level supervision, constraint checking, calibrated uncertainty, expert feedback, and robustness across sensors, regions and time.

## Limitations
- Not peer reviewed; the reading was truncated before the reproducibility and governance sections, so their content is not verified here.
- Floods appear only as a hypothetical scenario; India is not mentioned in the text read.
- A survey: no new experiments, and its coverage judgments depend on the authors' selection.

## What it means for SatClip
- Adopt: cite the survey as independent support that calibration, abstention and operational validation are open gaps in RS reasoning and EO agents as of August 2026.
- Adopt: its evaluation agenda (process checks, robustness across regions and time) as a checklist for SatClip's evaluation write-up, especially cross-district and cross-season robustness in India.
- Check: TerraAgent, GeoMMAgent, MAP-Agent, VRA, RemoteAgent and VagueEO are not in the archive; they should be screened for confidence or abstention features before SatClip's novelty claim is finalised.
- Novelty: strengthens rather than weakens the claim. A broad 2026 survey finds no RS reasoning system that evaluates calibrated confidence or abstention, which supports SatClip's combination claim, with the caveat that surveys lag preprints and the truncated sections were not read.
