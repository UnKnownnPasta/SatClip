---
id: 197
title: "AgriFieldNet Competition Dataset"
authors: "Radiant Earth Foundation and IDinsight"
year: 2022
venue: "Dataset, Version 1.0, Radiant MLHub (now hosted on Source Cooperative), DOI 10.34911/rdnt.wu92p1, published 7 September 2022"
link: https://doi.org/10.34911/rdnt.wu92p1
code: "Data at https://source.coop/radiantearth/agrifieldnet-competition (CC BY 4.0); a community baseline tutorial is linked there"
category: indian-context
era: recent
tags: [india, uttar-pradesh, rajasthan, odisha, bihar, crop-type, sentinel-2, smallholder, ground-reference, dataset, cc-by-4.0, field-ids]
verified: "2026-10-08 via curl to https://api.datacite.org/dois/10.34911/rdnt.wu92p1 (title, creators, year, publisher, licence), curl to the Source Cooperative page and its Documentation.pdf (states, 13 classes, chip size and count, band list, label encoding); WebFetch permission request timed out and these two hosts are outside the arXiv and Crossref fallback list, so this is flagged; imagery acquisition dates and field counts are not stated in the pages read"
takeaway: "An open CC BY 4.0 set of ground-collected crop-type labels for smallholder fields in Uttar Pradesh, Rajasthan, Odisha and Bihar on 10 m Sentinel-2 chips, with field IDs; SatClip can use it to calibrate and test crop answers in the Indo-Gangetic districts it targets, but must source its own dates and Sentinel-1 data"
---

# Radiant Earth Foundation and IDinsight 2022, AgriFieldNet India crop-type dataset

## Problem
Crop-type models for India lack open, field-verified labels, especially for small, mixed fields in northern states where floods and crop losses hit hardest.

## Approach
- Ground reference collected by IDinsight's Data on Demand team; curation and publication by Radiant Earth, funded through the ECAAS initiative.
- Labels rasterised onto Sentinel-2 chips with a separate field-ID layer, so fields split across chips can be grouped and evaluated at field level.
- Released for the AgriFieldNet India competition with separate train and test label collections.

## Data and benchmarks
- 1,217 chips of 256 x 256 pixels in four states: Uttar Pradesh, Rajasthan, Odisha and Bihar.
- Sentinel-2 bands B01 to B12 including B8A (12 bands) resampled to a common 10 m grid; each chip has a crop-ID raster and a field-ID raster with STAC JSON metadata.
- 13 classes: fallow plus wheat, mustard, lentil, green pea, sugarcane, garlic, maize, gram, coriander, potato, berseem (spelled Bersem in the documentation) and rice. Unlabelled pixels have value 0.

## Key results
A dataset, not a method; no benchmark scores are reported in the documentation read.

## Limitations
- Sparse labels: only surveyed fields are labelled, and many pixels in a chip are 0.
- Classes are dominated by rabi crops (wheat, mustard, gram); kharif rice is present but monsoon coverage is not documented.
- No Sentinel-1 data and no acquisition dates in the documentation read, so it is single-sensor and its temporal coverage must be checked before use.
- The current page lists both train and test label folders; how the test split was drawn is not described in the documentation read.

## What it means for SatClip
- Adopt: a CC BY 4.0 Indian ground-truth source in exactly the Bihar and Uttar Pradesh districts SatClip targets; use field IDs to compute field-level reliability diagrams for crop-type or crop-presence answers.
- Adopt: join its fields to SatClip's own Sentinel-1 and Sentinel-2 STAC queries for matching seasons, so calibration uses the same instruments SatClip answers with.
- Avoid: do not mix it with flood calibration; it has no flood labels.
