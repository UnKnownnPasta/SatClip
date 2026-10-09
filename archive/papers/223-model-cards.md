---
id: 223
title: "Model Cards for Model Reporting"
authors: "Margaret Mitchell, Simone Wu, Andrew Zaldivar, Parker Barnes, Lucy Vasserman, Ben Hutchinson, Elena Spitzer, Inioluwa Deborah Raji, Timnit Gebru"
year: 2019
venue: "FAT* '19: Conference on Fairness, Accountability, and Transparency, Atlanta, 29-31 January 2019, DOI 10.1145/3287560.3287596; arXiv:1810.03993 (v1 October 2018, v2 January 2019)"
link: https://arxiv.org/abs/1810.03993
code: "None in the paper"
category: data-infrastructure
era: historical
tags: [model-cards, documentation, disaggregated-evaluation, intended-use, transparency, accountability, audit]
verified: "2026-10-09 via curl to export.arxiv.org/api/query?id_list=1810.03993 (title, nine authors, dates, journal_ref FAT* '19, DOI) and WebFetch of arxiv.org/pdf/1810.03993 (card sections, two example cards, metrics, stated limitations); per-group numbers live in figures and were not read"
takeaway: "Proposes a short standard document per model listing intended use, evaluation factors, metrics with disaggregated results and caveats; SatClip should publish one model card per sensor-task pair, with per-state, per-season and per-terrain error and calibration, and link it from every receipt"
---

# Mitchell et al. 2019, Model Cards

## Problem
Trained models are released and reused in settings they were never evaluated for, and aggregate accuracy hides much worse performance on particular groups or conditions. There was no standard way to tell downstream users where a model works and where it does not.

## Approach
- A model card is a short document shipped with a model, with nine sections: Model Details, Intended Use, Factors, Metrics, Evaluation Data, Training Data, Quantitative Analyses (unitary and intersectional), Ethical Considerations, Caveats and Recommendations.
- Central idea: evaluate disaggregated by relevant factors (groups, instruments, environments) and their intersections, and report the decision threshold and uncertainty of each metric.
- Two example cards: a smile classifier on CelebA and the Perspective API toxicity classifier.

## Data and benchmarks
- Smile detection: CelebA, disaggregated by annotated gender and age group; false positive, false negative, false discovery and false omission rates at a 0.5 threshold, with 95% bootstrap confidence intervals.
- Toxicity: synthetic template sentences with identity terms swapped in; pinned AUC per group, comparing two model versions.

## Key results
- The smile card exposes group differences hidden by the aggregate (for example a higher false discovery rate for older men).
- The toxicity card shows an earlier version scoring poorly on some identity terms and a later version improved after mitigation.
- These are illustrations of the reporting format, not a benchmark claim.

## Limitations
- A card is only as honest as its authors; nothing enforces accuracy.
- Requires evaluation data labelled with the factors of interest, which is often missing.
- Not exhaustive; sections need tailoring per domain.
- Static document; it can drift out of date as models are retrained.

## What it means for SatClip
- Adopt: publish a model card for each pipeline (Sentinel-1 flood extent, Sentinel-2 crop or burn mapping, intent parser), with Factors chosen for Indian deployment: agro-climatic zone, season (monsoon versus dry), terrain and slope, orbit direction, cloud fraction, urban versus rural.
- Adopt: report error and calibration (ECE, abstention rate, risk at the chosen alpha) per factor with bootstrap intervals, matching the paper's practice, and state the decision threshold used by the confidence meter.
- Adopt: the receipt should cite the model card version (hash) so an auditor sees the exact caveats in force when the answer was produced; the Intended Use section should explicitly exclude uses such as individual compensation decisions without field verification.
- Adopt: when a query lands in a factor cell with no evaluation data, abstain and name the gap, rather than extrapolating from the aggregate.
