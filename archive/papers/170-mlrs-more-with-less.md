---
id: 170
title: "More with Less: a Large Scale Remote Sensing VLM with a Simple Recipe"
authors: "Stefan Maria Ailuro, Mario Markov, Mohammad Mahdi, Luc Van Gool, Danda Pani Paudel"
year: 2026
venue: "ACCV 2026 (per arXiv comment); arXiv:2607.15942, v1 17 July 2026, v2 1 October 2026"
link: https://arxiv.org/abs/2607.15942
code: "https://github.com/insait-institute/MLRS (project page named in the arXiv comment; not fetched)"
category: rs-vlm
era: recent
tags: [general-vlm, internvl3.5, sam3, tool-use, grpo, grto, multi-task-rl, sar, multi-temporal, ultra-high-resolution, data-scaling]
verified: "2026-10-07 via curl to https://export.arxiv.org/api/query (title, authors, dates, ACCV 2026 comment) and curl to https://arxiv.org/html/2607.15942v2 (method, training setup, scaling results, limitations); WebFetch permission request timed out; ACCV acceptance taken from the arXiv comment only"
takeaway: "A plain InternVL3.5-8B trained with multi-task RL that either answers or calls SAM3 matches specialised RS VLMs, which supports SatClip's 'small model decides, a tool measures' split; but its temporal VQA got worse with training and it reports no confidence or abstention"
---

# Ailuro et al. 2026, MLRS (general VLM plus a segmentation tool, trained with RL)

## Problem
Most RS VLM progress has come from RS-specific encoders and fusion modules. The authors test whether an unmodified general VLM, trained on enough diverse RS data, is just as good.

## Approach
- Controller: InternVL3.5-8B (a 2B variant is also trained). SAM3 is an external localisation tool called through text.
- A single language policy reasons, then either answers in text or emits a structured segmentation call (noun phrase plus boxes) that is parsed into SAM prompts.
- Inputs: optical, false colour and SAR (SAR is shown as a greyscale image), plus multi-temporal and multi-view image groups.
- Training: Group Relative Tool Optimization (GRPO on the VLM plus a surrogate loss that also fine-tunes SAM3), adaptive task rewards (format validity plus a task score: accuracy, embedding similarity, IoU, box matching), LoRA, 8 H200 GPUs. 80K curated training samples from a 2.3M raw pool.

## Data and benchmarks
In distribution: DisasterM3, DynamicVL, SARLANG-1M, EarthReason, LaSeRS, GeoSeg-Bench. Out of distribution: XLRS-Bench, RSHR-Bench, VLRS-Bench, UrBench, GEOBench-VLM, GeoSeg-Bench2.

## Key results
- SAR captioning on the in-distribution set rises from 0.09 to 0.38 G-Eval.
- Out of distribution: GEOBench-VLM detection 0.24 to 0.56 Pr@0.5; GeoSeg-Bench2 segmentation 0.41 to 0.70 IoU; XLRS-Bench VQA 0.39 to 0.51; GEOBench-VLM VQA 0.39 to 0.50; XLRS-Bench detection 0.054 to 0.409 Acc@0.5.
- Temporal VQA peaks early then degrades below the base model (VLRS-Bench 0.274 to 0.230, RSHR-Bench 0.345 to 0.295); multi-view VQA barely moves.
- Fine-tuning SAM3 during RL helps most segmentation sets but drops GEOBench-VLM zero-shot, a sign of tool overfitting.

## Limitations
- One backbone family only; diversity findings are described by the authors as suggestive.
- Needs 8B parameters and H200-class training; not CPU friendly.
- SAR is read as a greyscale picture, with no calibration or physical units.
- No confidence, abstention or scene provenance in the outputs.

## What it means for SatClip
- Adopt: strong external evidence that a general VLM that routes to a tool is enough; SatClip goes further by making the tool (SAR threshold, NDVI difference) the only source of numbers.
- Avoid: the temporal VQA regression is a warning that before/after flood or crop questions should not be answered by the VLM's own visual reading; keep change detection in classical instruments.
- Avoid: do not fine-tune the measuring tool jointly with the language model, as MLRS's GRTO does; SatClip instruments should stay fixed and auditable so receipts can be re-run.
