---
id: 124
title: "Copernicus Data Space Ecosystem documentation: STAC product catalogue, OData catalogue and S3 access APIs"
authors: "Copernicus Data Space Ecosystem (European Commission, ESA; operated by a consortium including CloudFerro)"
year: 2025
venue: "Official online documentation, documentation.dataspace.copernicus.eu"
link: https://documentation.dataspace.copernicus.eu/APIs/STAC.html
code: https://browser.stac.dataspace.copernicus.eu (STAC Browser; source linked from docs)
category: data-infrastructure
era: recent
tags: [copernicus-data-space, cdse, stac, odata, s3, sentinel-1, catalogue, failover, openeo]
verified: "2026-10-06 via https://documentation.dataspace.copernicus.eu/APIs/STAC.html (STAC 1.1.0, endpoint https://stac.dataspace.copernicus.eu/v1/, legacy endpoint deprecated from 17 Nov 2025, limited set of collections), https://documentation.dataspace.copernicus.eu/APIs/OData.html (query options and performance tips) and https://documentation.dataspace.copernicus.eu/APIs/S3.html (eodata endpoint, credentials); year 2025 reflects the current STAC endpoint, docs are continuously updated; a direct curl of the STAC collections endpoint did not return JSON from this sandbox, so the live collection list was not confirmed"
takeaway: "CDSE is SatClip's authoritative last-resort catalogue: its new STAC 1.1 endpoint and OData API index every Sentinel product, but pixel access needs S3 credentials and products are mostly SAFE archives, so it is the slowest and most fragile of the three failover routes"
---

# Copernicus Data Space Ecosystem APIs

## Problem
CDSE is the official distribution point for Copernicus Sentinel data, replacing the older SciHub. Programmatic users need search, metadata and bulk access that work at scale.

## Approach
- STAC: a STAC API implementing spec 1.1.0 at https://stac.dataspace.copernicus.eu/v1/, with a STAC Browser GUI. The docs describe it as complementary to OData, with a limited but growing set of collections. The old catalogue.dataspace.copernicus.eu/stac endpoint is deprecated from 17 November 2025.
- OData: the primary catalogue (OASIS standard REST) at catalogue.dataspace.copernicus.eu/odata/v1/Products with $filter, $orderby, $top, $skip, $count and $expand, plus OData Subscriptions for push notification of new products.
- S3: object storage at eodata.dataspace.copernicus.eu (load balanced between CloudFerro and Open Telekom Cloud), requiring per-user access and secret keys generated after registration.
- Other processing APIs are documented alongside: openEO, Sentinel Hub, and a Traceability API.

## Data and benchmarks
Full Sentinel-1, 2, 3, 5P archives plus Copernicus services and some contributing missions. No performance benchmarks are given, but the OData docs advise always filtering by collection name and date range and splitting multi-year searches into per-year queries for speed.

## Key results
Gives a complete, authoritative index of Sentinel products, including the newest Sentinel-1 data, with OData product records that carry the S3 path of each product.

## Limitations
- Sentinel-1 GRD on S3 is in SAFE layout, not analysis-ready RTC; SatClip would need its own calibration and terrain correction.
- Pixel download needs registered credentials, unlike Earth Search's anonymous S3 COGs.
- The STAC endpoint is new and documented as still being optimised for performance and stability.

## What it means for SatClip
- Keep CDSE as the third STAC route in failover after Earth Search and Planetary Computer, and add an OData fallback for the case where the STAC endpoint is down or missing a collection.
- Use CDSE as the ground truth for "does a scene exist" when the other catalogues are empty: if CDSE has a Sentinel-1 acquisition that the mirrors lack, the evidence card should say the scene exists but is not yet processed, rather than "no data".
- Use OData Subscriptions (or periodic queries) to pre-warm the per-cell cache for flood-affected districts during monsoon, so a new pass is cached before officials ask.
- Store CDSE credentials as optional configuration; offline deployments must run without them and report the reduced source list in the receipt.
