---
id: 204
title: "Towards LLM Agents for Earth Observation"
authors: "Chia Hsiang Kao, Wenting Zhao, Cheryl Lam, Aarush Umap, Shreelekha Revankar, Samuel Speas, Snehal Bhagat, Rajeev Datta, Cheng Perng Phoo, Utkarsh Mall, Carl Vondrick, Kavita Bala, Bharath Hariharan"
year: 2026
venue: "ACL 2026 Findings (per arXiv comment and an ACL Anthology preview page listing 2026.findings-acl.124); earlier ICML 2025 TerraBytes workshop; arXiv:2504.12110 (v1 April 2025, v3 5 October 2026)"
link: https://arxiv.org/abs/2504.12110
code: "Dataset and project page https://iandrover.github.io/2025_univearth/ (per the paper; page not opened)"
category: rs-benchmark
era: recent
tags: [univearth, google-earth-engine, code-agents, live-data-retrieval, nasa-earth-observatory, hallucinated-collection-ids, reflexion, yes-no-qa, failure-taxonomy]
verified: "2026-10-09 via curl to https://export.arxiv.org/api/query?id_list=2504.12110 (title, authors, v3 date, ACL 2026 Findings comment, abstract) and curl of https://arxiv.org/html/2504.12110v3 (benchmark construction, Table 1 sources, Table 3 results, collection-ID hallucinations, reflexion results, Limitations); WebFetch of arxiv.org was rate limited (HTTP 429); ACL Anthology page seen only as a search result, not opened"
takeaway: "UnivEARTH (408 yes/no questions from NASA Earth Observatory) makes LLM agents fetch live data by writing Google Earth Engine code: best zero-shot accuracy 40.0%, code fails over 44% of the time, collection IDs are hallucinated, and reflexion lifts the best model to 64.5%; the strongest evidence that free-form code agents over live archives are unreliable, which favours SatClip's fixed instruments"
---

# Kao et al. 2026, UnivEARTH

## Problem
Most EO agent benchmarks use curated images and predefined tools. Real EO questions require choosing the right sensor, product, place and date from a large live catalogue, which earlier benchmarks do not test.

## Approach
- 408 yes/no questions mined from NASA Earth Observatory articles (cutoff 30 September 2025), each checked to be answerable with data available in Google Earth Engine (GEE), then reviewed by two or more student reviewers until consensus.
- Agents must plan, write a GEE Python script, run it against the live catalogue, and a judge model (Gemini-2.5-Flash) derives the final answer from the output.
- Failure taxonomy: empty collection, no valid pixels after masking, calculation failure, and code or syntax error.
- Variants: Python vs JavaScript API, injecting correct collection IDs and band names, and reflexion (up to two debugging rounds on execution errors).

## Data and benchmarks
- Topics: hydrosphere (34%, including surface water extent and precipitation), temperature, land cover, atmosphere, fire, human activity, geology.
- Main sources: Landsat 4 to 9, MODIS, VIIRS, Sentinel-5P, GRACE, GPM, CHIRPS and others; Sentinel-2 appears in only two questions and Sentinel-1 is not listed in the source table.
- Models: Gemini-2.5-Pro and Flash, Claude-4.5-Sonnet and Haiku, GPT-5, DeepSeek-Reasoner and Chat, Kimi-k2.

## Key results
- Best zero-shot accuracy 40.0% (Claude-4.5-Sonnet), then Gemini-2.5-Pro 36.9% and GPT-5 33.1%; Flash, Haiku and Kimi below 20%.
- Syntax and method errors 21.4% for the best model and above 30% for all others; empty collections around 15% for most.
- Typical hallucinated GEE collection IDs are wrong version or tier strings (Table 4).
- Supplying correct collection IDs cut errors (for example VIIRS accuracy 38.2% to 61.5% for Claude) but exposed more wrong answers.
- Reflexion: Claude-4.5-Sonnet 40.0% to 64.5%, GPT-5 33.1% to 59.3%; wrong-answer rate rose at the same time (15.7% to 26.0% for Claude), so running code is not correct code.
- The authors themselves call these scores only marginally above chance for a yes/no task.

## Limitations
- No unanswerable or inconclusive questions (the authors list this as a limitation), so abstention is not measured.
- Yes/no only; reviewers were computer science students checking against article text, not domain experts.
- No calibration, confidence or provenance output is evaluated, though the code itself is an implicit receipt.
- Dependent on GEE; the text calls GPT-5's 33.1% to 59.3% change a 79 percentage point increase, when it is about 26 points (79% relative), so read numbers from the tables.

## What it means for SatClip
- Avoid: letting an LLM write retrieval or analysis code at query time. UnivEARTH shows that even frontier models pick wrong collections, empty date windows and broken cloud masks; SatClip's fixed STAC queries and fixed instruments avoid all four failure classes.
- Adopt: the failure taxonomy (empty collection, no valid pixels, calculation failure) maps directly onto SatClip's abstention reasons; an empty Sentinel-2 window or all-cloud scene should trigger the SAR fallback or an explicit abstain with the reason in the receipt.
- Adopt: add unanswerable questions to SatClip's evaluation set, the gap the authors name.
- Novelty: weakens the claim slightly on one axis. It shows live satellite data retrieval by a language agent from natural-language questions is already published and peer reviewed (ACL Findings 2026), so live retrieval alone is not new. It has no calibrated confidence, abstention, SAR fallback or non-expert delivery, and its low accuracy is an argument for SatClip's constrained design rather than against its novelty.
