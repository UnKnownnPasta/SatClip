---
id: 102
title: "National Database for Emergency Management (NDEM): Web enabled Geospatial Portal"
authors: "National Remote Sensing Centre (NRSC), ISRO, for the Ministry of Home Affairs"
year: 2017
venue: "NRSC brochure for NDEM version 3.0, April 2017, Hyderabad"
link: https://ndem.nrsc.gov.in/documents/downloads/NDEM_Brochure_V3.pdf
code: "none found"
category: indian-context
era: recent
tags: [india, disaster-management, ndem, nrsc, mha, decision-support, flood-inundation, gis-database]
verified: "2026-10-06 via https://ndem.nrsc.gov.in/documents/downloads/NDEM_Brochure_V3.pdf (full text read) and https://www.nrsc.gov.in/readmore_NDEM; later NDEM 5.0 release mentioned in news but its details were not checked"
takeaway: "NDEM is the official channel through which district disaster managers already receive NRSC flood inundation maps, so SatClip must position as a fast, auditable complement and export in formats NDEM users can ingest"
---

# NDEM: National Database for Emergency Management

## Problem
Disaster managers in India need one trusted place that combines base maps, hazard layers and live event information during an emergency. Before NDEM, these data sat with many separate nodal agencies.

## Approach
The Ministry of Home Affairs conceived NDEM and NRSC/ISRO built and runs it as a national repository of GIS data plus decision support system (DSS) tools. Version 1.0 (2013) ran over a satellite based VPN; version 2.0 (2015) moved to secured internet access with a disaster dashboard and mobile relief apps; version 3.0 (2017) was rebuilt on open source tools (OpenLayers 3, Bootstrap, MVC), adding incident reporting, Hindi and English interfaces, network analysis and social media inputs.

## Data and benchmarks
The brochure lists a multi-scale geospatial database: the whole country at 1:50,000, 350 multi-hazard prone districts at 1:10,000, and five megacities at 1:2,000. The dashboard integrates IMD rainfall, CWC river water levels, cloud motion and city forecasts, and hosts value added satellite products (including flood inundation maps) for major disasters from 2013 onward. Services cover all 36 States/UTs.

## Key results
NDEM is operational for central and state users, with flood hazard maps, flood hazard zonation maps and near real time flood inundation maps organised by disaster phase (mitigation, preparedness, response, recovery). No accuracy figures are given; it is a service, not a study.

## Limitations
Access is restricted to authorised government users, so the public and researchers cannot query it. Products are event maps prepared by NRSC analysts; the brochure does not describe uncertainty, per-district confidence, or how a user can re-run the analysis.

## What it means for SatClip
- Do not pitch SatClip as a replacement: district officials will cross-check against NDEM and NRSC maps, so the evidence card should state which public Sentinel-1 scenes were used and acknowledge that official NRSC maps may use other sensors.
- Adopt NDEM's phase framing (preparedness, response, recovery) to route questions, for example a change instrument for response and a multi-year frequency query for mitigation.
- Beat: offer what NDEM does not show, namely on-demand numbers for any date, a confidence value, abstention, and a re-runnable receipt.
