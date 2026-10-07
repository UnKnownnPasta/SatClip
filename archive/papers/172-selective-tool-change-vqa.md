---
id: 172
title: "Selective Tool Use for Agentic Change Visual Question Answering in Remote Sensing"
authors: "Yakoub Bazi, Mohamad M. Al Rahhal, Mohamed A. Mekhtiche, Mansour Zuair"
year: 2026
venue: "arXiv preprint (arXiv:2609.14523, v1 13 September 2026); no peer-reviewed venue found"
link: https://arxiv.org/abs/2609.14523
code: "https://github.com/yakoubbazi/ToolChangeVQA (stated as to be released; not fetched)"
category: rs-vlm
era: upcoming
tags: [change-vqa, tool-use, deterministic-tools, lora, qwen3.5-4b, cdvqa, semantic-change-detection, evidence-conditioned-answering]
verified: "2026-10-07 via curl to https://export.arxiv.org/api/query (title, authors, date, abstract) and curl to https://arxiv.org/html/2609.14523v1 (full text including Tables I to IV); WebFetch permission request timed out"
takeaway: "Closest 2026 match to SatClip's architecture: a LoRA-tuned 4B VLM that calls deterministic change tools lifts measurement questions from about 50% to near 100% with perfect maps, but only to 63 to 66% with predicted maps and with no confidence or abstention, so instrument quality and calibrated refusal are where SatClip must win"
---

# Bazi et al. 2026, selective tool use for change VQA

## Problem
VLMs answer change questions such as "did anything change" well, but are unreliable on questions that need transition statistics, proportions or locations, because they never actually compute them.

## Approach
- A single VLM (Qwen3.5-4B, LoRA on selected decoder attention projections, vision encoder frozen) either answers directly or emits one structured call to a deterministic tool.
- Three tools operate on bi-temporal semantic maps: transition (class transitions and area statistics), spatial (location of new regions), temporal summary. The tool returns a structured observation and the same VLM writes the final answer.
- Semantic maps are never shown to the VLM; at most one tool call per question; no separate router.
- Supervision for tool choice, arguments and observations is generated automatically from CDVQA's six-class annotations.

## Data and benchmarks
Tool-augmented CDVQA: 2,968 image pairs and 47,586 questions in eight families (F1 to F2 direct, F3 to F8 tool based), split 70/15/15 by image pair; 7,164 test questions. Two evidence settings: reference (ground-truth maps) and predicted (a semantic change detection model with 73.08 mIoU and 87.38% pixel accuracy).

## Key results
- Direct answering: 73.77% overall, with 50.34% on proportion (F4), 47.20% on largest or smallest change (F5) and 52.42% on location of new regions (F6).
- With reference maps: 88.79% overall; F4 99.83%, F6 99.76%, F8 100%; F5 only 59.51%.
- With predicted maps: 77.47% overall; F4 63.40%, F6 66.46%. Gains persist but shrink by about 11 points overall.
- The model followed the tool policy correctly; most residual errors come after the tool returns, when the VLM compares several quantities.
- Trained on a single RTX A6000.

## Limitations
- Aerial RGB benchmark with six urban classes; no SAR, no Sentinel data.
- Tool routing is fixed per question family, so the model learns a mapping rather than open-ended planning.
- No confidence, abstention or provenance; a wrong predicted map silently produces a confident wrong answer.
- The VLM still does the final comparison of numbers, which is where F5 errors arise.

## What it means for SatClip
- Adopt: strong independent support for SatClip's design (small LoRA VLM routes, deterministic tool measures). Cite the jump from about 50% to near 100% on measurement questions when evidence is exact.
- Beat: the drop from reference to predicted maps shows that answer quality is capped by the instrument; SatClip must report the instrument's own calibrated confidence and abstain when it is low, which this paper does not do.
- Adopt: let code, not the VLM, do comparisons and rankings of returned numbers (the F5 failure); SatClip's explainer should only verbalise values already computed and stored in the evidence card.
