---
id: 199
title: "TorchGeo: Deep Learning With Geospatial Data"
authors: "Adam J. Stewart, Caleb Robinson, Isaac A. Corley, Anthony Ortiz, Juan M. Lavista Ferres, Arindam Banerjee"
year: 2022
venue: "ACM SIGSPATIAL 2022 (30th International Conference on Advances in Geographic Information Systems, per arXiv v4 header); extended in ACM Transactions on Spatial Algorithms and Systems (2025), pp. 1-28, DOI 10.1145/3707459; arXiv:2111.08872"
link: https://arxiv.org/abs/2111.08872
code: "https://github.com/microsoft/torchgeo (open source, named in the paper)"
category: data-infrastructure
era: recent
tags: [torchgeo, pytorch, rasterio, gdal, cog, geosampler, reprojection, data-loading, multispectral-pretrained, sentinel-2, landsat]
verified: "2026-10-08 via curl to https://export.arxiv.org/api/query (title, authors, dates, abstract, GitHub URL), curl to https://api.crossref.org (ACM TSAS record, DOI 10.1145/3707459, 2025) and curl to https://arxiv.org/html/2111.08872v4 (SIGSPATIAL 2022 header, COG benchmark setup, caching discussion); WebFetch permission request timed out; sampling-rate figures are in plots and are not quoted"
takeaway: "The standard PyTorch library for loading georeferenced rasters by spatial query, with samplers that read windows from COGs and reproject on the fly; SatClip can reuse its GeoDataset and GridGeoSampler pattern for windowed S1/S2 reads, and should pre-align layers because on-the-fly warping is the main slowdown"
---

# Stewart et al. 2022, TorchGeo

## Problem
Satellite rasters come with many bands, different coordinate systems, resolutions and extents. Standard computer-vision loaders ignore this metadata, so joining imagery to labels or to another sensor requires hand-written GDAL steps that are slow and error-prone.

## Approach
- GeoDataset classes index files by spatial and temporal bounds (an R-tree) and return a sample for any bounding box and time, reprojecting and resampling on the fly through rasterio and GDAL.
- Datasets combine with intersection and union operators, for example Landsat imagery intersected with a label layer, or two sensors for fusion.
- GeoSamplers (random, random batch, grid) choose patch locations; a grid sampler suits whole-scene inference.
- Also ships benchmark-dataset loaders, multispectral transforms and the first pretrained weights using all Sentinel-2 bands.

## Data and benchmarks
- Loader benchmark: 114 Landsat 8 Collection 2 Level-2 scenes plus the 2019 Cropland Data Layer, stored as COGs with 512 block size (151 GB), in their native CRSs, on a 6-core CPU with local SSD.
- Model benchmarks on existing datasets (for example So2Sat) to test pretrained weights.

## Key results
- Grid sampling is much faster than random sampling, and preprocessing (aligning CRS and resolution ahead of time) plus caching gives large speedups, because GDAL's cache saves raw reads but warping must be repeated when CRSs differ.
- Pretrained multispectral weights improve transfer on downstream tasks with limited labels (abstract).

## Limitations
- Benchmarks used local SSD, not HTTP range reads from a remote STAC catalogue, so cloud latency is not measured.
- PyTorch-oriented; heavy dependency set for a lean CPU service.
- The paper does not cover Sentinel-1 calibration or terrain correction; it assumes analysis-ready inputs.

## What it means for SatClip
- Adopt: SatClip's window reader should follow the same pattern (query by bounds and date, read a COG window, return array plus CRS and transform) and log the exact scene and window used as provenance.
- Adopt: pre-align Sentinel-1 and Sentinel-2 windows to one district grid once and cache it in the Redis tile queue, rather than warping on every request.
- Optional: use TorchGeo's loaders and pretrained Sentinel-2 weights when training the segmentation head; keep the runtime reader minimal (rasterio plus STAC) for CPU deployment.
