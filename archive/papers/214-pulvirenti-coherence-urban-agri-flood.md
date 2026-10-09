---
id: 214
title: "Use of SAR Data for Detecting Floodwater in Urban and Agricultural Areas: The Role of the Interferometric Coherence"
authors: "Luca Pulvirenti, Marco Chini, Nazzareno Pierdicca, Giorgio Boni"
year: 2016
venue: "IEEE Transactions on Geoscience and Remote Sensing, 54(3), 1532-1544 (2016), DOI 10.1109/TGRS.2015.2482001"
link: https://doi.org/10.1109/TGRS.2015.2482001
code: "None found"
category: change-detection
era: historical
tags: [insar-coherence, urban-flood, flooded-vegetation, agriculture, cosmo-skymed, multitemporal, double-bounce, emilia-romagna]
verified: "2026-10-09 via curl to api.crossref.org (title, authors, journal, volume, issue, pages, DOI) and api.semanticscholar.org (abstract elided, paywalled); WebFetch of the Sapienza IRIS record iris.uniroma1.it/handle/11573/1090666 (abstract content). Full text not read"
takeaway: "Multitemporal InSAR coherence catches floodwater in towns and crop fields that intensity thresholds miss or confuse, and can tell receded water from standing water; SatClip's GRD-based pipeline cannot use it today, so urban and flooded-crop pixels must be flagged as unreliable"
---

# Pulvirenti et al. 2016, coherence for urban and agricultural floods

## Problem
SAR intensity works well for open floodwater, but flooded vegetation and flooded urban areas give ambiguous signals: floodwater under crops or between buildings can raise backscatter through double bounce rather than lower it. Intensity-only maps therefore miss or misclassify these areas.

## Approach
- Lay out the scattering theory for how floodwater changes interferometric coherence in agricultural and urban settings.
- Use a multitemporal series of coherence (from repeat-pass interferometric pairs) together with intensity, and track how coherence changes through the event.

## Data and benchmarks
- The January 2014 flood in Emilia-Romagna, Italy.
- COSMO-SkyMed X-band images, using the constellation's short revisit and a dedicated acquisition plan that yielded an interferometric series over the event.

## Key results
- Adding the multitemporal coherence trend substantially reduced classification errors compared with intensity alone (exact figures not read; paywalled).
- Coherence separated areas where water had receded from areas where it persisted.
- In one case, coherence allowed a change in water level to be measured.

## Limitations
- One event, X-band, with a tailored acquisition plan; Sentinel-1 is C-band with a 6 to 12 day revisit, so crop decorrelation between passes is likely stronger than in this X-band case (not tested in the paper).
- Needs complex (SLC) data and interferometric processing, which is far heavier than GRD thresholding.

## What it means for SatClip
- Avoid in sar_water_otsu: do not report urban or flooded-crop pixels as "dry" just because gamma0 did not drop; the Planetary Computer sentinel-1-rtc collection is derived from GRD amplitude and carries no phase, so coherence cannot be computed from it.
- Adopt: mark built-up pixels (for example from a global built-up layer) and actively flooded-crop seasons as "SAR intensity unreliable" in answers.
- Adopt in sar_logratio_change: treat a backscatter increase over paddy or built-up areas during a flood as a possible flooded-vegetation or double-bounce signal, and surface it as "possible flooding, low confidence" rather than ignoring positive log-ratios.
- Future: if SatClip ever adds an SLC path, multitemporal coherence is the method to reach for urban and crop flooding.
