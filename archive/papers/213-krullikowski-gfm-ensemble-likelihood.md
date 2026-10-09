---
id: 213
title: "Estimating Ensemble Likelihoods for the Sentinel-1-Based Global Flood Monitoring Product of the Copernicus Emergency Management Service"
authors: "Christian Krullikowski, Candace Chow, Marc Wieland, Sandro Martinis, Bernhard Bauer-Marschallinger, Florian Roth, Patrick Matgen, Marco Chini, Renaud Hostache, Yu Li, Peter Salamon"
year: 2023
venue: "IEEE Journal of Selected Topics in Applied Earth Observations and Remote Sensing (JSTARS), 16, 6917-6930 (2023), DOI 10.1109/JSTARS.2023.3292350; preprint on TechRxiv, DOI 10.36227/techrxiv.22688101"
link: https://doi.org/10.1109/JSTARS.2023.3292350
code: "Not released; the likelihood layer is distributed operationally as part of Copernicus GFM"
category: trust-calibration
era: recent
tags: [gfm, copernicus, ensemble, likelihood, uncertainty, sentinel-1, flood-mapping, user-communication, exclusion-mask]
verified: "2026-10-09 via curl to api.crossref.org (JSTARS record: title, 11 authors, volume, pages, DOI; TechRxiv preprint record with full abstract; the preprint lists 10 authors, without Renaud Hostache); WebFetch of the GFM Product Definition wiki at extwiki.eodc.eu (likelihood layer range and the 50 cut-off, LIST/DLR/TUW algorithms, TUW uncertainty flipped). IEEE Xplore and TechRxiv full text did not render, so harmonisation formulas and any numeric accuracy were not read"
takeaway: "Copernicus GFM gives every flood pixel a 0 to 100 likelihood by harmonising and averaging the uncertainty outputs of three independent Sentinel-1 algorithms; SatClip can mimic this cheaply by running two or three of its own water tests and reporting agreement as confidence"
---

# Krullikowski et al. 2023, GFM ensemble likelihoods

## Problem
The Copernicus Global Flood Monitoring (GFM) service produces a flood mask for every new Sentinel-1 IW scene worldwide by combining three independently developed algorithms (from DLR, LIST and TU Wien). Each algorithm expresses uncertainty differently, so the service needed a single, comparable per-pixel likelihood to communicate confidence to users.

## Approach
- Each of the three algorithms provides its own classification uncertainty or likelihood.
- These are rescaled to a common range from 0 (low flood likelihood) to 100 (high flood likelihood).
- The ensemble likelihood is the mean of the three harmonised likelihoods. Per the GFM product documentation, the TU Wien uncertainty is flipped before use and a value of 50 separates flooded from unflooded; pixels in the exclusion mask get no likelihood.

## Data and benchmarks
- Two test sites: a real flood event in Myanmar, and a site in Somalia with conditions that are hard for SAR flood detection.

## Key results
- In Myanmar, the ensemble stayed robust where the individual algorithms disagreed, and the likelihood layer conveyed that disagreement to users.
- In Somalia, where misclassification is likely, averaging reduced false detections, and low likelihood values flagged results to use with caution.
- The abstract reports these qualitatively; numeric scores were not read (full text not accessed).

## Limitations
- Averaging rescaled scores from different methods gives a confidence index, not a calibrated probability; a likelihood of 70 is not shown to mean 70% of such pixels are flooded.
- Evaluation on two sites only, neither in South Asia.
- Running three full algorithms is heavier than a single threshold.

## What it means for SatClip
- Adopt in sar_water_otsu: run two or three cheap, different water tests on the same scene (Otsu on VV, Otsu on VH, and a change test against a dry reference from sar_logratio_change) and report per-pixel agreement on a 0 to 100 scale, with the 50 cut used for the mask, mirroring GFM.
- Adopt: show the agreement layer in answers ("3 of 3 methods agree on 80% of this area") which a district official can read without statistics.
- Adopt: where a GFM product exists for the same Sentinel-1 scene, use it as a cross-check and flag big disagreements.
- Avoid: do not call the averaged score a probability until it has been calibrated against labels (entry 212 and the calibration entries such as 131 and 133).
