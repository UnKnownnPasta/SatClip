---
id: 210
title: "Height Above the Nearest Drainage – a hydrologically relevant new terrain model"
authors: "A. D. Nobre, L. A. Cuartas, M. Hodnett, C. D. Rennó, G. Rodrigues, A. Silveira, M. Waterloo, S. Saleska"
year: 2011
venue: "Journal of Hydrology, 404(1-2), 13-29 (2011), DOI 10.1016/j.jhydrol.2011.03.051"
link: https://doi.org/10.1016/j.jhydrol.2011.03.051
code: "None released with the paper; HAND is now implemented in many open tools and shipped as a global layer with MERIT Hydro (not verified here)"
category: sar-optical-fusion
era: historical
tags: [hand, height-above-nearest-drainage, terrain-mask, dem, flood-prone-areas, exclusion-mask, amazonia, false-water]
verified: "2026-10-09 via curl to api.crossref.org (title, authors, journal, volume, pages, DOI) and api.semanticscholar.org (authors, year; abstract elided by publisher); WebFetch of experts.arizona.edu record (abstract content); WebFetch of the GFM Product Definition wiki at extwiki.eodc.eu (how GFM applies a HAND threshold). Full text not read (publisher page blocked); DEM name, class thresholds and correlation coefficients not confirmed"
takeaway: "HAND (height of each pixel above its nearest drainage channel) is the standard terrain prior for SAR flood maps; operational systems such as Copernicus GFM mask pixels with HAND of 10 m or more, which SatClip should copy to kill terrain-shadow and hillside false water"
---

# Nobre et al. 2011, HAND terrain model

## Problem
Raw elevation is a poor guide to where water collects: a pixel at 300 m can be a valley floor in one basin and a ridge in another. Hydrologists needed a terrain descriptor that says how far, vertically, a location sits above the channel it drains into, so that soil wetness and flood proneness can be compared across catchments.

## Approach
- Derive a drainage network and flow directions from a DEM, then for every cell follow the flow path to the nearest drainage cell and record the elevation difference. That difference is HAND.
- HAND normalises topography to local drainage, which the authors interpret as a gravitational draining potential.
- Group HAND values into landscape classes (for example waterlogged lowland versus well drained upland) by vertical distance to drainage.

## Data and benchmarks
- Calibration and validation over roughly 18,000 km2 of the lower Rio Negro catchment in central Amazonia, with preliminary tests in ungauged catchments of different geology and soils.
- Uses remotely sensed topography only as input; the abstract does not name the DEM (SRTM is widely assumed but was not confirmed here).

## Key results
- The abstract reports a high correlation between HAND and water-table depth; the coefficient was not visible in the material read.
- HAND classes were reported as hydrologically consistent across the study catchment and neighbouring ungauged basins.
- Downstream use (not from this paper): the Copernicus GFM product documentation states that a HAND threshold of 10 m or more defines non-flood-prone areas in its exclusion mask, chosen from tests on more than 400 Sentinel-1 and TerraSAR-X scenes (citing Twele et al. 2016 and Chow et al. 2016). It also notes that the Copernicus DEM is not hydrologically conditioned and so is not used directly for HAND.

## Limitations
- Developed for soil-water classes in Amazonia, not for SAR flood masks; the flood use is a later adaptation.
- Quality depends on the DEM and on drainage-network extraction (stream initiation threshold); in flat deltas and paddy landscapes, small DEM errors give misleading HAND.
- Full text was not read; class thresholds and validation statistics are not reproduced here.

## What it means for SatClip
- Adopt in sar_water_otsu: add a HAND mask from a hydrologically conditioned source (MERIT Hydro HAND or a HAND layer derived from a conditioned DEM), and set water to "not assessable" where HAND is 10 m or more, matching GFM. Shrink the mask by one pixel as GFM does.
- Adopt: also compute the Otsu histogram only over low-HAND pixels, so hillslope shadows do not drag the threshold.
- Avoid: do not compute HAND directly from the Copernicus DEM on the Planetary Computer without hydrological conditioning; GFM explicitly avoids this.
- Avoid: do not apply the 10 m value blindly in flat Bihar or Assam floodplains, where nearly everything is below 10 m and HAND gives little separation; validate the threshold on Indian scenes, and pair it with a slope mask for the hills of Kerala and the Northeast.
