---
id: 044
title: "High resolution paddy rice maps in cloud-prone Bangladesh and Northeast India using Sentinel-1 data"
authors: "Mrinal Singha, Jinwei Dong, Geli Zhang, Xiangming Xiao"
year: 2019
venue: "Scientific Data, 6, Article 26, DOI 10.1038/s41597-019-0036-3"
link: https://doi.org/10.1038/s41597-019-0036-3
code: "none (maps released as GeoTIFF on figshare)"
category: indian-context
era: historical
tags: [rice-mapping, paddy, sentinel-1, vh, random-forest, google-earth-engine, northeast-india, assam, bangladesh, cloud-prone, crop-mask]
verified: "2026-10-04 via https://pmc.ncbi.nlm.nih.gov/articles/PMC6472375"
takeaway: "Sentinel-1 VH time series plus random forest mapped 2017 paddy at 10 m in Northeast India and Bangladesh per season (Boro, Aus, Aman) at 94 to 98% OA; reuse as a crop mask and adopt VH time series for rice questions"
---

# Paddy rice maps for Northeast India and Bangladesh from Sentinel-1

## Problem
Northeast India and Bangladesh are among the cloudiest rice-growing regions in the world, so optical rice maps are coarse (500 m class) or gappy. Agriculture and food security planning needs 10 m rice maps by season.

## Approach
Sentinel-1 VH backscatter time series for 2017 were assembled in Google Earth Engine. VH was chosen because it is more sensitive than VV to rice growth stages (the flooded transplanting dip followed by a rise as the canopy grows). Separate random forest models (500 trees) were trained for the three rice seasons: Boro (December to April), Aus (April to July) and Aman (July to November).

## Data and benchmarks
469 areas of interest labelled using very high resolution Google Earth imagery, more than 2,000 field photos (2015), Sentinel-2 imagery and the Global Field Photo Library; split 30% training and 70% validation. Outputs compared with MODIS-based and IRRI rice products.

## Key results
- Overall accuracy: Boro 94.2%, Aus 98.3%, Aman 95.2%.
- User's / producer's accuracy for rice: Boro 82.4 / 95.0%, Aus 99.4 / 90.6%, Aman 92.8 / 86.0%.
- Spatially consistent with MODIS and IRRI maps while 10 m instead of 500 m or coarser.
- The authors stress that in cloud-prone months there may be no usable optical observation for one or two months.

## Limitations
- Single year (2017); no year-to-year transfer test.
- Mixed pixels in small fields next to vegetation or water, and incidence angle effects on backscatter.
- Training labels partly from 2015 field photos and image interpretation, so label noise is possible.
- Region is Northeast India and Bangladesh; not tested on Indo-Gangetic or southern rice systems.

## What it means for SatClip
- Adopt VH time series features (the transplanting minimum and growth rise) as the transparent instrument for "was rice planted here this season" questions; report the curve on the card instead of a black-box class.
- Use the published 2017 figshare maps as an optional crop mask for Assam and the Northeast when intersecting flood extent with paddy, labelled with their year.
- Use the season calendar (Boro, Aus, Aman locally; kharif and rabi nationally) to set date windows automatically, and abstain when the query window misses the transplanting dip.
- Beat it on recency and abstention: compute masks per year on demand from STAC-listed Sentinel-1 scenes, and flag pixels with mixed or angle-sensitive signal as low confidence.
</content>
</invoke>
