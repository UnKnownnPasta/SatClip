---
id: 103
title: "Yield Estimation System based on Technology (YES-TECH) under PMFBY: Manual for Implementation"
authors: "Mahalanobis National Crop Forecast Centre (MNCFC), Department of Agriculture and Farmers Welfare, Government of India"
year: 2023
venue: "Official manual, Ministry of Agriculture and Farmers Welfare, New Delhi, January 2023"
link: https://apsac.ap.gov.in/wp-content/uploads/2023/01/Document2.pdf
code: "none found"
category: indian-context
era: recent
tags: [india, crop-insurance, pmfby, yield-estimation, sentinel-1, eos-04, crop-mask, mncfc, policy]
verified: "2026-10-06 via https://apsac.ap.gov.in/wp-content/uploads/2023/01/Document2.pdf (manual text read; hosted by Andhra Pradesh Space Applications Centre) and https://pmfby.gov.in/pdf/EoI_for_empanelment_of_WIP_under_YE_TECH_181023.pdf (MNCFC EoI, Sept 2023, which cites the manual); a copy on pmfby.gov.in itself was not located"
takeaway: "YES-TECH makes satellite crop masks and modelled yields legally count for 30 percent of insurance loss assessment, and it lists Sentinel-1 and EOS-04 backscatter as inputs, so SatClip's agriculture answers should be framed at insurance unit level with explicit validation"
---

# PMFBY YES-TECH manual

## Problem
Crop insurance payouts under Pradhan Mantri Fasal Bima Yojana (PMFBY, since 2016) depend on yields per Insurance Unit (IU), traditionally measured through Crop Cutting Experiments (CCEs). The manual names their weaknesses: few measurements, slow turnaround and exposure to human error.

## Approach
After pilot studies in 2019 and 2020 across agro-climatic zones, an expert committee recommended five approaches for paddy and wheat: semi-physical (radiation use efficiency) models, AI models, crop simulation models, ensembles of these, and an indirect parametric crop health index. The manual makes accurate current and historical crop maps the first step for all five, built from SAR and optical data at 5 to 30 m.

## Data and benchmarks
Input tables list Sentinel-1 SAR (20 m) for crop masks and sowing dates, Sentinel-2 for NDVI and LSWI, Sentinel-3 FAPAR, and radar backscatter features (VH, VV, RVI) from Sentinel-1 and EOS-4. Validation uses good quality CCE yields at IU level from 2017 onward, scored with MAE, RMSE or NRMSE. Modelled yields must be produced for the current year and at least five historical years.

## Key results
- From the 2023 season, claims blend 70 percent CCE yield with 30 percent technology-based yield (direct approach), or the same 70/30 split on deviations from threshold (indirect approach).
- States must give technology at least 30 percent weight and may choose more, subject to MNCFC approval.
- MNCFC later invited agencies to be empanelled to run these estimates (EoI, September 2023).

## Limitations
The manual is procedural: it sets inputs, roles and weights, but reports no accuracy numbers for the five approaches. It currently covers paddy and wheat only, and technology outputs are explicitly not used to change long-run average or threshold yields.

## What it means for SatClip
- Adopt the Insurance Unit (often Gram Panchayat) as a supported spatial unit for agriculture questions, alongside districts.
- SatClip's Sentinel-1 crop and flood masks are exactly the kind of input YES-TECH names; an evidence card that reports the mask, scene dates and a validation score against CCE data speaks the agriculture officer's language.
- Avoid presenting a yield number: SatClip should stay with measurable quantities (sown or flooded area, NDVI change) and abstain on yield unless a validated model is plugged in.
