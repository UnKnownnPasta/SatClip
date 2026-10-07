---
id: 139
title: "Eviza: A Natural Language Interface for Visual Analysis"
authors: "Vidya Setlur, Sarah E. Battersby, Melanie Tory, Rich Gossweiler, Angel X. Chang"
year: 2016
venue: "UIST 2016 (Proceedings of the 29th Annual Symposium on User Interface Software and Technology, pp. 365-377)"
link: https://doi.org/10.1145/2984511.2984588
code: "none found (Tableau Research prototype)"
category: human-factors
era: historical
tags: [natural-language-interface, visual-analytics, ambiguity-widgets, spatial-queries, pragmatics]
verified: "2026-10-07 via https://api.crossref.org/works/10.1145/2984511.2984588 (title, authors, pages, date 2016-10-16) and Semantic Scholar abstract; full text not fetched, so details of the user evaluation are not stated here"
takeaway: "When a question is ambiguous (which district, which date, what counts as flooded), SatClip should show the default it chose as an editable chip, as Eviza's ambiguity widgets do, rather than silently guessing or refusing"
---

# Setlur et al. 2016, Eviza

## Problem
Natural-language interfaces to data often return a single static answer or chart to closed questions, and need experts to model expected queries in advance. They also handle vague language (such as "near", "recent", "large") poorly.

## Approach
- Lets users converse with an existing visualization (including maps), so each query changes the current view through filtering, navigation or selection rather than starting from scratch.
- Uses a probabilistic grammar with predefined rules that update dynamically from the data in the visualization, instead of heavy deep learning or knowledge-base methods.
- Shows ambiguity widgets: when a query is ambiguous or the system applies a default (for example a distance for "near" or a threshold for "high"), it exposes that choice as an adjustable control.
- Built-in awareness of time, space and quantities, links to knowledge bases for extra semantics, support for follow-up queries (pragmatics) and multimodal input.

## Data and benchmarks
Prototype system with example datasets including geographic data; the paper includes a preliminary user evaluation whose size and metrics were not verified for this entry.

## Key results
- Demonstrates that a lightweight grammar plus visible, editable defaults can support an interactive question dialogue over spatial and temporal data.
- Ambiguity widgets make system assumptions inspectable and correctable by the user. Quantitative results were not verified.

## Limitations
- Rule-based grammar has limited coverage compared with modern language models.
- Prototype, not a deployed product; evaluation was small and preliminary as described by the authors (details not confirmed here).
- English only; no multilingual or low-literacy users.

## What it means for SatClip
- Every assumption SatClip makes when parsing a question (district boundary, date window, flood definition threshold, sensor chosen) should appear on the evidence card as a chip the user can tap to change, extending the scene and date chips already planned.
- Distinguish two "no answer" cases: ambiguity (resolve with a chip and a sensible default) versus insufficient evidence (abstain). Do not abstain when a clarifying default would do.
- Pairs with NL4DV (068): NL4DV gives the inspectable spec, Eviza shows how to surface its ambiguous parts in the UI.
- Hindi and other Indian-language vague terms ("aas paas", "pichle hafte") need explicit default mappings, tested with users.
