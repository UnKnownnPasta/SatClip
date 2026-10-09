---
id: 203
title: "Seeing Clearly without Training: Mitigating Hallucinations in Multimodal LLMs for Remote Sensing"
authors: "Yi Liu, Jing Zhang, Di Wang, Xiaoyu Tian, Haonan Guo, Bo Du"
year: 2026
venue: "arXiv preprint arXiv:2603.02754 (v1 March 2026); no venue stated"
link: https://arxiv.org/abs/2603.02754
code: "Authors state code and data will be released at https://github.com/MiliLab/RADAR (release not checked)"
category: rs-benchmark
era: upcoming
tags: [hallucination, rshbench, rs-vqa, training-free, attention-guided-zoom, llm-as-judge, factual-vs-logical-hallucination, geozero]
verified: "2026-10-09 via curl to https://export.arxiv.org/api/query?id_list=2603.02754 (title, authors, date, abstract) and WebFetch of https://arxiv.org/html/2603.02754v1 (RSHBench size and sources, judge protocol and kappa values, RADAR method, Tables 2 and 3 numbers, limitations)"
takeaway: "A 2026 RS hallucination benchmark (RSHBench, 371 items, factual vs logical subtypes, three-LLM-judge majority vote) finds 47 to 61% of RS-VQA outputs hallucinate; a training-free attention-guided zoom (RADAR) cuts GeoZero's rate from 49.9% to 38.8%; strong evidence for SatClip's choice to keep numbers out of the VLM"
---

# Liu et al. 2026, RSHBench and RADAR

## Problem
Multimodal LLMs on remote sensing VQA often state things not in the image, mostly because they fail to find small targets in large scenes. Existing RS hallucination work (entry 33, RSHallu) measures rates but gives limited diagnosis of which step failed.

## Approach
- RSHBench: models must output a step-by-step trace and a final answer in fixed JSON; three LLM judges (Gemini-3-pro, GPT-5.2, Qwen3-max) label hallucination by majority vote, split into factual (object, attribute, spatial) and logical (invalid reasoning, unjustified causality, inconsistency, over-attribution) subtypes.
- RADAR, a training-free test-time method: divides query-specific attention by generic scene attention to find evidence regions, does a coarse "where" then a fine "what" crop, skips cropping when attention entropy says the focus is too diffuse, and answers from both the full image and the crop.

## Data and benchmarks
- RSHBench: 371 image-question pairs drawn from LRS-VQA, MME-RealWorld-RS, UCM and LHRS-Bench, stratified by task (counting, localisation, attributes, structure).
- Judge agreement: leave-one-out Cohen's kappa 0.86 (GPT-5.2), 0.81 (Qwen3-max), 0.57 (Gemini-3-pro), plus a 100-item human check.
- Accuracy also reported on LRS-VQA, LHRS-Bench and MME-RealWorld-RS.

## Key results
- Baseline hallucination rates of roughly 47% to 61% across Claude-3.7, Gemini-2.5-pro, GPT-4o, GLM-4.6v, LLaVA-1.5, Qwen3-VL-4B, Llama-3.2-90B and GeoZero.
- GeoZero hallucination rate 49.87% to 38.81% with RADAR; average accuracy over three benchmarks 45.56 to 47.40.
- On Qwen3-VL-4B, MME-RealWorld-RS accuracy 34.45 to 41.79 with full RADAR; dropping either stage reduces the gain.
- Generic cropping (ViCrop) gave small or negative gains in some settings.

## Limitations
- Small benchmark (371 items) on high-resolution optical imagery; no SAR, no multi-temporal change, no Sentinel-scale data.
- Labels come from LLM judges, so borderline cases may be mislabelled.
- RADAR needs internal attention maps, so it does not apply to closed APIs, and it adds inference cost.
- The prompt asks models to say when the answer cannot be determined, but the paper does not report abstention rates or calibration.
- Not peer reviewed as of the verification date.

## What it means for SatClip
- Avoid: the measured rates (about half of RS-VQA outputs hallucinate in some way) argue against letting any VLM produce SatClip's flood or crop numbers; keep the VLM, if any, to phrasing and intent parsing.
- Adopt: the factual vs logical split is a useful audit rubric for SatClip's plain-language explanations; a logical error (for example blaming crop loss on a flood the mask does not show) should be checked separately from a wrong number.
- Adopt: the entropy-based "focus test" is a neat analogue of SatClip's abstention: if the evidence is too diffuse, fall back rather than zoom in on noise.
- Novelty: does not weaken the claim. It is a diagnosis and mitigation paper for optical VQA with no calibrated confidence, receipts or live data; it strengthens the motivation for SatClip's instrument-first design.
