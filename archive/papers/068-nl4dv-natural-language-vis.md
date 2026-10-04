---
id: 068
title: "NL4DV: A Toolkit for Generating Analytic Specifications for Data Visualization from Natural Language Queries"
authors: "Arpit Narechania, Arjun Srinivasan, John Stasko"
year: 2021
venue: "IEEE Transactions on Visualization and Computer Graphics 27(2) (Proceedings of IEEE VIS 2020)"
link: https://doi.org/10.1109/TVCG.2020.3030378
code: https://github.com/nl4dv/nl4dv
category: human-factors
era: recent
tags: [natural-language-interface, visualization, query-parsing, ambiguity, vega-lite, toolkit, nli]
verified: "2026-10-04 via https://arxiv.org/abs/2008.10723 (arXiv API metadata) and https://github.com/nl4dv/nl4dv"
takeaway: "Python toolkit that turns a natural-language data question into a structured JSON of attributes, tasks and charts, with explicit ambiguity flags; SatClip's question parser should emit a similar inspectable spec"
---

# NL4DV: A Toolkit for Generating Analytic Specifications for Data Visualization from Natural Language Queries

## Problem
Building natural language interfaces for data visualization requires NLP expertise that most visualization developers lack, so each system reimplemented its own fragile parser.

## Approach
NL4DV takes a tabular dataset and a natural-language query and returns a JSON "analytic specification" with three parts: an attribute map (which data columns the query refers to), a task map (which analytic task is intended: correlation, distribution, derived value, trend or filter, with parameters), and a ranked list of Vega-Lite chart specifications. It detects attributes both explicitly (name matches) and implicitly (via data values), using string and semantic similarity with configurable aliases. Each inferred item is labelled as explicit or implicit, and ambiguous matches are flagged so a front end can ask the user to disambiguate. It wraps NLTK, Stanford CoreNLP and spaCy behind a simple Python API.

## Data and benchmarks
No quantitative benchmark or user study; the paper demonstrates four application scenarios (notebook chart generation, a Vega-Lite editor, recreating an ambiguity widget, and a multimodal speech system).

## Key results
Shows that a rule-and-lexicon pipeline can give developers a reusable, inspectable intermediate representation for NL-driven visualization. The paper reports no accuracy figures.

## Limitations
- No measured parsing accuracy; robustness to varied phrasing is not quantified.
- Limited to a small set of analytic tasks and up to three attributes per query.
- Tabular data only; no spatial or temporal reasoning about maps or imagery.
- Pre-LLM approach; later work replaces much of the parsing with language models.

## What it means for SatClip
- Adopt the pattern of an explicit intermediate spec: the VLM should convert a question into a JSON query (instrument, region, date window, comparison) that is shown on the evidence card and executed deterministically, never a free-form answer.
- Copy the explicit versus implicit labelling: if the user never named a date and SatClip assumed "latest scene", mark that field as inferred on the card.
- Copy ambiguity flags: when a place name matches several districts or blocks, ask a one-tap clarifying question instead of guessing.
- Support local aliases (Hindi and regional words for flood, paddy, tank) in the parser lexicon, like NL4DV's alias configuration.
- Beat it on evaluation: build a test set of real Indian official and journalist questions and report parse accuracy, which NL4DV did not.
