---
id: 104
title: "Analysis of Wheat Crop Forecasts, in India, Generated Using Remote Sensing Data, under FASAL Project"
authors: "S. Kumar, S. Saxena, S. K. Dubey, K. Chaudhary, S. Sehgal, Neetu, S. S. Ray"
year: 2019
venue: "Int. Arch. Photogramm. Remote Sens. Spatial Inf. Sci., XLII-3/W6: 223-228 (ISPRS-GEOGLAM-ISRS workshop, New Delhi, Feb 2019)"
link: https://doi.org/10.5194/isprs-archives-XLII-3-W6-223-2019
code: "none found"
category: indian-context
era: historical
tags: [india, fasal, mncfc, crop-forecasting, wheat, sentinel-2, resourcesat-2, district-statistics, official-statistics]
verified: "2026-10-06 via https://isprs-archives.copernicus.org/articles/XLII-3-W6/223/2019/ (abstract and PDF read) and https://desagri.gov.in/programs-schemes/forecasting-agricultural-output-using-space-agro-meteorology-and-land-based-observations-fasal/ (FASAL programme page); exact per-year RMSE values in the paper's tables were not transcribed"
takeaway: "India's official crop forecasting already compares satellite area estimates with government statistics by deviation, RMSE and correlation at district level, so SatClip should validate its agriculture instrument the same way and report the deviation on the evidence card"
---

# FASAL wheat forecasts (MNCFC)

## Problem
FASAL (Forecasting Agricultural output using Space, Agro-meteorology and Land based observations) gives the Ministry of Agriculture pre-harvest forecasts of crop area and production. The paper asks how well the satellite based wheat forecasts matched the Directorate of Economics and Statistics (DES) final figures from 2013 to 2017.

## Approach
The Mahalanobis National Crop Forecast Centre (MNCFC), which runs FASAL operationally, moved from a sample segment approach with single date Resourcesat-2 AWiFS data (2013-14) to district level complete enumeration with LISS-III (23.5 m) and Landsat-8 (30 m), and then to Sentinel-2 MSI at 10 m. Wheat is classified per district and yield comes from spectral and weather based models. Estimates are compared with DES using relative deviation (national), RMSE and correlation (state) and correlation (district).

## Data and benchmarks
Multi-year IRS, Landsat-8 and Sentinel-2 imagery over the major wheat states (the paper notes Uttar Pradesh, Madhya Pradesh and Punjab hold most of the area), ground truth points, and DES official statistics as the reference.

## Key results
- The paper's national comparison reports relative deviations of -3.93 percent for area and -7.64 percent for production, and links low production estimates to 2015 hail and heavy rain damage.
- A sample classification accuracy assessment shows overall accuracy of about 84.8 percent.
- Accuracy and precision improved over 2013 to 2017 as resolution and ground truth density increased.

## Limitations
Wheat is a rabi crop mapped with cloud free optical data; the method does not transfer directly to the monsoon kharif season. Results are compared to DES figures that are themselves estimates, and the authors call for more ground truth per district and higher resolution data for block and village level outputs.

## What it means for SatClip
- Adopt the validation protocol: for any agriculture answer, report deviation from official district statistics where they exist, not just pixel accuracy.
- The trend toward 10 m Sentinel data in FASAL supports SatClip's choice of public Sentinel-1/2 via STAC.
- Beat in kharif: optical FASAL methods struggle under monsoon cloud, so SatClip's SAR-first NDVI fallback logic (abstain on optical if cloudy, use Sentinel-1) fills a real gap.
