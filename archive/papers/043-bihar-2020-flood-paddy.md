---
id: 043
title: "Google Earth Engine-Based Identification of Flood Extent and Flood-Affected Paddy Rice Fields Using Sentinel-2 MSI and Sentinel-1 SAR Data in Bihar State, India"
authors: "Himanshu Kumar, Sateesh Kumar Karwariya, Rohan Kumar"
year: 2022
venue: "Journal of the Indian Society of Remote Sensing, 50, 791-803, DOI 10.1007/s12524-021-01487-3"
link: https://doi.org/10.1007/s12524-021-01487-3
code: "none (authors state GEE code available on request)"
category: indian-context
era: recent
tags: [bihar, flood-mapping, sentinel-1, sentinel-2, paddy, crop-damage, google-earth-engine, monsoon-2020, india, flood-duration]
verified: "2026-10-04 via https://link.springer.com/article/10.1007/s12524-021-01487-3"
takeaway: "Bihar monsoon 2020: S1 plus S2 in GEE mapped about 7,019 sq km submerged and water standing on paddy for 50 to 65 days; a model for flood-on-crop questions, but method details sit behind a paywall"
---

# Flood extent and flood-affected paddy in Bihar, 2020

## Problem
North Bihar floods almost every monsoon (Kosi, Gandak, Bagmati and other rivers), and the losses fall heavily on kharif paddy. District and agriculture officials need to know not only where water was, but which rice fields were under water and for how long.

## Approach
All available Sentinel-1 SAR and Sentinel-2 MSI images for June to October 2020 were processed in Google Earth Engine with supporting datasets to map flood progression through the season, then intersected with paddy and population layers to estimate impact and flood duration on fields.

## Data and benchmarks
Sentinel-1 and Sentinel-2 archives for the 2020 monsoon in Bihar, plus auxiliary GEE layers. The open abstract does not describe the validation design.

## Key results
From the abstract:
- About 7,019 sq km was submerged during the 2020 monsoon.
- Floodwater persisted on agricultural fields for 50 to 65 days, causing major crop damage.
- The strongest impacts fell on agricultural land (11.23% of the total area) and population (15.56% of the total population).
Unverified: polarisation, threshold rule, speckle filter, masks, and any accuracy figures (overall accuracy, kappa) are in the paywalled methods; we could not read them, so none are quoted here.

## Limitations
- Method details and accuracy are not openly available; reproducing the result needs a request to the authors.
- One season, one state.
- Duration estimates depend on revisit; with a 6 to 12 day Sentinel-1 cadence (and only Sentinel-1A after the December 2021 Sentinel-1B failure), start and end dates of flooding are uncertain by several days.

## What it means for SatClip
- Adopt its question framing for the crop-insurance user: "how many days was water on paddy in these blocks" is answerable by counting consecutive Sentinel-1 water detections over a crop mask, and the card should show the acquisition dates bounding each run.
- Use Bihar June to October 2020 as a second Indian validation event (after Kerala 2018), comparing our total submerged area with the reported figure of about 7,019 sq km and explaining differences in masks.
- Beat it on openness: publish thresholds, masks and scene IDs in the receipt instead of "code on request".
- State duration uncertainty explicitly (plus or minus the revisit gap) and abstain from day-precise claims when the gap is longer than the user's tolerance.
</content>
</invoke>
