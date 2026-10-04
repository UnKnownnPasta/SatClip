---
id: 046
title: "Flood Affected Area Atlas of India - Satellite based study"
authors: "National Remote Sensing Centre (NRSC), ISRO, for the National Disaster Management Authority (NDMA)"
year: 2023
venue: "Official technical document, NRSC/ISRO (released 11 March 2023), hosted on NDEM"
link: https://ndem.nrsc.gov.in/documents/downloads/allindia_flood_techdoc.pdf
code: none
category: indian-context
era: recent
tags: [nrsc, isro, ndem, flood-atlas, flood-frequency, sar, optical, india, official-methodology, ndma]
verified: "2026-10-04 via https://ndem.nrsc.gov.in/documents/downloads/allindia_flood_techdoc.pdf"
takeaway: "The official Indian baseline: 25 years (1998 to 2022) of IRS and foreign optical/SAR flood layers, SAR water by variable thresholding, validated by state agencies; SatClip should complement it, not compete"
---

# Flood Affected Area Atlas of India (NRSC/ISRO, 2023)

## Problem
India needs a consistent national record of which areas flood and how often, to plan mitigation and relief. Event maps exist (NRSC produces them through its Decision Support Centre and NDEM), but a multi-decade, all-India synthesis was missing.

## Approach
NRSC, at the request of NDMA, compiled flood inundation layers from historical satellite data acquired between 1998 and 2022. Inputs are Indian Remote Sensing (IRS) satellites plus foreign optical and microwave (SAR) data. For optical data, unsupervised classification separates the active river channel, tributaries and water bodies. For SAR, a variable threshold technique is applied to backscatter, then isolated pixels are removed by grouping. Permanent water bodies, river bank lines and active channels are used as reference layers so only flood water is counted, and results are intersected with land use / land cover at 1:250,000 scale. Central Water Commission gauge levels for the same period are used as supporting information.

## Data and benchmarks
25 years of flood-season imagery (specific sensors such as RISAT-1, Radarsat or Sentinel-1 are not named in the document text we read). Validation: state-level maps were validated by the disaster management organisations of major flood-prone states. Outputs are district and state flood-affected area statistics and digital maps to be hosted on the NDEM geoportal. The release note confirms it was released on 11 March 2023 at the third session of the National Platform for Disaster Risk Reduction.

## Key results
A national flood-affected area layer and district/state statistics. We could not confirm any headline totals (total area affected, share of geographic area, top states) from the pages we fetched; check the atlas tables before quoting a number.

## Limitations
- The document acknowledges flash floods are largely unmapped because of satellite data gaps, and that actual flooded area may exceed what the satellites captured (images rarely coincide with peak flood).
- Thresholds are described as "variable" without published values, so the method cannot be reproduced independently.
- Coarse land cover scale (1:250,000) limits field-level crop impact estimates.
- Permanent water and salt pans are excluded by design.

## What it means for SatClip
- Treat this as the authoritative Indian baseline and say so: when a user asks "does this area usually flood?", the card should point to the NRSC atlas or NDEM layer as the official reference and present our Sentinel-1 result as an independent, dated, re-runnable observation.
- Adopt its exclusion logic (permanent water, river channel and salt pans removed before counting flood) so our numbers are comparable with official statistics.
- Beat it on transparency and timeliness: publish the threshold, scene IDs and masks per answer, which the atlas does not, and serve event-time questions within hours of a Sentinel-1 overpass.
- Use its stated blind spot (flash floods, peak missed between overpasses) as an explicit abstention rule: if no acquisition falls within a few days of the claimed date, say the event may have been missed rather than reporting "no flood".
</content>
</invoke>
