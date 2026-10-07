---
id: 145
title: "Detecting trend and seasonal changes in satellite image time series"
authors: "Jan Verbesselt, Rob Hyndman, Glenn Newnham, Darius Culvenor"
year: 2010
venue: "Remote Sensing of Environment, 114(1): 106-115"
link: https://doi.org/10.1016/j.rse.2009.08.014
code: "https://cran.r-project.org/package=bfast (R package bfast, page fetched and cites this paper)"
category: change-detection
era: historical
tags: [bfast, time-series, ndvi, seasonality, structural-breaks, phenology, disturbance]
verified: "2026-10-07 via https://api.crossref.org/works/10.1016/j.rse.2009.08.014 (title, four authors, venue, volume, issue, pages, 2010), abstract from the Wageningen University research portal page, and the CRAN bfast package page"
takeaway: "Seasonality alone can masquerade as change in a two-date NDVI difference; SatClip's crop-change instrument should compare against the same season's expected NDVI and abstain when a drop could be ordinary phenology or harvest"
---

# Verbesselt et al. 2010, BFAST

## Problem
Many change detection methods compare dates without accounting for seasonal cycles, so normal vegetation phenology gets confused with real land-cover change or disturbance.

## Approach
- Breaks For Additive Seasonal and Trend (BFAST): decompose a vegetation index time series into trend, seasonal and remainder components.
- Iteratively estimate the number and timing of breaks in both the trend and the seasonal components, and characterise each break by magnitude and direction.
- Breaks in the trend are read as disturbances (for example fire); breaks in the seasonal pattern as phenological or land-cover changes.

## Data and benchmarks
- Simulated 16-day NDVI series with varying seasonality, noise and inserted abrupt changes.
- 16-day MODIS NDVI composites over a forested study area in south-eastern Australia.

## Key results
- On simulations, BFAST detected changes larger than about 0.1 NDVI across noise levels of roughly 0.01 to 0.07 and seasonal amplitudes of 0.1 to 0.5 NDVI.
- On MODIS, it located and characterised spatial and temporal forest changes; per the abstract it needs no land-cover normalisation, reference period or predefined change trajectory.

## Limitations
- Needs a long, regular time series; two dates are not enough, and cloud gaps in monsoon Sentinel-2 data break that assumption.
- Validated on forest at 250 m scale, not on smallholder crops in India; detection limits from simulation may not transfer.
- Offline fitting; the later BFAST Monitor variant addresses near real-time use.

## What it means for SatClip
- A two-date NDVI drop during a kharif or rabi season can be harvest, not damage. SatClip should compare the observed change against the expected seasonal change for that crop window (from prior years or a seasonal model) before calling it crop loss.
- The roughly 0.1 NDVI detection floor under realistic noise is a useful sanity bound: smaller differences should trigger low confidence or abstention unless the receipt shows strong supporting evidence.
- Where a cloud-free history exists, a BFAST-style break check is a cheap secondary instrument that can be cited in the receipt alongside the two-date difference.
