---
id: 106
title: "Flood Hazard Zonation Atlas of Assam: Using multi-sensor satellite data (1998-2023)"
authors: "National Remote Sensing Centre (NRSC), ISRO, project team led by K. H. V. Durga Rao and A. V. Suresh Babu, with NDMA and Assam State Disaster Management Authority"
year: 2025
venue: "NRSC technical report NRSC-RSA-DMSG-FMHAD-MAY,2025-TR-2791, Version 3, June 2025"
link: https://www.nrsc.gov.in/nrscnew/assets/pdf/Flood_Hazard_Zonation_Atlas_of_Assam_using_multi_sensor_satellite_data1998_2023.pdf
code: "none found"
category: indian-context
era: recent
tags: [india, assam, flood-hazard, nrsc, ndma, asdma, radarsat, risat-1a, sentinel-1, village-level, district-level]
verified: "2026-10-06 via the NRSC PDF linked above (front matter, executive summary, criteria, observations and limitations read); substitutes for the suggested NDMA flood guidelines, whose PDF on ndma.gov.in could not be fetched"
takeaway: "NRSC's official Assam atlas classifies every 50 m pixel and village by how many times it flooded in 26 years, giving SatClip both a prior for plausibility checks and the hazard vocabulary district officials already use"
---

# NRSC Flood Hazard Zonation Atlas of Assam (1998-2023)

## Problem
Planners need to know not just where it flooded this year but which areas flood repeatedly, so they can site relief camps, shelters and infrastructure and draft district disaster management plans. At the request of NDMA, NRSC updated its Assam atlas (versions from 2011 and 2015) to cover 26 years.

## Approach
NRSC compiled flood inundation layers from 389 satellite datasets, Indian (IRS optical, RISAT-1, RISAT-1A/EOS-04) and foreign (RADARSAT-1/2, Sentinel-1A/1B, TerraSAR-X, ALOS-2 and others, some through the International Charter), at a common 50 m grid. Each pixel's flood frequency maps to five classes set by an NDMA expert committee: very low (1 to 3 times), low (4 to 6), moderate (7 to 10), high (11 to 14) and very high (more than 14). Villages take the dominant class by area, and a district Flood Hazard Index adds CWC water levels from 31 gauge stations.

## Data and benchmarks
Satellite flood layers 1998 to 2023, CWC gauge records, Resourcesat-2 LISS-IV land use for crop exposure, and new district boundaries from ASDMA. ASDMA district and circle offices field-validated the maps and their feedback was folded into the atlas.

## Key results
- Cumulative flood-affected area in Assam of 27.08 lakh hectares over 1998 to 2023.
- 1,876 villages in the very high class across 119 circles, and 11,039 villages in the very low class.
- 17 districts ranked Hazard Rank I, 4 Rank II and 14 Rank III; about 18.22 lakh hectares of cropped land at risk.

## Limitations
The report itself notes that satellite passes may not coincide with flood peaks and that inundation includes embankment breaches and rain ponding. Flood frequency depends on how many events were imaged each year, which varies across sensors and decades, and the 50 m grid is coarse for small fields.

## What it means for SatClip
- Adopt the NDMA hazard classes and village or circle granularity in answers, so "very high hazard village" means the same thing in SatClip as in the official atlas.
- Use the atlas frequency as a prior: a SatClip water mask that floods a pixel the atlas never saw flooded, or misses a very high zone during a declared flood, should lower the confidence or trigger a review flag.
- Beat on timeliness: the atlas is a multi-year summary released after the fact; SatClip answers for a specific date with the exact Sentinel-1 scenes on the card.
