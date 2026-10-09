---
id: 221
title: "Uncertainty in three dimensions: the challenges of communicating probabilistic flood forecast maps"
authors: "Valérie Jean, Marie-Amélie Boucher, Anissa Frini, Dominic Roussel"
year: 2023
venue: "Hydrology and Earth System Sciences (HESS), 27, 3351-3373, DOI 10.5194/hess-27-3351-2023"
link: https://doi.org/10.5194/hess-27-3351-2023
code: "None (qualitative interview study)"
category: human-factors
era: recent
tags: [uncertainty-visualisation, flood-maps, probabilistic-maps, map-design, decision-makers, municipalities, colour-scale, qualitative-study]
verified: "2026-10-09 via WebSearch then WebFetch of hess.copernicus.org/articles/27/3351/2023/ (title, authors, volume, pages, DOI, publication date 21 September 2023, methods, reported percentages, limitations); the last ~8% of the page (end of prototype 4 results, discussion and conclusions) was not read"
takeaway: "Interviews with 140 ministry, municipal, agency, farmer and citizen respondents found probabilistic flood maps are often misread (exceedance probabilities, depth versus level) and that words plus numbers are preferred; SatClip's map cards should show extent first, use plain probability wording, and avoid user-adjusted probability sliders"
---

# Jean et al. 2023, Communicating probabilistic flood forecast maps

## Problem
Flood forecasts carry uncertainty in space, time and magnitude. Agencies want to show it on maps, but little evidence existed on whether public-sector and lay users can read probabilistic flood maps or what they actually need.

## Approach
- Qualitative, participatory study in southern Quebec, run on video calls from June 2020 to June 2021, sessions of about two hours.
- Part 1 asked about information needs (forecast horizon, time step, update frequency); part 2 showed four interactive map prototypes built from hydraulic model output for one river.
- Prototypes: (1) a slider choosing an exceedance probability, showing extent and depth; (2) a hydrograph with median, low and high scenarios; (3) a fixed-flow map (withheld from citizens as too technical); (4) choose a depth, see probability of exceeding it.
- Two colour scales compared: a blue water scale and a traffic-light scale. Transcripts analysed thematically.

## Data and benchmarks
- 140 respondents: 28 from five provincial ministries, 62 from 52 municipalities, 12 from 9 territorial organisations, 33 citizens in 11 focus groups and 5 farmers in 2 focus groups.
- No quantitative accuracy benchmark; findings are interview themes and group percentages.

## Key results
- Probabilities were often misinterpreted: non-exceedance probability confused people, depth was confused with water level, and some assumed the median scenario was not a 50% case.
- Respondents generally wanted words and numbers together, though the preferred order varied by group.
- Citizens and farmers cared mostly about where water would be on their land (extent), less about depth.
- Municipalities, organisations and farmers clearly preferred the blue scale; ministries and citizens rated both similarly.
- 1 to 3 days was the most cited useful forecast horizon (68% of ministry and 48% of municipal respondents).

## Limitations
- Qualitative, single region, French-language; percentages come from small uneven groups (only five farmers).
- Small-group sessions may have shaped answers; prototypes were mock-ups of one river.
- Participants had little prior flood-map experience, which may not match trained officials.
- Concerns forecasts, not observed satellite flood extent, though the reading problems carry over.

## What it means for SatClip
- Adopt: lead the evidence card with the observed flood extent inside the region mask and the area number; put any probability layer second, never as the only view.
- Adopt: write probabilities as plain statements tied to the number ("about 8 in 10 chance this pixel was flooded on 14 Aug, Sentinel-1 scene X") rather than exceedance or non-exceedance terms, and always show words with the number.
- Adopt: use a single-hue water scale for flood extent and reserve the traffic-light colours for the confidence meter, so the two are not confused.
- Avoid: do not give users a probability slider that redraws the map; it invites misreading. Offer a fixed calibrated band (likely, possible) and a short legend.
- Test: repeat a small version of this study with Indian district disaster officers in at least two languages before release.
