---
id: 186
title: "Exploring Sentinel-1 and Sentinel-2 diversity for flood inundation mapping using deep learning"
authors: "Goutam Konapala, Sujay V. Kumar, Shahryar Khalique Ahmad"
year: 2021
venue: "ISPRS Journal of Photogrammetry and Remote Sensing, 180, 163-173"
link: https://doi.org/10.1016/j.isprsjprs.2021.08.016
code: "Not verified (no repository found in the sources read)"
category: sar-optical-fusion
era: recent
tags: [flood-mapping, sentinel-1, sentinel-2, dem, terrain, sen1floods11, u-net, hsv, water-indices, fusion]
verified: "2026-10-08 via curl to api.crossref.org (journal title, three authors, volume 180, pages 163-173, October 2021) and api.openalex.org for the authors' EGU General Assembly 2021 abstract of the same title (doi 10.5194/egusphere-egu21-10445, Konapala and Kumar); the journal abstract was not retrievable (Crossref and OpenAlex had none; ScienceDirect page not readable), so all numbers below come from the EGU 2021 abstract and may differ from the final paper; WebFetch permission prompt timed out so curl was used"
takeaway: "On Sen1Floods11, adding a DEM to Sentinel-1 raised median flood F1 from 0.63 to 0.74 (EGU abstract figures), strong evidence that SatClip's SAR water instrument needs terrain inputs or masks"
---

# Konapala, Kumar and Ahmad 2021, Sentinel-1 and Sentinel-2 combinations for flood mapping

## Problem
SAR is cloud-proof but noisy and confused by terrain; optical indices are clean but blocked by cloud. Which band combinations, and which extra layers, actually help a deep model map flood water?

## Approach
- Trains a U-Net on many input combinations: Sentinel-1 VV and VH, Sentinel-2 bands and water indices, an HSV (hue, saturation, value) transform of Sentinel-2, and a DEM.
- Uses the 446 hand-labelled Sen1Floods11 chips (entry 022), split 313 train, 44 validation, 89 test, over 11 flood events.

## Data and benchmarks
- Sen1Floods11 hand labels; metric is per-image F1, reported as the median across test chips.

## Key results
(From the EGU 2021 abstract; final journal numbers not verified.)
- Sentinel-1 only: median F1 0.63. Sentinel-1 plus DEM: 0.74.
- Sentinel-2 HSV transform alone: median F1 0.94, ahead of common water indices; HSV plus Sentinel-1: 0.95.

## Limitations
- Small test set (89 chips); medians hide failure cases.
- The strong optical results assume cloud-free Sentinel-2, which is rare during an Indian monsoon flood.
- Sen1Floods11 has few Indian chips, so terrain gains may differ in the Brahmaputra or Kosi plains.

## What it means for SatClip
- Concrete improvement: add elevation information to the SAR water instrument. The cheapest version is a rule mask (HAND or slope from a DEM such as Copernicus GLO-30) that removes "water" on high or steep ground; a learned version would add the DEM as an input channel.
- Adopt: when a cloud-free Sentinel-2 scene exists within the flood window, weight it heavily; optical water evidence is much stronger than SAR alone.
- Avoid citing the 0.94/0.95 figures as SatClip expectations; they are medians on cloud-free chips from one conference abstract.
