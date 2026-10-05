---
id: 099
title: "2026 IEEE GRSS Data Fusion Contest: SAR Temporal Storytelling"
authors: "IEEE GRSS Image Analysis and Data Fusion Technical Committee with Capella Space"
year: 2026
venue: "IEEE GRSS Data Fusion Contest (results at IGARSS 2026, Washington DC; papers planned for IGARSS 2026 Proceedings and IEEE JSTARS)"
link: https://www.grss-ieee.org/resources/news/in-focus-inside-the-2026-ieee-grss-data-fusion-contest/
code: none found (contest required winners to make code public; individual repositories not checked)
category: upcoming
era: upcoming
tags: [challenge, sar, x-band, insar, time-series, change-detection, capella, self-supervised]
verified: "2026-10-05 via https://www.grss-ieee.org/resources/news/in-focus-inside-the-2026-ieee-grss-data-fusion-contest/ and https://www.grss-ieee.org/community/technical-committees/winners-of-the-2026-ieee-grss-data-fusion-contest-sar-temporal-storytelling/ ; dataset download page and quantitative scores not found"
takeaway: "The field's flagship 2026 contest asked teams to turn SAR time series into readable stories of change, validating SatClip's framing; but entries were open-ended research on commercial X-band, not abstaining, receipted answers on free data"
---

# 2026 IEEE GRSS Data Fusion Contest: SAR Temporal Storytelling

## Problem
SAR sees through clouds and darkness, so time series of SAR images can document how places change. Turning those stacks into understandable narratives of change ("what happened here, and when") is hard, and large open SAR time-series datasets with interferometric pairs were rare.

## Approach
An open-ended single track: participants chose their own objective and method, and could submit any analysis or visualization that told a temporal story from the SAR data. Judging criteria listed were technical rigour, creativity, clarity of presentation, practical relevance and use of the dataset. Code had to be made public.

## Data and benchmarks
- More than 1,500 high-resolution X-band SAR collects from Capella Space, globally distributed, multiple imaging modes.
- More than 17,000 potential InSAR pairs, described by GRSS as the first large-scale commercial radar dataset of its kind for this use.
- No fixed benchmark metric; ranking was by expert judging.

## Key results
Four co-equal winners (announced July 2026):
1. Phase Gradient Voting, unwrap-free deformation screening for X-band InSAR stacks (Chiba University).
2. TRISAR, self-supervised triplet metric learning for temporal SAR interpretation (ELTE / HUN-REN SZTAKI).
3. T-SAR-JEPA, temporal self-supervised anomaly detection in SAR amplitude stacks (independent / Dakota State University).
4. FiLM-GPNet, pseudo-supervised phase restoration for large InSAR stacks (Universities of Oulu and Turku).
No quantitative scores were published on the pages we read.

## Limitations
- Commercial X-band data under a contest licence; not reproducible on free data and not routinely available over Indian districts.
- No common metric, so results are hard to compare.
- Winners focus on representation learning and InSAR processing; none, from the titles and summaries, is a natural-language question-answering or decision-support system, and we found no mention of calibrated confidence or abstention.

## What it means for SatClip
- Not a direct threat; it is a signal that "SAR temporal storytelling" is now a mainstream research goal, which supports SatClip's pitch that officials need narratives backed by SAR time series.
- Adopt: the T-SAR-JEPA style idea (anomaly scoring on amplitude stacks) could become a "this change is unusual for this place" flag next to our log-ratio instrument; worth reading the IGARSS paper when available.
- Beat: SatClip tells the story in plain language for a specific district question, on free Sentinel-1 data, with scene IDs and dates as receipts, and refuses when the evidence is weak. Contest entries tell stories to experts.
- Use in the pitch: cite the contest theme as evidence of demand, then show SatClip as the accountable, deployable version for Indian monsoon floods.
