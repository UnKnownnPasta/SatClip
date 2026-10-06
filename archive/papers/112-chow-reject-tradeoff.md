---
id: 112
title: "On optimum recognition error and reject tradeoff"
authors: "C. K. Chow"
year: 1970
venue: "IEEE Transactions on Information Theory, 16(1): 41-46"
link: https://doi.org/10.1109/TIT.1970.1054406
code: "none found (theory paper)"
category: historical
era: historical
tags: [reject-option, abstention, bayes-decision, selective-prediction, error-reject-curve]
verified: "2026-10-06 via https://api.crossref.org/works/10.1109/TIT.1970.1054406 (title, venue, volume, issue, pages, year; Crossref lists author as C. Chow, full name C. K. Chow from common citation); content summarized from standard knowledge of the paper, full text not fetched"
takeaway: "The theoretical root of SatClip's abstention: reject when the best posterior falls below a threshold, and choose that threshold from the error-reject curve rather than by feel"
---

# Chow 1970, error-reject tradeoff

## Problem
A classifier that must label every input makes errors on ambiguous cases. If it may refuse (reject) some inputs, what is the optimal rule and how do error rate and reject rate trade off?

## Approach
- Under Bayes decision theory, the optimal rule rejects an input whenever its maximum posterior class probability is below a threshold.
- Sweeping the threshold traces an error-reject curve; the paper derives general properties of this curve and links its slope to the threshold.
- Costs of error, rejection and correct decisions fix the optimal operating point.

## Data and benchmarks
Theoretical analysis; no empirical benchmark.

## Key results
- The Chow rule is optimal when posteriors are correct.
- Error rate decreases monotonically as reject rate increases, and the curve can be used to pick an operating point or compare classifiers.

## Limitations
- Optimality depends on calibrated posteriors; with miscalibrated scores (common in modern deep models) the rule degrades, hence later calibration work (Guo) and selective classification (Geifman), both already in this archive.
- Assumes known costs and i.i.d. inputs; no handling of distribution shift.

## What it means for SatClip
- SatClip's "not enough evidence" output is a Chow reject option at the card level: calibrate confidence first, then abstain below a threshold.
- Pick the threshold from an empirical error-reject (risk-coverage) curve on labelled Indian flood events (for example Sen1Floods11 and NRSC atlas cases), and publish the chosen coverage and expected error.
- Treat the threshold as a cost decision: a district official may prefer more abstentions to a wrong flooded-area number, so expose the operating point in documentation.
