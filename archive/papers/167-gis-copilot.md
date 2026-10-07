---
id: 167
title: "GIS Copilot: Towards an Autonomous GIS Agent for Spatial Analysis"
authors: "Temitope Akinboyewa, Zhenlong Li, Huan Ning, M. Naser Lessani"
year: 2025
venue: "International Journal of Digital Earth, 18(1), article 2497489 (2025); arXiv preprint November 2024"
link: https://doi.org/10.1080/17538947.2025.2497489
code: "Not verified (no repository named in the arXiv abstract)"
category: eo-agents
era: recent
tags: [gis-agent, qgis, code-generation, autonomous-gis, non-experts, natural-language-interface, tool-documentation]
verified: "2026-10-07 via curl to https://export.arxiv.org/api/query?id_list=2411.03205 (title, authors, abstract) and api.crossref.org (journal, volume, issue, article number, 2025-04-28 date); success-rate figures are not in the abstract and were not verified"
takeaway: "A natural-language agent inside QGIS that writes and runs analysis code, aimed partly at non-experts; strong on one- and few-step tasks but not on autonomous multi-step ones, and it offers no calibrated confidence, abstention or provenance card, which is the gap SatClip fills"
---

# Akinboyewa et al. 2025, GIS Copilot

## Problem
Generative AI could make spatial analysis accessible, but it is rarely integrated into the GIS software people already use.

## Approach
- Integrates an LLM directly into QGIS.
- The agent is given documentation of key GIS tools and parameters, then generates spatial analysis workflows and code from natural-language commands.
- Builds on the Autonomous GIS vision from the same group (entry 091).

## Data and benchmarks
- Over 100 spatial analysis tasks at three levels: basic (one tool, usually one layer), intermediate (multi-step, guided by the user), and advanced (multi-step, agent decides the steps).

## Key results
- High success in tool selection and code generation for basic and intermediate tasks (exact rates not in the abstract, not verified).
- Full autonomy on advanced tasks is not yet achieved, by the authors' own account.

## Limitations
- Generated code is the answer path, so correctness depends on the LLM each time; no calibrated confidence or abstention is described.
- Needs QGIS and prepared data layers; it does not find and process satellite scenes for the user.
- Evaluation is a curated task set, not field use by officials.

## What it means for SatClip
- **Closest prior art for the 'non-expert asks in plain language' framing**, so SatClip must state the difference clearly: GIS Copilot helps a user drive a GIS; SatClip hands a non-GIS official a measured answer with scene IDs, a mask, calibrated confidence and an abstain path.
- **Avoid** free code generation as the answer path; its weak advanced-task results echo GeoGPT (entry 090) and Earth-Agent (entry 094).
- **Adopt** its use of tool documentation in the prompt for SatClip's parser, limited to describing which instruments exist and what they cannot answer.
- Offer a QGIS export of SatClip's mask and receipt so GIS staff can inspect cards in the tool they already use.
