---
id: 089
title: "Change-Agent: Towards Interactive Comprehensive Remote Sensing Change Interpretation and Analysis"
authors: "Chenyang Liu, Keyan Chen, Haotian Zhang, Zipeng Qi, Zhengxia Zou, Zhenwei Shi"
year: 2024
venue: "IEEE TGRS"
link: https://arxiv.org/abs/2403.19646
code: https://github.com/Chen-Yang-Liu/Change-Agent
category: eo-agents
era: recent
tags: [change-detection, change-captioning, llm-agent, tool-use, bi-temporal, levir-mci, python-tools]
verified: "2026-10-05 via https://export.arxiv.org/api/query?id_list=2403.19646 and https://arxiv.org/html/2403.19646 (journal ref TGRS 2024, DOI 10.1109/TGRS.2024.3425815)"
takeaway: "Closest prior art to SatClip's 'instrument as eyes, LLM as brain' split for change questions, but the LLM writes free Python and nothing is calibrated, receipted or allowed to abstain"
---

# Change-Agent: Towards Interactive Comprehensive Remote Sensing Change Interpretation and Analysis

## Problem
Change detection gives a pixel mask but no meaning; change captioning gives a sentence but no precise location. Users who want to ask follow-up questions (how many buildings appeared, why did this change) have no single interactive system that does both.

## Approach
The system pairs a multi-level change interpretation (MCI) model, described as the agent's eyes, with an LLM acting as the brain. The MCI model has two branches, pixel-level change detection and semantic change captioning, linked by a proposed BI-temporal Iterative Interaction (BI3) layer. The LLM receives a crafted prompt and a suite of Python tools, drafts a Python program for the user's request, and a Python interpreter executes it. This lets the agent count changed objects, process images, and offer change-cause or future-change commentary from the LLM's general knowledge.

## Data and benchmarks
- LEVIR-MCI, built by extending the authors' LEVIR-CC captioning set: 10,077 bi-temporal image pairs, 256 by 256 pixels at 0.5 m, each with a change mask (roads and buildings) and five captions.
- Over 40,000 annotated changed object instances (5,002 roads, 39,378 buildings in total).
- MCI model scored with MIoU for detection and BLEU-1..4, METEOR, ROUGE-L, CIDEr-D for captions.

## Key results
- The MCI model reports state-of-the-art results on LEVIR-MCI on both tasks at once, including a reported +0.75% MIoU gain over prior detection methods.
- The agent itself is shown through qualitative dialogue examples; we found no quantitative evaluation of the LLM planning, code correctness, or tool-call accuracy.
- Which LLM backbone the released agent uses was not confirmed from the text we read (the paper discusses ChatGPT and Llama2 generally).

## Limitations
- Very high resolution urban optical imagery only, two change classes (roads, buildings); no SAR, no cloud handling.
- Change-cause analysis and future prediction come from LLM world knowledge, not from measurements, so they are not grounded.
- Free-form generated Python means outputs can differ run to run and there is no recorded receipt or confidence.

## What it means for SatClip
- Adopt the framing: a specialised perception model produces masks and counts, the LLM only plans and narrates. This is the same split SatClip uses and gives us a respected TGRS citation for it.
- Avoid letting the LLM write arbitrary code or speculate about causes. SatClip's router should pick from a fixed instrument list with typed parameters, and any "why" text should be clearly labelled as context, not evidence.
- Beat it on evaluation: Change-Agent shows agent behaviour only by example. SatClip should report exact routing accuracy and parameter accuracy, plus calibration of the confidence it attaches to SAR log-ratio change.
