---
id: 114
title: "Change Vector Analysis: An Approach for Detecting Forest Changes with Landsat"
authors: "William A. Malila"
year: 1980
venue: "LARS Symposia (Symposium on Machine Processing of Remotely Sensed Data, Purdue University), paper 385; pages not confirmed"
link: https://docs.lib.purdue.edu/lars_symp/385
code: "none found"
category: historical
era: historical
tags: [change-detection, change-vector-analysis, landsat, forest, multi-temporal, bitemporal]
verified: "2026-10-06 via https://docs.lib.purdue.edu/lars_symp/385 (title, author, year, LARS Symposia series, abstract); page numbers and exact symposium title not confirmed on that page"
takeaway: "Origin of change vector analysis: describe change as magnitude plus direction in a transformed feature space, which lets SatClip say what kind of change happened, not just that something changed"
---

# Malila 1980, change vector analysis

## Problem
Forest managers needed a digital way to detect and characterize forest disturbance (harvesting, regrowth) from multi-date Landsat imagery, beyond simple per-band differencing.

## Approach
- Transform each date's Landsat channels with a linear transformation (Kauth-Thomas style brightness and greenness features, per the common reading of the paper).
- Compute a spectral change vector between the two dates for each unit.
- Use clustering to define spectrally uniform forest patches, then interpret the change vector's magnitude (how much) and direction (what kind).

## Data and benchmarks
A Northern Idaho forest test site with two-date Landsat data, used to map harvest and regrowth. No quantitative benchmark beyond the case study is described in the abstract.

## Key results
- Harvesting and regrowth were mapped successfully on the test site.
- Established the magnitude plus direction framing later formalized by Bovolo (CVA polar framework, already in this archive).

## Limitations
- Requires good radiometric consistency between dates; atmospheric and phenological differences create false change.
- Magnitude threshold and direction sectors were chosen by the analyst.
- Single-site demonstration, conference paper rather than journal article.

## What it means for SatClip
- Treat the NDVI difference and SAR log-ratio instruments as one-dimensional slices of a change vector; a combined vector (for example delta NDVI with delta VH dB) lets the card distinguish flooding of crops from harvest or ploughing.
- Report direction-based change class, not only magnitude, on the evidence card, and give the threshold method (for example K-I on magnitude) in the receipt.
- Insist on same-season, same-orbit pairs to avoid phenology or geometry masquerading as change; abstain when no suitable pair exists.
