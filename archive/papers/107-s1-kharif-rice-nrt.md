---
id: 107
title: "Operational Near Real Time Rice Area Mapping Using Multi-Temporal Sentinel-1 SAR Observations"
authors: "J. D. Mohite, S. A. Sawant, A. Kumar, M. Prajapati, S. V. Pusapati, D. Singh, S. Pappula"
year: 2018
venue: "Int. Arch. Photogramm. Remote Sens. Spatial Inf. Sci., XLII-4: 433-438 (ISPRS TC IV Mid-term Symposium, Delft, Oct 2018)"
link: https://doi.org/10.5194/isprs-archives-XLII-4-433-2018
code: "none found"
category: indian-context
era: historical
tags: [india, andhra-pradesh, kharif, rice, sentinel-1, random-forest, google-earth-engine, early-season, near-real-time]
verified: "2026-10-06 via https://isprs-archives.copernicus.org/articles/XLII-4/433/2018/ (abstract and metadata) and https://api.crossref.org/works/10.5194/isprs-archives-XLII-4-433-2018; full PDF not read, so per-date accuracy tables were not checked"
takeaway: "Kharif rice in coastal Andhra Pradesh can be mapped from Sentinel-1 alone with about 84 percent independent accuracy, and accuracy rises as each new monsoon acquisition arrives, so SatClip's sown-area answers should state how many SAR dates they used and abstain early in the season"
---

# Near real time kharif rice mapping with Sentinel-1

## Problem
Officials, input suppliers and farmers want early, in-season maps of rice area during kharif (June to September), but monsoon cloud cover makes optical data unreliable. The authors aim for an operational, early season rice map that updates as new radar images arrive.

## Approach
Sentinel-1 IW dual polarisation (VV, VH) C-band time series were processed on Google Earth Engine. A Random Forest classifier was trained first on two mid-June images and then retrained each time one more acquisition was added, up to the end of August. The output was masked with an agriculture layer derived from ESA global land cover.

## Data and benchmarks
Four coastal districts of Andhra Pradesh (Guntur, Krishna, East Godavari, West Godavari), kharif 2017. Training labels for rice, non-rice agriculture, water, settlements, forest and aquaculture came from GEE, ESA land cover layers and field observations.

## Key results
- Overall accuracy rose from 78.11 percent to 87.00 percent as images were added; the best model used 30 trees and six images from mid-June to end August.
- An independent stratified random sample gave 84.45 percent accuracy.
- The authors planned to run the method in the 2018 season for incremental near real time estimates.

## Limitations
One season and four districts only, a single classifier, and labels partly from global land cover rather than dense field surveys. Aquaculture ponds in this delta look like flooded paddy in early SAR, a known confusion the abstract lists as a separate class but does not quantify.

## What it means for SatClip
- Adopt the incremental idea: a sown-area answer should list how many Sentinel-1 dates in the season were available, with confidence growing with dates and abstention before enough have arrived.
- Expect confusion between transplanting-stage paddy, aquaculture and flood water; SatClip's flood instrument should mask known paddy and aquaculture or warn about them in July, which matters for Barpeta-type questions.
- Beat: the paper gives one accuracy figure for a whole region; SatClip should give a per-district confidence and the scene list on each card.
