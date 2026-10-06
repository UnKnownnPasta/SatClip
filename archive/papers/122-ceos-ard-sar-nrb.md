---
id: 122
title: "CEOS-ARD Product Family Specification: Synthetic Aperture Radar (Normalised Radar Backscatter [NRB], Polarimetric Radar, Ocean Radar Backscatter, Geocoded SLC, Interferometric Radar, Composite Backscatter), Version 1.3.1"
authors: "Committee on Earth Observation Satellites (CEOS) Land Surface Imaging Virtual Constellation; document history credits Charbonneau, Rosenqvist, Truckenbrodt, Small, Zhou, et al."
year: 2026
venue: "CEOS Analysis Ready Data Product Family Specification, v1.3.1 (July 2026); successor to CARD4L NRB PFS v5.5"
link: https://ceos.org/ard/files/PFS/SAR/v1.3.1/CEOS-ARD_PFS_SAR_v1.3.1.pdf
code: none found (specification; CEOS-ARD GitHub linked from https://ceos.org/ard/)
category: data-infrastructure
era: recent
tags: [ceos-ard, card4l, analysis-ready-data, sar, gamma0, rtc, normalised-radar-backscatter, metadata, data-mask]
verified: "2026-10-06 via https://ceos.org/ard/ (spec listing, v1.3.1 dated 11 July 2026) and the PFS PDF itself (NRB definition, Threshold/Goal structure, data mask, scattering area and local incidence angle layers, DEM requirements); exact numeric radiometric and geometric accuracy thresholds not extracted"
takeaway: "CEOS-ARD NRB is the checklist for what a trustworthy gamma0 RTC input looks like (data mask with layover and shadow, local incidence angle, scattering area, DEM provenance), and SatClip should record which of these its RTC source supplies on every evidence card"
---

# CEOS-ARD SAR Product Family Specification (NRB)

## Problem
SAR users spend much of their effort on preprocessing (calibration, terrain correction, geocoding) and different producers do it differently, so backscatter from different providers, tracks or dates is not directly comparable. CEOS defines Analysis Ready Data as products processed to a minimum set of requirements so they can be analysed immediately and combined through time.

## Approach
- One combined SAR specification (merged in 2022 to 2023 from the earlier CARD4L NRB v5.5 and POL v3.5 documents, with "Target" renamed "Goal") covering six product types, of which NRB is the land backscatter product.
- NRB requires Radiometric Terrain Correction and delivery in the gamma-nought convention following Small (2011), with optional sigma-nought conversion layer.
- Each item is graded as Threshold (minimum to qualify) or Goal (desired), across general metadata, per-pixel metadata, radiometric corrections and geometric corrections; producers self-assess and are peer reviewed.
- Per-pixel layers include a data mask (Goal level adds explicit layover and radar shadow bits, ocean, DEM gap filling), a DEM-based scattering area image, local incidence angle, and optionally the per-pixel DEM and acquisition ID for mosaics.

## Data and benchmarks
This is a specification, not an experiment. The CEOS site keeps a table of datasets assessed as CEOS-ARD or under review, with self-assessments and peer review outcomes.

## Key results
The main output is a shared definition: an NRB product carries enough metadata (orbit, DEM used and its resolution, calibration accuracy, noise equivalent levels, ENL) that a user can judge fitness for a task without reprocessing.

## Limitations
- Compliance is self-assessed then peer reviewed; a product claiming RTC gamma0 is not automatically CEOS-ARD.
- Many fields are Goal, not Threshold, so two compliant products can still differ in what masks they ship.
- The spec does not prescribe a speckle filter or water threshold; downstream algorithms remain the user's job.

## What it means for SatClip
- Use NRB as the quality checklist for SatClip's gamma0 RTC inputs. The Planetary Computer sentinel-1-rtc items seen on 2026-10-06 expose only vv and vh COG assets, so layover and shadow must come from nodata or be derived; note this gap in the evidence card instead of assuming it.
- Kittler-Illingworth water thresholding is badly fooled by radar shadow (dark like water). Mask shadow and layover before thresholding in hilly districts (Assam, Uttarakhand), and abstain when the masked fraction of the district is high.
- Record in the receipt: RTC provider, DEM name, orbit type (precise vs restituted), polarisation and ENL if present. These are the NRB fields that most affect comparability between the pre-flood and flood dates used by log-ratio change.
- Only compare dates from the same relative orbit and RTC source, which NRB's comparability goal assumes.
