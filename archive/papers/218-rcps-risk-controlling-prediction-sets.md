---
id: 218
title: "Distribution-Free, Risk-Controlling Prediction Sets"
authors: "Stephen Bates, Anastasios Angelopoulos, Lihua Lei, Jitendra Malik, Michael I. Jordan"
year: 2021
venue: "Journal of the ACM, 68(6), pp. 1-34 (2021), DOI 10.1145/3478535; arXiv:2101.02703 (v1 January 2021, v3 August 2021)"
link: https://doi.org/10.1145/3478535
code: "https://github.com/aangelopoulos/rcps (listed in the arXiv comment; repository not opened from this session)"
category: trust-calibration
era: recent
tags: [conformal-prediction, risk-control, rcps, segmentation, pixel-sets, upper-confidence-bound, high-probability-guarantee, polyp-segmentation]
verified: "2026-10-09 via curl to export.arxiv.org/api/query?id_list=2101.02703 (title, five authors, dates, abstract, code link), curl to api.crossref.org (JACM 68(6), pp. 1-34, DOI 10.1145/3478535, issued 2021-09-30), and WebFetch of arxiv.org/html/2101.02703 (Section 5.4 segmentation setup, loss, alpha and delta, calibration size, limitations); exact achieved-risk numbers for segmentation are shown only as histograms and were not read off"
takeaway: "Calibrates a single threshold on held-out data so that, with probability at least 1 minus delta, the expected per-object share of missed pixels stays below alpha; the high-probability version of entry 133 and a direct recipe for SatClip's flood-mask threshold"
---

# Bates et al. 2021, Risk-Controlling Prediction Sets (RCPS)

## Problem
Accuracy alone does not support consequential decisions; users also need to know, per instance, how wrong an output can be. Standard conformal prediction controls only miscoverage (did the set contain the label?). Many tasks, including segmentation, need control of a graded loss such as the fraction of an object that was missed.

## Approach
- Builds a nested family of set-valued predictors indexed by a scalar lambda (larger lambda, larger set) on top of any black-box model.
- For each lambda, computes an upper confidence bound on the risk from a held-out calibration set, then picks the smallest lambda whose bound (and every larger lambda's bound) stays under the target alpha.
- Guarantee: with probability at least 1 minus delta over the calibration draw, the risk on future points is at most alpha. Requires i.i.d. calibration and test data; the base model can be trained elsewhere.
- Offers several concentration bounds (Hoeffding, Bentkus, a combined Hoeffding-Bentkus, Waudby-Smith-Ramdas, and an asymptotic CLT bound) and recommends WSR for bounded non-binary losses.
- Segmentation case: a pixel set is all pixels whose renormalised score exceeds the threshold; the loss is the average, over 8-connected ground-truth components, of the fraction of each component's pixels left out, so small objects are not ignored.

## Data and benchmarks
- Five demonstrations: cost-sensitive classification, multi-label classification, hierarchical classification, image segmentation, and protein structure prediction.
- Segmentation: 1,781 polyp images pooled from Kvasir, Hyper-Kvasir, CVC-ColonDB, CVC-ClinicDB and ETIS-Larib, 1,000 used for calibration and the rest for testing over repeated random splits, PraNet as the base model, alpha = 0.1 and delta = 0.1.

## Key results
- Across random splits the realised segmentation risk stays at or below the target, and average set size is reported as comparable to average polyp size (exact values appear only as histograms, not checked here).
- The paper suggests roughly 1,000 to 10,000 calibration points depending on alpha; fewer points give valid but more conservative (larger) sets.

## Limitations
- The guarantee is marginal over images, not per image or per pixel; a specific district map can still miss more than alpha.
- Needs calibration data drawn from the same distribution as deployment; season, sensor geometry or region shift breaks it.
- The CLT bound is only asymptotically valid; finite-sample bounds are more conservative.
- Requires a monotone nested family, which constrains how the mask is post-processed.

## What it means for SatClip
- Adopt: set the flood (or water, burn-scar) mask threshold with RCPS on labelled Indian events, using a per-component missed-area loss like the paper's so small inundated villages count as much as a large river reach. State alpha and delta on the evidence card ("misses at most 10% of flooded area on typical scenes, with 90% confidence in that bound").
- Adopt: prefer RCPS (high-probability) over plain CRC (entry 133, expected-value) when the receipt must make a promise an auditor can check, and record alpha, delta, the bound used, the calibration set ID and its size in the receipt.
- Adopt: maintain separate calibration sets per regime (monsoon S1 VV/VH, dry season, terrain classes) because the guarantee holds only under exchangeability; when the query falls outside every calibrated regime, abstain and say which labelled data would be needed.
- Watch: with a few hundred labelled Indian scenes the sets will be conservative; show this as a wider "possibly flooded" band rather than hiding it.
