---
id: 225
title: "ToolChain-CRC: Conformal Risk Control for Agentic AI Under Retrieval and Tool-Use Drift"
authors: "Jeffery Opoku, David Banahene"
year: 2026
venue: "arXiv preprint (arXiv:2606.18467, v1 16 June 2026, stat.ML, 26 pages); no peer-reviewed venue found"
link: https://arxiv.org/abs/2606.18467
code: "A 'Code availability' heading exists in the paper but no repository URL appeared in the text read"
category: upcoming
era: upcoming
tags: [conformal-risk-control, llm-agents, tool-use, retrieval, trajectory-level-risk, accept-or-intervene, anytime-alarm, distribution-drift, selective-prediction]
verified: "2026-10-09 via curl to export.arxiv.org/api/query?id_list=2606.18467 (title, two authors, date, abstract, comment '26 pages, 11 figures') and WebFetch of arxiv.org/html/2606.18467 (method sections 3 to 6, Theorem 1, Propositions 1 and 2, limitation headings); the experiments section, target alpha values and all numeric results were not reachable in the HTML capture, so no results numbers are reported here"
takeaway: "Calibrates an accept-or-intervene rule over the whole agent trajectory (retrieval, tool calls, synthesis) rather than the final answer, with a conformal guarantee on the risk of accepted runs; SatClip's abstention should score scene search, preprocessing and mask steps, not just the final number"
---

# Opoku and Banahene 2026, ToolChain-CRC

## Problem
Agents retrieve, call tools and then answer. A final answer can look fine even when retrieval was weak or a tool returned a wrong value, so calibrating confidence on the final output alone can let failed runs through.

## Approach
- Each run is a trajectory of steps. Every step gets a runtime risk score in [0, 1]: for retrieval, one minus retrieval or source-support confidence; for tools, error flags, invalid output, cross-tool disagreement or a domain verifier; for synthesis, an unsupported-answer score. Each step also has an audited label used only for calibration.
- Step scores are combined into a trajectory score, by default a noisy-or (one minus the product of one minus each step score), optionally a weighted sum.
- A run is accepted if its trajectory score is below a threshold lambda; otherwise the system intervenes. Lambda is calibrated with conformal risk control so the expected loss of accepted runs is at most alpha (Theorem 1), assuming complete trajectories are exchangeable; steps inside a run may be adaptive and dependent.
- Proposition 1 formalises how final-answer-only calibration can miss upstream risk. A utility rule trades risk against intervention rate among feasible thresholds without becoming less cautious.
- Extensions per the abstract: a drift-aware version with auditable constants and an anytime alarm (supermartingale based) that can stop a risky run mid-way.

## Data and benchmarks
- Per the abstract: synthetic tool-chain drift, RAG and tool-use stress tests, SQuAD-derived retrieval tasks, an API-free agentic QA case study, ablations, target-risk sensitivity, 20-seed robustness, a drift-margin audit and a live RAG and tool-use agent benchmark.
- Models and alpha values used were not visible in the text read.

## Key results
- Qualitatively, per the abstract: final-answer-only calibration can miss retrieval and tool failures, while trajectory-level calibration keeps accepted-run risk below target.
- No numeric results could be confirmed in this session.

## Limitations
- Listed by the authors: needs step risk scores to exist; large shifts can drive high intervention rates; strongest guarantees assume exchangeable trajectories; the drift metric itself must be audited; public RAG experiments are benchmark-derived; it is a calibration layer, not an agent design.
- Two-author preprint without peer review yet.
- Needs audited step-level labels for calibration, which are costly.

## What it means for SatClip
- Adopt: treat each SatClip answer as a trajectory and give every step a risk score from physical checks: scene search (no scene within the date window, high cloud fraction), preprocessing (terrain shadow or layover share in the mask, orbit mismatch between before and after scenes), segmentation (calibrated mask uncertainty, entry 219) and the intent parse (schema-valid but low-margin district match).
- Adopt: combine step scores with a noisy-or into the abstention decision and calibrate its threshold with CRC on audited runs, so a correct-looking number built on a cloudy or mismatched scene still triggers abstention.
- Adopt: write every step score into the PROV receipt (entry 222) so the next step offered on abstention names the failing step ("wait for the next Sentinel-1 pass on 18 Oct" rather than a generic refusal).
- Watch: start with a small audited set of Indian runs and expect high intervention rates; verify the paper's numbers once the full text is readable before quoting gains.
