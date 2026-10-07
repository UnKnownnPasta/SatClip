---
id: 175
title: "GSLV-F17/EOS-05 mission: India's first imaging satellite from geosynchronous orbit"
authors: "Indian Space Research Organisation (ISRO), Office of Media and Public Relations"
year: 2026
venue: "Satellite mission announcement (ISRO mission page and GSLV-F17/EOS-05 mission brochure, revised 31 August 2026)"
link: https://www.isro.gov.in/Mission_GSLVF17.html
code: "Not applicable; no public data access page found"
category: upcoming
era: upcoming
tags: [isro, eos-05, gslv-f17, geosynchronous-imaging, india, mission, revisit, monsoon, data-access-unknown]
verified: "2026-10-07 via curl to https://www.isro.gov.in/ (home page news: launched 4 September 2026 at 02:55 IST; three orbit-raising manoeuvre notices), https://www.isro.gov.in/Mission_GSLVF17.html (mission success, page dated 29 August 2026, description) and the mission brochure PDF (orbit and mass); WebFetch not used for this item; sensor bands, resolution and data policy are not stated in the pages read, so none are given here"
takeaway: "ISRO has put an imaging satellite in geosynchronous orbit over India, which could give many looks per day during monsoon cloud gaps; SatClip should plan an adapter but cannot rely on it until ISRO publishes sensor specs and open data access"
---

# ISRO 2026, GSLV-F17/EOS-05 geosynchronous Earth observation satellite

## Problem
Polar-orbiting satellites such as Sentinel-1 and Sentinel-2 see an Indian district only every few days, and optical passes are often lost to monsoon clouds. A satellite that stares at India from geosynchronous orbit could image the same place many times a day and catch short cloud breaks.

## Approach
- EOS-05 is described by ISRO as a state-of-the-art Earth observation spacecraft and India's first imaging satellite from geosynchronous orbit.
- Launched on GSLV-F17 (19th GSLV flight, 4 m ogive composite fairing) from the Second Launch Pad at Sriharikota; the ISRO home page reports launch on 4 September 2026 at 02:55 IST.
- Brochure: sub-geosynchronous transfer orbit with nominal perigee 170 km, apogee 28,934 km, inclination 19.28 degrees; satellite mass about 2,367 kg. ISRO later reported three orbit-raising manoeuvres, the third described as final.

## Data and benchmarks
None yet. The pages read do not list the imaging payload, spectral bands, spatial resolution, revisit schedule or a data distribution channel (for example Bhoonidhi).

## Key results
- Mission declared successful by ISRO, with the satellite placed in the intended orbit and moved toward its operational orbit.
- No imagery, product specifications or data policy found as of 2026-10-07.

## Limitations
- Specifications not verified: from general knowledge, geosynchronous imagers trade spatial resolution for revisit, so pixels are likely much coarser than Sentinel-2, but this is not confirmed by the sources read.
- If the payload is optical, it still cannot see through monsoon cloud; it would only exploit gaps more often.
- Data may be restricted to government users, which would limit an open, offline tool.

## What it means for SatClip
- Plan: add EOS-05 as a candidate optical instrument in the sensor registry, marked "specs pending", so the intent parser can say "no open EOS-05 data yet" rather than guess.
- Adopt if open: frequent looks could shorten time to a usable cloud-free scene for crop-condition and flood-recession questions, reducing how often SatClip must abstain.
- Do not count on it for the beachhead: SAR (Sentinel-1, NISAR in entry 098) remains the primary flood instrument; revisit this entry when ISRO publishes the payload and data policy.
