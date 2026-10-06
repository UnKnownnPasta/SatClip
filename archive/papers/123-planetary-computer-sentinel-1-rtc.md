---
id: 123
title: "Sentinel 1 Radiometrically Terrain Corrected (RTC), Microsoft Planetary Computer dataset (STAC collection sentinel-1-rtc)"
authors: "Microsoft Planetary Computer (host, licensor); RTC processing by Catalyst"
year: 2022
venue: "Microsoft Planetary Computer dataset catalogue and STAC API (official documentation)"
link: https://planetarycomputer.microsoft.com/dataset/sentinel-1-rtc
code: https://planetarycomputer.microsoft.com/api/stac/v1/collections/sentinel-1-rtc (STAC collection JSON)
category: data-infrastructure
era: recent
tags: [planetary-computer, sentinel-1, rtc, gamma0, stac, cog, sas-token, azure]
verified: "2026-10-06 via https://planetarycomputer.microsoft.com/api/stac/v1/collections/sentinel-1-rtc (description, methodology, CC-BY-4.0, temporal extent from 2014-10-10, providers, msft:requires_account=true), a live item search over Barpeta (S1D item dated 2026-10-02, EPSG:32646, 10 m, vv/vh float32 COGs, nodata -32768) and https://planetarycomputer.microsoft.com/api/sas/v1/token/sentinel-1-rtc (token endpoint answered anonymously); year 2022 is the approximate public release year and was not confirmed from an official page; whether anonymous tokens can actually read the blobs was not tested"
takeaway: "Planetary Computer's sentinel-1-rtc is the most direct source of the gamma0 RTC that SatClip's SAR instruments need, but it is flagged account-required and ships only vv and vh, so SatClip must treat token failure as a normal failover case and derive its own shadow mask"
---

# Planetary Computer Sentinel-1 RTC

## Problem
Raw Sentinel-1 GRD backscatter is distorted by terrain: slopes facing the radar look bright and back slopes dark, which swamps the land cover signal and breaks comparisons across tracks. Most users cannot run terrain correction themselves at scale.

## Approach
- Starts from ESA Level-1 GRD (IW mode only), calibrates to flat-earth gamma using ESA calibration coefficients, then applies radiometric terrain flattening following Small (2011) with PlanetDEM as the elevation source.
- Illuminated area per pixel is estimated from DEM facets projected onto the plane perpendicular to the line of sight; pixels not illuminated are flagged as shadow.
- Output is orthorectified to the local UTM zone at native sample spacing (not snapped to a fixed grid), stored as Cloud Optimized GeoTIFFs on Azure Blob Storage and indexed in a STAC API with sar, sat, proj and s1 extension fields.

## Data and benchmarks
- Global IW coverage from 2014-10-10, open ended, licensed CC-BY-4.0.
- A live search on 2026-10-06 over Barpeta, Assam returned a Sentinel-1D item from 2026-10-02 (descending, relative orbit 77, VV+VH, 10 m, float32 linear power COGs, nodata -32768), so the new Sentinel-1D is already flowing in.
- No accuracy benchmark is published on the dataset page.

## Key results
Provides analysis-ready gamma0 per scene with STAC metadata rich enough to filter by orbit direction, relative orbit and polarisation before opening any pixels.

## Limitations
- Collection metadata says a Planetary Computer account is required to obtain SAS tokens for this dataset, unlike most PC collections; tokens expire (the one fetched had roughly one day of validity).
- Items expose only vv and vh (plus preview and tilejson); no separate data mask, local incidence angle or scattering area layer, so it falls short of the per-pixel layers CEOS-ARD NRB describes.
- Commercial processing chain (Catalyst) with limited public validation; not snapped to a common grid, so multi-date stacks need reprojection.

## What it means for SatClip
- Make PC sentinel-1-rtc the first choice for SAR instruments, and filter STAC queries on sat:relative_orbit and sat:orbit_state so pre and post scenes for log-ratio change share geometry.
- Wrap SAS signing (planetary_computer.sign) in the failover layer: a 401, 403 or expired token should trigger fallback to Earth Search or Copernicus Data Space GRD with SatClip's own calibration, and the evidence card must say which source and processing were used.
- Cache tokens with their expiry and re-sign before tile workers start, so a long district job does not fail midway.
- Derive a shadow and layover proxy from nodata plus a DEM slope check before Kittler-Illingworth thresholding, since the dataset does not ship one.
- Credit "Catalyst / Microsoft Planetary Computer, CC-BY-4.0" in the card to meet the licence.
