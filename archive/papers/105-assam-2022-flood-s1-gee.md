---
id: 105
title: "Large-Scale Flood Hazard Monitoring and Impact Assessment on Landscape: Representative Case Study in India"
authors: "Bijay Halder, Subhadip Barman, Papiya Banik, Puja Das, Jatisankar Bandyopadhyay, Fredolin Tangang, Shamsuddin Shahid, Chaitanya B. Pande, Baqer Al-Ramadan, Zaher Mundher Yaseen"
year: 2023
venue: "Sustainability (MDPI), 15(14): 11413"
link: https://doi.org/10.3390/su151411413
code: "none found"
category: indian-context
era: recent
tags: [india, assam, flood-2022, sentinel-1, google-earth-engine, mndwi, landsat, district-statistics, change-detection]
verified: "2026-10-06 via https://api.crossref.org/works/10.3390/su151411413 (title, authors, volume, abstract) and https://pure.kfupm.edu.sa/en/publications/large-scale-flood-hazard-monitoring-and-impact-assessment-on-land/; mdpi.com full text was blocked, so thresholds, polarisation, scene dates and any accuracy assessment were not confirmed"
takeaway: "A peer-reviewed Assam 2022 Sentinel-1 study reports a flooded area of about 33,900 km2 (43 percent of the state) with no stated uncertainty, which is exactly the kind of headline number SatClip should reproduce with scene IDs, a confidence and an abstention rule"
---

# Assam 2022 floods with Sentinel-1 on Earth Engine

## Problem
Assam floods every monsoon. The authors report that the 2022 floods hit about 1.9 million people and 2,930 villages and killed 54 people, and they set out to quantify inundation and associated vegetation loss across the state.

## Approach
On Google Earth Engine, the study compares pre-flood and post-flood Sentinel-1 C-band GRD scenes to delineate inundation, and uses Landsat 8 and 9 OLI/TIRS with the Modified Normalized Difference Water Index (MNDWI) to separate pre and post flood water and land conditions. Results are summarised per district.

## Data and benchmarks
Sentinel-1 GRD (pre and post event), Landsat 8 and 9, and Assam district boundaries. From the abstract, no benchmark dataset or independent reference map is named; the exact SAR threshold and polarisation could not be confirmed because the full text was not reachable.

## Key results
- About 33,902 km2 of flood inundation out of a 78,438 km2 state area, and about 24,507 km2 of vegetation loss.
- Cachar, Kokrajhar, Jorhat, Kamrup and Dhubri were the most affected districts; riverine areas, Dispur and Guwahati, and southern and eastern Assam stood out.

## Limitations
The abstract gives point estimates with no confidence interval or accuracy figure. Combining SAR inundation with optical indices in a cloudy monsoon month raises questions about which acquisition dates were actually usable. The very large flooded fraction is not checked here against NRSC's official event maps.

## What it means for SatClip
- Use this as a regression target: rerun SatClip's Kittler-Illingworth Sentinel-1 instrument on the same 2022 dates for the five named districts and compare, logging where the numbers diverge.
- The study shows why the evidence card matters: a single statewide number without dates, polarisation or uncertainty cannot be audited, while SatClip's receipt can.
- Avoid mixing optical indices into flood-extent numbers during monsoon unless cloud masks pass; keep MNDWI as a secondary check that can trigger abstention.
