---
id: 187
title: "Satellite-Based Flood Mapping through Bayesian Inference from a Sentinel-1 SAR Datacube"
authors: "Bernhard Bauer-Marschallinger, Senmao Cao, Mark Edwin Tupas, Florian Roth, Claudio Navacchi, Thomas Melzer, Vahid Freeman, Wolfgang Wagner"
year: 2022
venue: "Remote Sensing (MDPI), 14(15), 3673"
link: https://doi.org/10.3390/rs14153673
code: "Not verified (no repository found in the sources read)"
category: sar-optical-fusion
era: recent
tags: [sentinel-1, flood-mapping, bayesian, uncertainty, datacube, harmonic-model, seasonality, no-sensitivity-mask, copernicus-gfm, near-real-time, greece]
verified: "2026-10-08 via curl to api.crossref.org (title, eight authors, volume 14, issue 15, article 3673, 31 July 2022) and api.openalex.org (abstract); MDPI full text was not readable from this environment, so method details beyond the abstract are not given; WebFetch permission prompt timed out so curl was used"
takeaway: "The TU Wien member of the Copernicus GFM ensemble classifies each Sentinel-1 pixel by Bayes rule against its own seasonal backscatter history, giving a per-pixel flood probability and a no-sensitivity mask; the cleanest template for SatClip's calibrated SAR water confidence"
---

# Bauer-Marschallinger et al. 2022, Bayesian flood mapping from a Sentinel-1 datacube

## Problem
Fixed or scene-wide thresholds fail where land is naturally dark in SAR (sand, tarmac, some crops), where seasons change backscatter, and in steep terrain. A global, automatic, near-real-time flood service needs a method that adapts per pixel and says how sure it is.

## Approach
- Builds a datacube of every past Sentinel-1 observation for each pixel and fits a harmonic (seasonal) model, giving the expected non-flood backscatter for each day of the year.
- A global flood backscatter distribution is learned from hand-picked wind-free and frost-free flood images.
- A new image is classified per pixel with simple Bayes inference between the flood and seasonal non-flood distributions; the posterior also serves as an uncertainty value.
- A datacube-derived no-sensitivity mask removes pixels where SAR cannot see water change (obstructing land cover, unfavourable viewing geometry).

## Data and benchmarks
- Six-year Sentinel-1 datacube over Greece; test case is the 2018 Thessaly flood, compared with microwave and optical reference maps.

## Key results
- About 96% overall accuracy with few false positives, per the abstract. Other metrics were not read.
- The abstract states the algorithm is part of the ensemble flood mapping product of the Copernicus Emergency Management Service Global Flood Monitoring (GFM) component. (That the ensemble has three algorithms is from general knowledge, not from the sources read.)

## Limitations
- Needs years of history per pixel; new or recently changed land loses its baseline.
- Overall accuracy is dominated by dry land and flatters flood detection; single region test.
- Wind-roughened or vegetated flood water still breaks the flood signature.

## What it means for SatClip
- Adopt: replace or complement the scene-wide Otsu threshold with a per-pixel "is this darker than normal for this date" test using a few past Sentinel-1 passes from the same orbit. This turns flood extent into a change question and cuts false water from always-dark surfaces.
- Adopt: report the posterior probability as SatClip's per-pixel water confidence, and abstain in the no-sensitivity mask instead of calling it dry.
- Adopt: for India, read GFM's published ensemble flood extent and its exclusion mask as a cross-check before showing SatClip's own map.
