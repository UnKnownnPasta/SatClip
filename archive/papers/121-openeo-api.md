---
id: 121
title: "The openEO API: Harmonising the Use of Earth Observation Cloud Services Using Virtual Data Cube Functionalities"
authors: "Matthias Schramm, Edzer Pebesma, Milutin Milenkovic, Luca Foresta, Jeroen Dries, Alexander Jacob, Wolfgang Wagner, Matthias Mohr, Markus Neteler, et al. (17 authors)"
year: 2021
venue: "Remote Sensing (MDPI), 13(6): 1125"
link: https://doi.org/10.3390/rs13061125
code: https://github.com/Open-EO (API spec, processes, Python/R/JS clients); project site https://openeo.org/
category: data-infrastructure
era: recent
tags: [openeo, data-cube, api, cloud-processing, interoperability, process-graph, copernicus-data-space, ogc]
verified: "2026-10-06 via https://api.crossref.org/works/10.3390/rs13061125 (title, all 17 authors, volume, issue, article number, abstract) and https://openeo.org/ (API 1.3.0 released Feb 2026, OGC Community Standard May 2026); full text at mdpi.com was blocked, so details of the two test cases beyond the abstract are not confirmed"
takeaway: "openEO is the standard way to push a SatClip instrument to a backend such as Copernicus Data Space as a portable process graph, so SatClip should keep its instruments expressible as data cube steps and record that graph in the receipt"
---

# The openEO API

## Problem
Each EO cloud platform (Earth Engine, Sentinel Hub, openEO backends at VITO, EODC, and others) exposes its own way to find, load and process data. Users have to rewrite workflows per platform, and results from different platforms are hard to compare.

## Approach
- A single REST API contract between lightweight clients (Python, R, JavaScript) and any compliant cloud backend, independent of how the backend stores data.
- The API presents data as a virtual EO raster data cube (dimensions such as x, y, time, bands) and workflows as process graphs built from a shared, versioned catalogue of processes (load_collection, filter, reduce, apply, and so on).
- The backend executes the graph close to the data; the client only describes the computation and fetches results.

## Data and benchmarks
The paper presents two test cases (per the abstract): running similar workflows across different openEO backends, and comparing a locally run workflow with its openEO cloud equivalent. Exact datasets and metrics in the test cases could not be read because the full text was not reachable.

## Key results
The abstract reports that comparable analyses can be run on different backends through one interface, while also exposing current limitations in how consistently backends implement the same processes. Since publication the ecosystem has matured: the openEO site lists API version 1.3.0 (Feb 2026) and OGC adoption as a Community Standard (May 2026), and Copernicus Data Space documents openEO as one of its main processing APIs.

## Limitations
- Same process graph does not guarantee identical numbers: backends differ in resampling, nodata handling and collection preprocessing, which the paper itself flags as a limitation.
- Batch jobs on hosted backends are queued and metered by credits, so latency is not interactive.
- Requires an account on the backend; not an offline option.

## What it means for SatClip
- Adopt the data cube vocabulary for instruments: describe each instrument (Kittler-Illingworth water, log-ratio change, NDVI difference) as load, filter by district geometry and date, apply, reduce. That makes an optional openEO execution path on Copernicus Data Space cheap to add as a fourth failover route when STAC plus COG reads fail.
- Put the process graph JSON (or the equivalent local step list) in the evidence card receipt; it is a ready-made, human-readable re-run recipe.
- Do not assume cross-backend numbers agree: if SatClip ever computes the same answer via openEO and via local COG reads, report the source in the card and treat disagreement as grounds to lower confidence or abstain.
