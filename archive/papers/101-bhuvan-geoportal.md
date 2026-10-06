---
id: 101
title: "Bhuvan: ISRO's Geoportal (Gateway to Indian Earth Observation)"
authors: "National Remote Sensing Centre (NRSC), ISRO"
year: 2009
venue: "Official geoportal and brochure, NRSC/ISRO, Hyderabad (portal launched 2009); OGC blog profile by Divya Khanna, 7 Feb 2025"
link: https://bhuvan.nrsc.gov.in/bhuvan/PDF/Bhuvan%20Brochure.pdf
code: "none found"
category: indian-context
era: historical
tags: [india, geoportal, nrsc, isro, ogc-services, wms, irs-data, disaster-support, government]
verified: "2026-10-06 via https://bhuvan.nrsc.gov.in/bhuvan/PDF/Bhuvan%20Brochure.pdf (brochure text read) and https://www.ogc.org/blog-article/bhuvan-transforming-indias-governance-with-geospatial-insights/; no peer-reviewed paper describing Bhuvan was found; brochure publication year not printed; usage figures come from the OGC blog, not an audited source"
takeaway: "Bhuvan is the map Indian officials already know, so SatClip should publish its evidence-card masks as OGC-compatible layers that overlay on Bhuvan rather than ask users to switch platforms"
---

# Bhuvan geoportal (NRSC/ISRO)

## Problem
Indian Remote Sensing (IRS) imagery and the thematic maps derived from it were historically hard for non-specialists to see or reuse. ISRO wanted one public window onto Indian Earth observation that planners, students and administrators could use without GIS software.

## Approach
Bhuvan (Sanskrit for Earth) is a web Earth browser run by NRSC. The brochure describes a 2D client built on OpenLayers, a 3D globe, a mobile client, the NRSC Open EO Data Archive (NOEDA) for downloading IRS data and products, and thematic datasets served as OGC web services for online geoprocessing. It overlays near real time feeds such as automatic weather stations, potential fishing zones, forest fire alerts and agricultural drought assessment.

## Data and benchmarks
Content is multi-sensor, multi-temporal IRS imagery (from AWiFS at 55 m down to 1 to 2.5 m over some cities, with most of India shown at 6 m or better according to the brochure) plus vector thematic layers. The OGC profile lists eight OGC standards in use (WMS, WFS, WCS, CSW, KML, WMTS, WPS, SOS). There is no benchmark: it is an operational service.

## Key results
- The OGC profile (2025) reports about 150,000 unique users per day, around 20 million hits per day and over 100 use cases.
- It hosts monitoring for national schemes such as MGNREGA, PM Awas Yojana and PMGSY, and was used in the 2014 Cyclone Hudhud response.
- Registration is optional for viewing; download and sharing need a single sign-on account.

## Limitations
Bhuvan is a viewer and distribution layer, not a question-answering or measurement system: it shows layers but does not compute a district statistic with uncertainty on demand. Its own imagery is mostly optical IRS data, and the usage numbers above are self-reported.

## What it means for SatClip
- Adopt: expose every evidence card's water or change mask as a WMS/WMTS or COG layer plus a KML so a district officer can drop it onto Bhuvan, which is already the default map in government offices.
- Align district and village boundaries with the ones Bhuvan and NDEM use, so SatClip's percentage-flooded numbers match what officials see elsewhere.
- Beat: Bhuvan cannot answer "how much of Barpeta was flooded on a given date" with scene IDs and a confidence; that gap is SatClip's pitch.
