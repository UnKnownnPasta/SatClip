---
id: 224
title: "The Mirage of Calibrated Confidence: Trajectory-Independence of Verbalized Confidence in Vision-Language Models"
authors: "Jisoo Yang, Jaeho Han, Trung X. Pham, Junyeong Kim"
year: 2026
venue: "EMNLP 2026 Main (per arXiv comment); arXiv:2609.18453, v1 16 September 2026"
link: https://arxiv.org/abs/2609.18453
code: "No repository link found in the HTML text read"
category: upcoming
era: upcoming
tags: [verbalized-confidence, vlm, calibration, ece, reasoning-trajectory, trajectory-grounding-score, tgs-bench, qwen3-vl]
verified: "2026-10-09 via curl to export.arxiv.org/api/query?id_list=2609.18453 (title, four authors, date, abstract, comment 'EMNLP 2026 Main') and WebFetch of arxiv.org/html/2609.18453 (models, benchmarks, metric definitions, reported numbers); EMNLP acceptance only per the authors' comment, proceedings not checked; one ECE figure (0.081) was attributed in the text both to a 4B DynaMath comparison and to an 8B model in Figure 1, so the model size for that number is uncertain"
takeaway: "A VLM's spoken confidence barely changes with what its reasoning actually contains, and RL calibration training improved ECE while making confidence even less tied to the reasoning; SatClip must never use the VLM's self-reported confidence for the meter and should test any confidence signal by perturbing its evidence"
---

# Yang et al. 2026, The Mirage of Calibrated Confidence

## Problem
VLMs are increasingly asked to state a confidence after reasoning, and calibration methods are judged by ECE and AUROC. A model can reach a low ECE while its confidence ignores the reasoning it just produced: it can second-guess itself repeatedly, land on a wrong answer and still claim high confidence.

## Approach
- Three probes of whether confidence depends on the reasoning trajectory: substituting trajectory content, masking trajectory tokens (0% to 100%), and checking confidence around the model's own hesitation markers.
- Proposes the Trajectory-Grounding Score: TGS-self compares confidence with and without access to the model's trajectory (range -1 to 1; near zero means blind to the trajectory); TGS-pair checks whether confidence is higher for a correct trajectory than for one with a controlled flaw on the vision, reasoning or answer axis.
- Releases TGS-Bench with controlled good and bad trajectory pairs.

## Data and benchmarks
- Models: Qwen3-VL-4B-Instruct and 8B, and VL-Calibration 4B and 8B (RL-tuned from Qwen3-VL to give separate vision and reasoning confidence); a cross-architecture check is mentioned but was not read.
- TGS-Bench spans 10 benchmarks: A-OKVQA, DynaMath, Geo3K, LogicVista, MathVerse, MathVision, MathVista, MMK-12, MMMU-Pro and WeMath.

## Key results
- Under content substitution, confidence stayed nearly unchanged in a large share of cases; for the calibrated model, on the vision axis this was about 82 to 90% versus about 40% for the base model.
- Hesitation markers appeared in 22.5% of base-model and 57.2% of calibrated-model trajectories; confidence was nearly identical before and after the hesitation in 78.5% and 49.0% of those events respectively.
- On DynaMath, calibration training lowered ECE from about 0.42 to about 0.08 while TGS-self fell from 0.042 to about zero, so ECE rankings and trajectory-grounding rankings disagree.
- Masking and substitution analyses were run only on the 4B models.

## Limitations
- No explicit limitations section was found in the text read.
- Mostly math and general VQA; no remote sensing, SAR or multispectral data.
- Two model families; generalisation to other VLMs rests on a check not read here.
- Recent preprint; acceptance stated by the authors only.

## What it means for SatClip
- Confirms the design rule: the confidence meter comes from Platt or regime-map calibration over instrument-derived features (backscatter change, cloud fraction, mask agreement), not from the VLM's or LLM's stated confidence, which can be calibrated on paper and still ignore the evidence.
- Adopt: add an evidence-sensitivity test to the evaluation suite: swap or blank the Sentinel scene behind an answer and require the confidence to drop; a signal that does not move fails, whatever its ECE.
- Adopt: if the language layer writes any explanation, check it against the card's numbers and drop hedging or certainty words that disagree with the calibrated band.
- Watch: report ECE together with an evidence-grounding check in the model card (entry 223), since ECE alone can hide this failure.
