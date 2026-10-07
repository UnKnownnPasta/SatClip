---
id: 150
title: "Efficient Guided Generation for Large Language Models"
authors: "Brandon T. Willard, Rémi Louf"
year: 2023
venue: "arXiv preprint (July 2023); no peer-reviewed venue found"
link: https://arxiv.org/abs/2307.09702
code: "https://github.com/dottxt-ai/outlines (Outlines library named in the abstract; repo URL from general knowledge, not fetched)"
category: efficient-inference
era: recent
tags: [constrained-decoding, guided-generation, json-schema, regex, finite-state-machine, cfg, outlines, structured-output]
verified: "2026-10-07 via curl to https://export.arxiv.org/api/query (WebFetch permission request timed out); title, authors, date and abstract from arXiv; no journal or conference reference listed on arXiv; repo URL not fetched; no speed numbers quoted because the abstract gives none"
takeaway: "Constrain the intent model's decoding to SatClip's JSON schema so every output parses and only allowed fields and values can appear, at little extra cost on CPU"
---

# Willard and Louf 2023, efficient guided generation (Outlines)

## Problem
Applications that read LLM output need it in a strict format (JSON, a regex, a grammar). Sampling freely and then validating or retrying is unreliable and slow, and naive masking that checks the whole vocabulary at every step is costly.

## Approach
- Reformulates generation as transitions in a finite-state machine built from a regular expression (or, by extension, a context-free grammar).
- Precomputes an index from FSM states to the vocabulary tokens that keep the output valid, so each decoding step only looks up an allowed-token mask.
- Model agnostic: works with any tokenizer and causal language model.

## Data and benchmarks
Mainly an algorithmic paper; it compares against existing guided-generation approaches on generation overhead. Specific benchmark settings and figures were not re-checked here.

## Key results
- Guarantees that output matches the given structure.
- Adds little overhead to token generation and is reported to significantly outperform existing solutions (no numbers verified here).
- Implemented in the open-source Outlines library; the same idea is now common in other runtimes (for example grammar-constrained sampling in llama.cpp, not covered by this paper).

## Limitations
- Guarantees syntax, not meaning: a valid JSON intent can still have the wrong district, date range or index.
- Grammar support is more involved than regex; very large or recursive schemas can make the index expensive to build.
- Forcing structure can hide model uncertainty: the model must still be allowed to emit an explicit "cannot parse" or clarification intent.

## What it means for SatClip
- Compile SatClip's intent schema (task type, AOI, dates, sensor, index, comparison) into a constrained decoder so the LoRA model can never emit unparsable or out-of-vocabulary fields; enumerate allowed values such as district codes and supported indices.
- Include an explicit abstain or ask-clarification branch in the schema, and log token probabilities at choice points to feed calibration and the reject option (entry 112).
- Fine-tune with the same schema the decoder enforces, so training and serving formats match; then semantic validation (does the district exist, is the date range valid) runs in plain code before any instrument is called.
