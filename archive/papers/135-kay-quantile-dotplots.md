---
id: 135
title: "When (ish) is My Bus? User-centered Visualizations of Uncertainty in Everyday, Mobile Predictive Systems"
authors: "Matthew Kay, Tara Kola, Jessica R. Hullman, Sean A. Munson"
year: 2016
venue: "CHI 2016 (Proceedings of the 2016 CHI Conference on Human Factors in Computing Systems, pp. 5092-5103)"
link: https://doi.org/10.1145/2858036.2858558
code: "none found in the paper; quantile dotplots are later implemented in the authors' R package ggdist (not checked for this entry)"
category: human-factors
era: historical
tags: [uncertainty-visualization, quantile-dotplot, mobile, non-experts, frequency-framing]
verified: "2026-10-07 via https://api.crossref.org/works/10.1145/2858036.2858558 (title, authors, pages, year) and the author-hosted PDF at https://www.mjskay.com/papers/chi_2016_uncertain_bus.pdf (abstract, survey of 172 users, about 1.15x variance reduction, participant counts)"
takeaway: "Non-experts on a phone read uncertainty best as a small number of countable discrete outcomes, so SatClip's confidence meter and flooded-area range should use a frequency framing (for example 20 dots) instead of a density curve or a bare percentage"
---

# Kay et al. 2016, quantile dotplots for mobile uncertainty

## Problem
People use real-time predictions (here, bus arrival times) on phones to make quick decisions, but apps show point estimates and users may not realise the prediction is uncertain. Standard uncertainty charts are not designed for small screens, little time and no training.

## Approach
- Literature review on how lay people reason about probability, which favours discrete, frequency-style representations.
- Survey of 172 users of the OneBusAway transit app to identify their goals (for example when to leave, how long to wait) and what uncertainty information they want.
- Iterative design of several mobile uncertainty displays, introducing the quantile dotplot: a continuous predictive distribution drawn as a fixed number of dots (each dot an equally likely outcome), so readers can count dots to get probabilities.
- Online controlled experiment comparing dotplots (20 and 100 dots), density plots and other designs on probability estimation questions.

## Data and benchmarks
Survey of 172 app users; online experiment with several hundred participants after exclusions (the paper reports 320 in one layout condition and 221 in another). Stimuli used realistic bus prediction distributions with fake route names.

## Key results
- Quantile dotplots with few dots (20) reduced the variance of people's probability estimates by about 1.15 times relative to density plots and supported more confident estimates.
- With 100 dots, performance looked similar to density plots, consistent with people estimating area instead of counting when dots get too many.
- Users' stated goals map naturally onto threshold questions ("what is the chance I miss it if I leave now"), which counting dots answers directly.

## Limitations
- One everyday domain (transit) with mostly Western, tech-savvy participants recruited online.
- Measures estimation accuracy and confidence, not real decisions with stakes.
- Effect size is modest; the gain is mainly in consistency of estimates.

## What it means for SatClip
- Show the headline number's uncertainty as a small discrete set, for example a 20-dot strip for "flooded area between X and Y km2" or "17 of 20 similar past cases were correct", rather than a smooth curve or only a percent.
- Keep dot counts low enough to count on a low-end Android phone screen; test 10 or 20 dots with field officers.
- Phrase confidence as a frequency in the card text (for example "in about 4 of 5 comparable checks") to match how non-experts reason, and keep the abstention state when the dots would spread too widely to be useful.
