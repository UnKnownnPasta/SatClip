---
id: 215
title: "Sentinel-1 InSAR Coherence to Detect Floodwater in Urban Areas: Houston and Hurricane Harvey as A Test Case"
authors: "Marco Chini, Ramona Pelich, Luca Pulvirenti, Nazzareno Pierdicca, Renaud Hostache, Patrick Matgen"
year: 2019
venue: "Remote Sensing (MDPI), 11(2), 107 (2019), DOI 10.3390/rs11020107"
link: https://doi.org/10.3390/rs11020107
code: "No code statement found; the bare-soil step uses the authors' earlier algorithm, hosted as the HASARD service on ESA G-POD (per the paper)"
category: change-detection
era: historical
tags: [insar-coherence, urban-flood, sentinel-1, slc, building-footprint, hurricane-harvey, houston, double-bounce, hierarchical-split-based]
verified: "2026-10-09 via curl to api.crossref.org (title, authors, journal, volume, issue, article number, abstract) and WebFetch of the open-access article at mdpi.com/2072-4292/11/2/107 (method, data, numbers, validation, limitations)"
takeaway: "First demonstration that Sentinel-1 coherence (pre-event pair vs co-event pair, inside SAR-derived building footprints) maps flooded urban areas missed by intensity, adding 11% to the Houston flood area at 20 m; confirms SatClip's urban blind spot is real and sizeable"
---

# Chini et al. 2019, Sentinel-1 coherence for urban floods

## Problem
Intensity-based flood maps miss floodwater between buildings, where double bounce keeps backscatter bright. With Sentinel-1's frequent revisit, the authors ask whether interferometric coherence can make urban flood mapping automatic and routine.

## Approach
- Step 1, buildings: from a year of Sentinel-1 images (12 images, August 2016 to August 2017), compute temporal average VV and VH intensity and temporal average VV coherence; mask layover with a DEM-based local incidence angle; find bright building pixels with a hierarchical split-based thresholding plus region growing; use high average coherence to reject bright vegetation; combine VV and VH maps with a logical OR.
- Step 2, urban flood: estimate coherence with a 9x9 window for a pre-event pair and for a co-event pair (one image during the flood). Inside building footprints, pixels where co-event coherence falls below pre-event coherence are labelled flooded.
- Step 3, open areas: flooded bare soil from the authors' existing change detection and region growing algorithm.
- Coherence is used only inside building footprints, because vegetation also decorrelates.

## Data and benchmarks
- Hurricane Harvey, Houston, flood image of 30 August 2017 in both Stripmap (5 m) and IW (20 m) modes, from SLC data.
- Qualitative validation against a GeoEye-1 image of 31 August 2017, about 12,000 crowdsourced flooded-house points from Tomnod/DigitalGlobe photointerpretation, the FEMA inundation model and some aerial photographs.

## Key results
- Urban flooding added 322,147 pixels (IW) and 1,687,048 pixels (Stripmap) to the flood maps, increasing the affected area by 11% (IW) and 4% (Stripmap).
- Mean co-event coherence over flooded urban areas was about 0.25, close to open water (about 0.1).
- No precision, recall or confusion matrix is reported; evaluation is visual and point-based.

## Limitations
- At 20 m, buildings mix with vegetation and other scatterers, causing under-detection.
- Traffic and debris also lower coherence and can create false alarms.
- Reference imagery was taken 24 to 36 hours after the SAR, and the FEMA model ignores wind damage, levee breaks and elevated structures.
- Requires SLC data and InSAR processing.

## What it means for SatClip
- Avoid: do not claim urban flood extent from sar_water_otsu; Houston showed a material extra flooded area hidden from intensity, and Indian towns (see entry 217 on Mumbai) are likely similar.
- Adopt now: compute a building mask (from a global built-up layer or, like this paper, from temporally bright and coherent pixels) and attach an "urban areas not assessed by SAR intensity" caveat with the built-up area count to every flood answer.
- Adopt in sar_logratio_change: inside built-up pixels, treat a co-event intensity increase as a weak flood cue for the caveat, not as a mapped flood.
- Future: an SLC coherence path (pre-event vs co-event pair, building-masked) is the proven upgrade; UrbanSARFloods (entry 190) gives labels to test it.
