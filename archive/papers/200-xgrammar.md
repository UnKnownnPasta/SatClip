---
id: 200
title: "XGrammar: Flexible and Efficient Structured Generation Engine for Large Language Models"
authors: "Yixin Dong, Charlie F. Ruan, Yaxing Cai, Ruihang Lai, Ziyi Xu, Yilong Zhao, Tianqi Chen"
year: 2025
venue: "MLSys 2025 (per arXiv comment); arXiv:2411.15100 (v1 November 2024, v3 May 2025)"
link: https://arxiv.org/abs/2411.15100
code: "Open source per the paper and integrated into MLC-LLM and SGLang; repository URL not shown in the text read (widely known as github.com/mlc-ai/xgrammar, not verified here)"
category: efficient-inference
era: recent
tags: [constrained-decoding, json-schema, context-free-grammar, structured-output, pushdown-automaton, token-mask-cache, llama.cpp, outlines, cpu]
verified: "2026-10-08 via curl to https://export.arxiv.org/api/query (title, authors, dates, abstract, MLSys '25 comment) and curl to https://arxiv.org/html/2411.15100 (method details, baselines including llama.cpp grammar engine and Outlines, test hardware, Table 4 syntactic accuracy); WebFetch permission request timed out"
takeaway: "A grammar engine that makes JSON-schema constrained decoding nearly free by precomputing token masks for most of the vocabulary (up to 100x lower per-token mask cost than prior engines); SatClip's intent parser should decode under its JSON schema with such an engine so every parse is valid, at negligible CPU cost"
---

# Dong et al. 2025, XGrammar

## Problem
Agents need LLM outputs that parse: JSON function calls, SQL, DSLs. Constrained decoding with context-free grammars guarantees this, but checking every vocabulary token against grammar stack states at each step adds noticeable latency, especially with 128k-token vocabularies.

## Approach
- Splits tokens into context-independent ones, whose validity depends only on the current grammar position and can be prechecked into an adaptive token-mask cache, and context-dependent ones checked at runtime.
- Grammar transformations expand rule context to shrink the context-dependent set; for Llama-3.1 with a JSON grammar fewer than 1% of tokens (1,134 of 128k) remain context dependent.
- A persistent stack enables fast branching and rollback for the runtime checks.
- Mask generation runs on CPU and is overlapped with GPU model execution.

## Data and benchmarks
- JSON schema and unconstrained-JSON CFG workloads (json-mode-eval), plus XML and Python grammars on synthetic data.
- Baselines: Outlines, the llama.cpp grammar engine and lm-format-enforcer; Llama-3.1-8B-Instruct on an AMD Ryzen 9 7950X CPU with an RTX 4090; end-to-end serving on H100 via MLC-LLM and SGLang compared with vLLM plus Outlines and llama.cpp.

## Key results
- Up to 100x lower per-token latency for grammar mask generation than prior engines.
- Up to 80x end-to-end speedup for structured-output serving of Llama-3.1 on H100.
- Syntactic correctness with Llama-3.1-8B: function calling 62% to 100%, XML generation 80% to 100% when constrained.

## Limitations
- End-to-end gains are measured on GPUs; on a CPU-only box, model decoding dominates, so the benefit is mainly that constraint checking stops adding cost.
- Guarantees syntax only; a valid JSON intent can still hold the wrong district, date range or question type.
- Integration targets MLC-LLM, SGLang and similar engines; llama.cpp has its own grammar engine.

## What it means for SatClip
- Adopt: constrain the LoRA intent parser to SatClip's JSON schema (question type enum, district code, date range, sensor) so malformed parses never reach the pipeline; XGrammar or llama.cpp's built-in grammar both work, and Outlines (entry 150) is the older reference.
- Adopt: use enum-only fields where possible so the grammar removes free text and a schema-valid but semantically doubtful parse triggers a clarifying question instead of a guess.
- Avoid: do not count schema validity as accuracy; measure intent accuracy separately on held-out Indian questions.
