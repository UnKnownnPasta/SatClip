---
id: 182
title: "JL1-CC&QA: Extending the JL1-CD Benchmark with Change Captioning and Question Answering"
authors: "Ziyuan Liu, Ruifei Zhu, Ouqiao Ma, Yuantao Gu"
year: 2026
venue: "arXiv preprint (arXiv:2606.31745, v1 30 June 2026); no peer-reviewed venue found"
link: https://arxiv.org/abs/2606.31745
code: "https://github.com/circleLZY/JL1-CD (stated in the abstract; README fetched but contained no release notes or venue)"
category: rs-benchmark
era: upcoming
tags: [change-captioning, change-vqa, jilin-1, satellite, change-masks, llm-generated-annotations, llm-judge, benchmark]
verified: "2026-10-08 via curl to https://export.arxiv.org/api/query (title, authors, date, abstract) and https://arxiv.org/html/2606.31745 (dataset construction, statistics, conclusion); WebFetch permission request timed out; the paper reports no model baselines, so none are given"
takeaway: "Adds 17,021 change captions and 20,060 open-ended change QA pairs to 5,000 Jilin-1 satellite pairs with binary masks, and its LLM judge rejected answers that invented precise percentages; a ready multi-task change set for SatClip's explainer tests but with no baselines yet and optical only"
---

# Liu et al. 2026, JL1-CC&QA

## Problem
Binary change masks say where something changed but not what or why. Existing change captioning and change QA sets are often aerial, small, or lack masks on the same images.

## Approach
- Start from JL1-CD: 5,000 bi-temporal Jilin-1 satellite image pairs at 0.5 to 0.75 m from several Chinese provinces (2022 to 2023), each with an expert binary change mask; cloudy or blurred pairs were excluded.
- Captions: a multimodal LLM (Kimi-K2.6) sees both images, the mask, the change area ratio and a location phrase and writes five captions; a second LLM call scores them on accuracy, specificity, spatial correctness, fluency and informativeness and keeps the top three; experts review a subset.
- QA: the LLM also gets the selected captions as context and writes five QA pairs per image across eight types (existence, description, location, magnitude, temporal comparison, causation, relative comparison, visual detail). The prompt forbids copying exact numeric metadata into answers; a judge discards pairs scoring below 7 of 10.

## Data and benchmarks
JL1-CC: 17,021 captions (68.1% pass rate). JL1-QA: 20,060 QA pairs from 24,995 generated (80.3% pass rate); questions average 11.1 words and answers 19.3 words; most frequent types are yes or no (21.2%), where (18.3%) and what (16.9%).

## Key results
- Dataset paper only: no captioning or QA model results are reported.
- The most common reason for rejecting QA pairs was hallucinated precise percentages, followed by redundancy and vague answers.

## Limitations
- Optical very-high-resolution only; no SAR, no Sentinel, no explicit flood category.
- Annotations are LLM written and LLM judged; human verification covers only a subset, so label noise is unknown.
- Causation questions invite speculation that images alone cannot support.
- No baselines, metrics protocol or confidence and abstention evaluation yet.

## What it means for SatClip
- Adopt: the finding that LLMs invent precise percentages is a direct warning for SatClip's explainer; numbers in SatClip answers must be copied from the evidence card, and a post-check should reject any number not present there.
- Adopt: the magnitude, location and temporal-comparison question types are useful paraphrase seeds for SatClip's change-intent parser.
- Avoid: answering causation questions (why did it change) from imagery; SatClip should decline or say the imagery cannot show cause.
