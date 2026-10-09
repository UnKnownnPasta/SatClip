---
id: 211
title: "Deriving exclusion maps from C-band SAR time-series in support of floodwater mapping"
authors: "Jie Zhao, Ramona Pelich, Renaud Hostache, Patrick Matgen, Senmao Cao, Wolfgang Wagner, Marco Chini"
year: 2021
venue: "Remote Sensing of Environment, 265, 112668 (2021), DOI 10.1016/j.rse.2021.112668; open access (CC BY per Semantic Scholar). Earlier conference version in ISPRS Annals V-1-2020, 395-400"
link: https://doi.org/10.1016/j.rse.2021.112668
code: "No repository found in the material read"
category: sar-optical-fusion
era: recent
tags: [exclusion-map, sentinel-1, time-series, radar-shadow, layover, urban, dense-vegetation, sand, flood-mapping, false-water, gfm]
verified: "2026-10-09 via curl to api.crossref.org (title, authors, journal, volume, article number; also the 2020 ISPRS Annals precursor with its abstract) and api.semanticscholar.org (full RSE abstract, open-access status). ScienceDirect full text could not be fetched (robots blocked), so thresholds and per-site numbers are not reproduced"
takeaway: "Every SAR flood map should ship with an exclusion map of pixels where SAR cannot see water (shadow, layover, dense forest, urban, sand), derived from the Sentinel-1 time series itself via temporal median, minimum and standard deviation; SatClip should compute one per district and report those pixels as unknown, not dry"
---

# Zhao et al. 2021, SAR exclusion maps

## Problem
Intensity-based flood mapping relies on floodwater darkening the backscatter. In some places this never happens or is ambiguous: radar shadow and layover from terrain, dense forest, urban areas, sand and other permanently dark surfaces. If a flood map simply labels these as dry (or wet), it misleads users. The authors argue each flood map should come with an explicit exclusion map.

## Approach
- Build the exclusion map (EX-map) from the multi-year Sentinel-1 backscatter time series, not from external land cover.
- Use three per-pixel temporal indicators: the temporal median, the temporal minimum and the temporal standard deviation of backscatter. Pixels whose statistics show insensitivity to water (always dark, always bright, or never changing) are excluded.
- The 2020 precursor paper also combined pixel-based time-series analysis with object-based spatial analysis.

## Data and benchmarks
- Sentinel-1 data from 2014 to 2019 over six representative study sites (the precursor used 922 Sentinel-1 tiles over the River Severn, UK, and Lake Maggiore, Italy, at 20 m).
- Reference layers: a global land cover map, DEM-derived shadow and layover masks, the Global Urban Footprint and a Sand Exclusion Layer.

## Key results
- The RSE abstract reports that the EX-map was consistent with the reference maps; per-site agreement numbers were not available in the material read.
- The 2020 precursor reported roughly 63% agreement with reference data from several sources.

## Limitations
- Thresholds on the temporal indicators were not visible in the abstract; they may need retuning for monsoon climates where many pixels are seasonally wet.
- Seasonal paddy and floodplain wetlands are wet for months each year; time-series statistics could flag them as permanent water look-alikes or leave them in, and the paper's sites (Europe and others) may not cover this case.
- Full text not read here.

## What it means for SatClip
- Adopt in sar_water_otsu: precompute per-district temporal median, minimum and standard deviation of VV and VH gamma0 from the sentinel-1-rtc archive (dry-season and full-year stacks), and mark pixels that are always dark (water look-alikes such as sand or tarmac) or never respond as excluded. GFM's operational variant flags pixels below -15 dB in more than 70% of the series (per GFM product documentation).
- Adopt: answer flood-extent questions with three classes (water, not water, cannot tell) and report the excluded area in the answer text, so officials see where SatClip is blind.
- Adopt in sar_logratio_change: skip excluded pixels before the log-ratio test, since shadow and layover produce change artefacts with orbit differences.
- Avoid: do not exclude seasonal paddy outright; keep it as a separate "seasonally wet" class so crop-change questions still work.
