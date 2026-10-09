---
id: 212
title: "Probabilistic Flood Mapping Using Synthetic Aperture Radar Data"
authors: "Laura Giustarini, Renaud Hostache, Dmitri Kavetski, Marco Chini, Giovanni Corato, Stefan Schlaffer, Patrick Matgen"
year: 2016
venue: "IEEE Transactions on Geoscience and Remote Sensing, 54(12), 6958-6969 (2016), DOI 10.1109/TGRS.2016.2592951"
link: https://doi.org/10.1109/TGRS.2016.2592951
code: "None found"
category: trust-calibration
era: historical
tags: [probabilistic-flood-map, per-pixel-probability, histogram-decomposition, bayes, reliability-diagram, sar, data-assimilation, uncertainty]
verified: "2026-10-09 via curl to api.crossref.org (title, authors, journal, volume, issue, pages, DOI) and api.semanticscholar.org (authors, venue; abstract elided, paywalled); WebFetch of the LIST publication page at list.lu (abstract content, study sites, reliability-diagram error range). IEEE Xplore page did not render; full text not read"
takeaway: "Turns a SAR flood map into a per-pixel flood probability by fitting water and non-water backscatter distributions to the image histogram and applying Bayes; the direct upgrade path from SatClip's single Otsu cut to a calibrated posterior"
---

# Giustarini et al. 2016, probabilistic SAR flood mapping

## Problem
Binary SAR flood maps hide uncertainty: pixels near the threshold are reported as confidently as pixels deep in either class. Hydrodynamic modellers, and anyone deciding on relief, need to know how likely each pixel is to be flooded.

## Approach
- Decompose the backscatter histogram of a flood image into two class-conditional distributions, one for open water and one for non-water.
- Combine these distributions with Bayes' rule to give each pixel a probability of being flooded, rather than a hard label.
- Argue that such probabilistic maps can be assimilated directly into hydraulic models without first converting them to water levels.

## Data and benchmarks
- Four SAR images over two floodplains: the River Severn (UK) and the Red River (US).
- Validation against flood maps derived from aerial photography, assessed with reliability diagrams.

## Key results
- Reliability diagrams showed close agreement between predicted probabilities and observed flood frequency; the reported error values ranged from 0.04 to 0.23 across cases (as summarised from the abstract on the LIST publication page).
- Details such as the distribution families used and prior choice were not confirmed (paywalled).

## Limitations
- Tested on four images in two temperate, mostly rural floodplains; no monsoon paddy, urban or steep terrain.
- Probabilities are only as good as the two-distribution fit; if the histogram is not bimodal (little water in the tile, or vegetation and shadow mixing in) the posterior is unreliable.
- The probability reflects backscatter ambiguity only, not exclusion-zone blindness such as shadow or urban areas.

## What it means for SatClip
- Adopt in sar_water_otsu: keep Otsu for the cut, but also fit two distributions (for example Gaussians in dB) to the same tile histogram and output P(water | gamma0) per pixel; report area as an expected value plus a range (sum of probabilities, and area above 0.25 and 0.75).
- Adopt: check calibration with a reliability diagram on Sen1Floods11 hand labels, and on Indian labels when available, before showing probabilities to officials.
- Adopt: refuse or warn when the tile histogram is not bimodal, since both Otsu and this method fail there.
- Avoid: do not present the posterior as covering shadow, layover or urban pixels; combine it with the exclusion and HAND masks (entries 210, 211) and label those pixels unknown.
