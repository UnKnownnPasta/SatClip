---
id: 033
title: "RSHallu: Dual-Mode Hallucination Evaluation for Remote-Sensing Multimodal Large Language Models with Domain-Tailored Mitigation"
authors: "Zihui Zhou, Yong Feng, Yanying Chen, Guofan Duan, Zhenxi Song, Mingliang Zhou, Weijia Jia"
year: 2026
venue: "arXiv preprint (arXiv:2602.10799, February 2026)"
link: https://arxiv.org/abs/2602.10799
code: none
category: trust-calibration
era: upcoming
tags: [hallucination, remote-sensing, rs-vlm, benchmark, image-level-hallucination, mitigation, geochat, lhrs-bot]
verified: "2026-10-04 via https://arxiv.org/abs/2602.10799"
takeaway: "RS VLMs answer hallucination-free only about 36% to 69% of the time on RSHalluEval, including errors about modality and resolution; strong evidence that SatClip's VLM must not produce measurements"
---

# RSHallu: Dual-Mode Hallucination Evaluation for Remote-Sensing Multimodal Large Language Models with Domain-Tailored Mitigation

## Problem
Multimodal LLMs used on remote sensing imagery hallucinate, and existing hallucination benchmarks (such as POPE [A029]) are object-centric and built on natural photos. Remote sensing adds its own failure types: misjudging the sensor modality, the resolution, or the overall land-use scene.

## Approach
Three contributions. (1) A taxonomy that adds image-level hallucination (wrong image attributes such as modality or resolution, and wrong scene or land-use interpretation) to the usual object-level types (existence, attributes, relations). (2) RSHalluEval, a benchmark of 2,023 QA pairs with dual-mode checking: an online mode using a cloud VLM (Qwen-VL-Max with chain-of-thought prompting) and a local mode using a compact Qwen2-VL checker fine-tuned on RSHalluCheck (15,396 QA pairs). (3) Mitigation via RSHalluShield, about 30k QA pairs for fine-tuning, plus training-free methods: logit correction and domain-aware prompting.

## Data and benchmarks
RSHalluEval, RSHalluCheck and RSHalluShield as above, evaluated on general models (LLaVA-1.5, mPLUG-Owl3, Qwen2-VL) and RS-specific models (GeoChat, LHRS-Bot, LHRS-Bot-Nova, VHM).

## Key results
From the expert evaluation table as summarised from the arXiv HTML: overall hallucination-free rate ranged from 36.33% (LHRS-Bot, worst) to 68.33% (VHM, best RS model), with mPLUG-Owl3 at 69.00%, the best general model. So domain-specific RS models did not reliably beat general ones. Mitigation improved hallucination-free rates by up to 21.63 percentage points while keeping downstream task performance, per the abstract. The local checker was much faster than the online mode in the reported comparison but weaker on image-attribute errors. These figures come from a tool-assisted read of the HTML and should be rechecked against the PDF before citing.

## Limitations
Unpublished preprint; code and data were announced but not released at verification time. Benchmark size is modest (about 2k evaluation pairs). The automatically generated mitigation data gives terse single-word scene answers that differ from expert style. Evaluation relies partly on an LLM judge, itself a possible error source. Coverage of SAR, multispectral indices and multi-temporal change questions was not confirmed.

## What it means for SatClip
- Cite this as current evidence that even the best RS VLMs give a hallucinated answer roughly a third of the time, which directly justifies SatClip's design rule that the VLM parses and explains but never measures.
- Adopt the image-level hallucination categories in SatClip's own tests: check that the explanation layer correctly states the sensor (Sentinel-1 VH versus Sentinel-2), resolution (10 m) and dates taken from the receipt, and flag any mismatch automatically.
- Copy the dual-mode idea cheaply: a deterministic local checker that compares every number and date in the VLM's explanation against the evidence card fields, so faithfulness is verified without a cloud judge.
- Beat these models on a shared axis: report a hallucination-free rate for SatClip's explanations on an Indian question set, which should approach 100% for numbers because they are copied from instruments, not generated.
