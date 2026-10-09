---
id: 216
title: "A change detection approach to flood inundation mapping using multi-temporal Sentinel-1 SAR images, the Brahmaputra River, Assam (India): 2015–2020"
authors: "Darshil Vekaria, Shard Chander, R P Singh, Sudhanshu Dixit"
year: 2023
venue: "Journal of Earth System Science, 132, article 3 (issue 1, March 2023; published online 27 December 2022), DOI 10.1007/s12040-022-02020-x"
link: https://doi.org/10.1007/s12040-022-02020-x
code: "Not stated in the material read (Google Earth Engine workflow)"
category: indian-context
era: recent
tags: [assam, brahmaputra, sentinel-1, change-detection, google-earth-engine, permanent-water-mask, shadow-mask, crop-damage, imerg, india]
verified: "2026-10-09 via curl to api.crossref.org (title, four authors, journal, volume, issue, article number, DOI) and WebFetch of the Springer article page (abstract content, accuracy figures, access status: paywalled). Full text not read; polarisation, threshold values and the validation reference source were not visible"
takeaway: "Six-year Sentinel-1 change-detection flood record for the Brahmaputra in Assam with permanent-water and shadow removal, reporting about 6 lakh ha flooded in peak years; a direct Indian analogue of sar_logratio_change, though its validation reference is unclear"
---

# Vekaria et al. 2023, Assam Sentinel-1 change detection 2015 to 2020

## Problem
Assam floods every monsoon along the Brahmaputra, but multi-year, consistent flood extent records from SAR were limited. The authors (affiliations not confirmed on the page read) set out to map flooding across six seasons and relate it to rainfall and crops.

## Approach
- Automatic change detection between pre-flood and flood Sentinel-1 images in Google Earth Engine, about 144 SAR images in total.
- Binarisation by thresholding, then removal of permanent water bodies and of terrain shadow.
- Link inundation trends to IMERG precipitation and overlay crop areas to estimate crop damage.

## Data and benchmarks
- Sentinel-1 SAR over the Brahmaputra valley, Assam, monsoon seasons 2015 to 2020.
- IMERG satellite precipitation for trend interpretation.
- Accuracy assessment is reported for 2019 and 2020; the reference source is not clear from the page read (acknowledgements mention Assam State Disaster Management Authority flood reports, but their role in validation was not confirmed).

## Key results
- Inundated area of about 6 lakh hectares in 2015-2016, about 3.5 lakh hectares in 2017-2018, and about 6 lakh hectares again in 2019-2020 (as summarised on the article page).
- Overall accuracy of 93.6% (2019) and 95.15% (2020), stated for "pre-flood events"; what exactly was assessed is unclear without the full text.
- The July 2020 flood affected the most cropland in the record.

## Limitations
- Overall accuracy on flood maps is dominated by the large dry class and says little about flood-class precision or recall.
- Threshold values, polarisation and the validation reference were not visible; reproducibility cannot be judged from the abstract.
- No HAND mask or urban handling described in the abstract; no per-pixel uncertainty.

## What it means for SatClip
- Adopt in sar_logratio_change: the same structure (pre-flood reference, flood image, threshold, then subtract permanent water and shadow) is a sanity baseline for Assam; SatClip's district totals for 2019 and 2020 should be of the same order as this record, and large gaps should trigger review.
- Adopt: report flooded cropland as a separate figure, since this is what Assam users asked about in this study.
- Avoid: do not adopt overall accuracy as SatClip's headline metric; report flood-class IoU, precision and recall on hand labels.
- Action: contact the authors for their validation points; Indian labels are SatClip's biggest gap.
