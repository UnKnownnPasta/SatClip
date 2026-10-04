---
id: 069
title: "Earth observation tools and services to increase the effectiveness of humanitarian assistance"
authors: "Stefan Lang, Petra Füreder, Barbara Riedler, Lorenz Wendt, Andreas Braun, Dirk Tiede, Elisabeth Schoepfer, Peter Zeil, Kristin Spröhnle, Kerstin Kulessa, Edith Rogenhofer, Magdalena Bäuerl, Alexander Öze, Gina Schwendemann, Volker Hochschild"
year: 2019
venue: "European Journal of Remote Sensing 53(sup2): 67-85 (published online 30 October 2019; issue dated 2020)"
link: https://doi.org/10.1080/22797254.2019.1684208
code: none
category: human-factors
era: historical
tags: [humanitarian, disaster-response, eo-uptake, user-needs, ngo, msf, information-service, operational]
verified: "2026-10-04 via https://api.crossref.org/works/10.1080/22797254.2019.1684208 and https://api.semanticscholar.org (abstract); publisher page returned 403"
takeaway: "Field report on delivering EO information to MSF and other NGOs, stressing that trust, reliability and workflow fit, not algorithms, limit uptake; SatClip should design around delivery and trust for non-expert responders"
---

# Earth observation tools and services to increase the effectiveness of humanitarian assistance

## Problem
Humanitarian organisations need current information for mission planning, displacement camps, vaccination and nutrition campaigns, damage assessment and water supply, and EO can provide much of it. Yet the abstract stresses that building and sustaining a trusted, reliable information service remains hard. The paper asks what has worked and what is still open in the use and uptake of EO in humanitarian action, technically and organisationally.

## Approach
An experience-based review grounded in an operational EO information service built for Médecins Sans Frontières (MSF) and extended to other NGOs. It covers population estimation from (semi-)automated dwelling counts in very high resolution optical imagery, data integration including radar, and service elements for environmental and ground or surface water monitoring. It examines the workflow from information extraction to delivery across a range of application scenarios.

## Data and benchmarks
Case studies and service workflows rather than a controlled benchmark. We could only read the abstract and bibliographic record (the publisher page blocked our fetcher), so we cannot confirm specific case locations, accuracy numbers or user-feedback methods from the full text.

## Key results
- Humanitarian actors have adopted EO quickly and shaped it to their needs.
- The hard problem is organisational as much as technical: delivering information that responders trust and can fit into their workflows.
- The paper presents first operational solutions as a customised service portfolio. (Detailed findings not confirmed by us beyond the abstract.)

## Limitations
- Practitioner perspective from one service provider and its NGO partners; not a systematic user study.
- Focus on very high resolution optical imagery (dwelling counts), more detailed than Sentinel-1/2 at 10 m.
- Full text not read by us; claims beyond the abstract should be checked before citing.

## What it means for SatClip
- Treat uptake as the primary risk: district officials, like NGO staff, will judge SatClip on whether its outputs are trustworthy and arrive in a usable form, not on model novelty.
- Deliver in the formats responders already use: a one-page evidence card that can be printed or forwarded on WhatsApp, plus a GeoJSON or KML of the mask for anyone with GIS support.
- Be explicit about service reliability: show data latency (scene date versus today) prominently, since stale data is a key reason responders distrust EO products.
- Scope to what 10 m Sentinel data can support (flood extent, crop and vegetation change), and abstain on questions needing building-level detail.
- Plan a short co-design session with a district disaster management office, mirroring the service-provider and NGO partnership model described here.
