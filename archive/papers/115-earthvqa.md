---
id: 115
title: "EarthVQA: Towards Queryable Earth via Relational Reasoning-Based Remote Sensing Visual Question Answering"
authors: "Junjue Wang, Zhuo Zheng, Zihang Chen, Ailong Ma, Yanfei Zhong"
year: 2024
venue: "Proceedings of the AAAI Conference on Artificial Intelligence (AAAI 2024)"
link: https://arxiv.org/abs/2312.12222
code: https://github.com/Junjue-Wang/EarthVQA
category: rs-benchmark
era: recent
tags: [vqa, counting, relational-reasoning, segmentation-guided, rmse, city-planning, benchmark]
verified: "2026-10-06 via https://arxiv.org/abs/2312.12222, https://arxiv.org/html/2312.12222 (v1) and https://raw.githubusercontent.com/Junjue-Wang/EarthVQA/master/README.md; AAAI 2024 acceptance taken from the arXiv comment, AAAI proceedings volume and pages not checked"
takeaway: "Even a VQA model that is fed segmentation masks scores far lower on counting and comprehensive analysis than on yes/no judging, which backs SatClip's choice to compute counts and areas from masks and let the language model only phrase them"
---

# EarthVQA

## Problem
Most Earth vision work stops at locating and labelling objects. Planners actually ask relational questions (how many ponds are near residential blocks, is this area suitable for a school), and earlier RS VQA sets such as RSVQA had few question types and little reasoning.

## Approach
- Builds EarthVQA on top of the LoveDA land-cover dataset, adding images, a playground class and refined masks.
- Basic judging and counting answers are generated automatically from the masks; relational and analysis answers (distances, layouts, topology) are annotated by hand for urban and rural governance needs.
- Proposes SOBA, a two-stage model: a segmentation network produces object semantics, then object-guided attention and bidirectional cross-attention reason over objects and their relations.
- Adds a numerical difference loss that penalises counting errors by how far off they are, joining classification and regression views of counting.

## Data and benchmarks
- 6,000 WorldView-3 images at 0.3 m from Nanjing, Changzhou and Wuhan (China), with semantic masks and 208,593 QA pairs.
- Six question families: basic judging, relational judging, basic counting, relational counting, object situation analysis, comprehensive analysis.
- Metrics: accuracy per family, overall accuracy (OA), and RMSE for counting. Public leaderboards on Codabench for segmentation and VQA.

## Key results
- SOBA reaches 78.14% OA (Table 1, arXiv v1), ahead of eight general and several RS VQA baselines.
- Per family for SOBA: basic judging 89.63%, relational judging 82.64%, basic counting 80.17%, relational counting 67.86%, object analysis 61.40%, comprehensive analysis 49.30%.
- Counting RMSE for SOBA is 0.79 (basic) and 1.15 (relational). Ablations credit the object-guided attention and the numerical difference loss with most of the gain.

## Limitations
- Only three Chinese cities at very high resolution optical; no SAR, no time series, no change questions.
- Many answers are derived from the same masks the model can learn from, so it rewards mask quality more than open-ended reasoning.
- Counting is answered as a class over small integers, not as calibrated measurements with uncertainty. The authors later extended the scope globally (EarthVL, per the README), not reviewed here.

## What it means for SatClip
- The drop from about 90% on judging to about 49% on comprehensive analysis, even with masks inside the model, supports keeping SatClip's numbers in the instruments (KI water mask, NDVI difference) and out of the VLM.
- Copy the idea of counting from masks: SatClip's evidence card can report counts and areas computed directly from the district mask, with RMSE-style scoring in our eval rather than accuracy only.
- Use EarthVQA's question taxonomy (judging, counting, relational, analysis) to structure SatClip's question parser tests, and route relational questions to "not supported yet" with an explicit abstention.
