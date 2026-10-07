---
id: 171
title: "One Adapter, Every Resolution: Gated Low-Rank Adaptation for Remote Sensing VLMs"
authors: "Song Zhang, Yanlong Chen, Yining Chen, Xiaowei Zhang, Yawei Li"
year: 2026
venue: "arXiv preprint (arXiv:2605.07562, v1 8 May 2026, v2 30 September 2026); arXiv comment says under review"
link: https://arxiv.org/abs/2605.07562
code: "Not released; arXiv comment says code, data and checkpoints will be released upon publication"
category: rs-vlm
era: upcoming
tags: [lora, qlora, gsd, scale-conditioning, heteroscedastic-uncertainty, fallback, qwen3-vl, xlrs-bench, omniearth-bench, 4-bit]
verified: "2026-10-07 via curl to https://export.arxiv.org/api/query (title, authors, dates, abstract with headline numbers) and curl to https://arxiv.org/html/2605.07562v2 (inference rule, fallback description, limitations appendix); WebFetch permission request timed out; the SSE-U error, coverage and fallback-rate numbers sit in math markup that did not extract, so they are not quoted"
takeaway: "The only 2026 RS VLM found that uses a calibrated uncertainty to abstain from a self-estimate and fall back to a safe default, but only for image resolution, not for the answer; SatClip can copy the pattern (estimate, check interval, fall back) and apply it to the evidence itself"
---

# Zhang et al. 2026, ScaleEarth (GSD-gated LoRA with an uncertainty-driven fallback)

## Problem
RS images range from centimetres to tens of metres per pixel, but RS VLMs either ignore ground sampling distance (GSD) or pass it as a text token, using the same weights at every scale.

## Approach
- Backbone Qwen3-VL-8B (frozen); a 4-bit QLoRA variant is also reported.
- CS-HLoRA: a single LoRA whose rank dimensions are switched on by sigmoid gates of log10(GSD), with thresholds initialised at object, structure and semantic scales.
- SSE-U: a heteroscedastic head on pooled vision features that predicts log-GSD with a Gaussian variance. At inference, use caller metadata if present; else use the SSE-U estimate if its interval is narrow enough; else fall back to a neutral default GSD chosen so that a wrong fallback degrades gracefully. The authors describe this as the model deciding by itself whether to trust its estimate or abstain.
- GeoScale-VQA: 1.5M QA pairs, each with a resolved GSD, generated with Qwen3-VL-32B from sources including PatternNet, MtSCCD and Sentinel-2 based RSVQA sets.

## Data and benchmarks
XLRS-Bench (13 sub-tasks, ultra-high resolution) and OmniEarth-Bench (7 Earth-science spheres). All ScaleEarth scores are metadata-free, so they rely on the SSE-U estimate or fallback.

## Key results
- XLRS-Bench average 59.4, 5.2 points above the strongest RS specialist reported.
- OmniEarth-Bench average 40.71, 7.45 points above the strongest open-source baseline.
- The 4-bit variant fits a single 40 GB GPU and keeps 57.4 on XLRS-Bench.
- The fallback is reported to trigger on a minority of benchmark samples and disabling it lowers the score (exact figures not extracted, see verified field).

## Limitations
- Uncertainty covers only the resolution estimate; answers themselves carry no confidence, and there is no answer-level abstention.
- Training data is LLM generated, so quality is bounded by the generator.
- Tested only on Qwen3-VL-8B and on GSDs within the training range; coarse satellite products beyond that were not evaluated.
- Code and weights not yet released.

## What it means for SatClip
- Adopt: the three-branch rule (trusted metadata first, then a model estimate only if its predicted interval is tight, else a safe default) is a clean template for SatClip's abstention logic, applied to the instrument's output rather than to metadata.
- Adopt: SatClip should always pass true scene metadata (pixel spacing, sensor) instead of letting any model guess it, which this paper shows matters.
- Beat: ScaleEarth confirms the gap: even the most uncertainty-aware RS VLM of 2026 gives no calibrated confidence on the answer and no provenance; SatClip's per-answer calibrated confidence plus abstain remains novel.
- Note for CPU: even its 4-bit version needs a 40 GB GPU, so SatClip's small LoRA parser must stay far smaller.
