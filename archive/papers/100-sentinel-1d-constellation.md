---
id: 100
title: "Copernicus Sentinel-1D launch and restored two-satellite Sentinel-1 constellation (Sentinel-1C and 1D)"
authors: "European Space Agency and European Commission (Copernicus); launch by Arianespace"
year: 2025
venue: "ESA press release and Copernicus Sentinels success story (mission announcement)"
link: https://www.esa.int/Newsroom/Press_Releases/Copernicus_Sentinel-1D_reaches_orbit_on_Ariane_6
code: none found (mission; data via Copernicus Data Space Ecosystem)
category: upcoming
era: upcoming
tags: [sentinel-1, sar, c-band, mission, revisit, copernicus, open-data, flood]
verified: "2026-10-05 via https://www.esa.int/Newsroom/Press_Releases/Copernicus_Sentinel-1D_reaches_orbit_on_Ariane_6 and https://sentinels.copernicus.eu/web/success-stories/-/sentinel-1d-a-new-chapter-for-copernicus ; current commissioning status and exact operational revisit over India not confirmed"
takeaway: "Sentinel-1C (Dec 2024) plus 1D (Nov 2025) restore two-satellite C-band SAR, about 6-day revisit at the equator, which directly raises how often SatClip can answer a flood question with a fresh scene instead of abstaining"
---

# Copernicus Sentinel-1D launch and restored two-satellite Sentinel-1 constellation (Sentinel-1C and 1D)

## Problem
After Sentinel-1B failed in 2022, Sentinel-1 ran on one ageing satellite (1A, launched 2014). Revisit over India dropped to roughly 12 days, which is too slow for many monsoon flood events: the water can recede before the next pass.

## Approach
ESA launched Sentinel-1C in December 2024 and Sentinel-1D on 4 November 2025 (Ariane 6, French Guiana). Sentinel-1C and 1D are to fly 180 degrees apart in a sun-synchronous orbit near 693 km, restoring the two-satellite configuration. Sentinel-1D is set to replace Sentinel-1A. Both carry C-band SAR and an AIS receiver for ship tracking.

## Data and benchmarks
- Data are free and open via the Copernicus Data Space Ecosystem, the same as earlier Sentinel-1 data, and appear in public STAC catalogs that index Sentinel-1 (catalog coverage of 1C/1D not checked here).
- The Copernicus article cites a revisit of about six days at the equator, more frequent at higher latitudes, once both are operating.

## Key results
No benchmark results apply; this is a mission. The practical result is doubled observation frequency for C-band SAR.

## Limitations
- We did not confirm the date Sentinel-1D completed commissioning or when its products became routinely available.
- Acquisition plans over India depend on the Sentinel-1 observation scenario; actual revisit at a given district may differ from the equatorial figure.
- Still C-band: same weaknesses under dense canopy and in urban areas, and wind-roughened water still causes misses.
- Cross-calibration between 1A, 1C and 1D may shift backscatter slightly, which affects fixed thresholds.

## What it means for SatClip
- Not a threat; it strengthens SatClip's core data supply and the free-data argument.
- Adopt: handle platform identifiers S1C and S1D in STAC queries and receipts (do not hard-code S1A). Record the platform on the evidence card.
- Calibration: re-check SAR water thresholds and log-ratio change thresholds per platform, and keep the abstain rule when pre and post scenes come from different platforms or orbits.
- Product impact: more frequent passes mean fewer "no recent scene, abstaining" answers during the monsoon; measure and report the abstention rate before and after 1D data appear in pilot districts.
- Pairs naturally with NISAR (entry 098) for a C-band plus L-band roadmap.
