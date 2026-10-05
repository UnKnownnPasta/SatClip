---
id: 096
title: "AlphaEarth Foundations: An embedding field model for accurate and efficient global mapping from sparse label data"
authors: "Christopher F. Brown, Michal R. Kazmierski, Valerie J. Pasquarella, William J. Rucklidge, Masha Samsikova, Chenhui Zhang, Evan Shelhamer, Estefania Lahera, Olivia Wiles, Simon Ilyushchenko, Noel Gorelick, Lihui Lydia Zhang, Sophia Alj, Emily Schechter, Sean Askay, Oliver Guinan, Rebecca Moore, Alexis Boukouvalas, Pushmeet Kohli (Google DeepMind, Google)"
year: 2025
venue: "arXiv preprint (arXiv:2507.22291, v1 29 July 2025, v2 8 September 2025)"
link: https://arxiv.org/abs/2507.22291
code: none found (model weights not found; embeddings released as the Earth Engine dataset "Satellite Embedding v1 (Annual)")
category: upcoming
era: upcoming
tags: [big-tech, embedding-field, foundation-model, sentinel-1, sentinel-2, landsat, earth-engine, sparse-labels]
verified: "2026-10-05 via https://arxiv.org/abs/2507.22291 and https://arxiv.org/html/2507.22291v1; Earth Engine catalog page could not be fetched, so dataset ID and license wording not checked directly"
takeaway: "Precomputed annual 10 m embeddings for every land pixel make cheap land-cover and change features available to anyone, a strong optional baseline for SatClip, but annual, opaque and not usable for a specific flood date"
---

# AlphaEarth Foundations: An embedding field model for accurate and efficient global mapping from sparse label data

## Problem
Mapping land cover, crops or change usually needs many labels, and labels are expensive to collect in the field. Classic featurizations (raw bands, composites, harmonics) or other learned models need heavy per-task work and still underperform when labels are very sparse.

## Approach
A roughly 480M-parameter "Space Time Precision" encoder ingests many gridded sources over time and produces a continuous embedding field: a compact vector per 10 m pixel per year. Inputs include Sentinel-2, Landsat 8 and 9, Sentinel-1 C-band SAR, PALSAR-2 L-band SAR, ERA5-Land climate, GLO-30 elevation, GRACE gravity, GEDI lidar, plus text (Wikipedia) and some land-cover labels. Embeddings are 64-dimensional and quantized to 8 bits for storage. Implicit decoders let the model reconstruct sources at arbitrary times, which is how it is trained.

## Data and benchmarks
- About 3 billion observations sampled over about 1.1% of Earth's land surface, 2017 to 2024, with ecoregion-stratified site selection.
- 15 evaluations on 11 datasets: land use and land cover, crop type, change detection, and biophysical variables (evapotranspiration, emissivity), across the US, Europe, sub-Saharan Africa and global sets.

## Key results
- As reported, about 23.9% average error reduction against a suite of other featurization approaches, without re-training the embedding model.
- Particularly strong in 10-shot and 1-shot settings.
- Global annual embedding layers for 2017 to 2024 released in Google Earth Engine.

## Limitations
- One embedding per pixel per year: it cannot isolate a single monsoon flood event or a specific pair of acquisition dates.
- Embedding dimensions have no physical meaning, so a district official cannot inspect why a pixel was labelled flooded or stressed.
- Authors note it can need more training observations than some baselines on certain tasks, and gains vary by application.
- Access is through Earth Engine; downstream use depends on Google's terms and account access.

## What it means for SatClip
- Threat level: medium. It is not a question-answering system, but it makes high-quality land features nearly free, and Google's Earth AI agent (entry 095) can sit on top of it.
- Adopt (optional): use the annual embeddings as an offline baseline or a sanity check for our CLIP zero-shot land-cover instrument in pilot districts, and as a prior for "is this pixel normally water or cropland".
- Avoid: making any SatClip number depend on these embeddings. They are annual and opaque, which breaks our rule that every number traces to dated scenes and a transparent method.
- Beat: event-specific answers. SatClip measures this week's flood from this week's Sentinel-1 pass with scene IDs; AlphaEarth tells you what a pixel looked like across a year.
- Keep the instrument-first story: AlphaEarth is a representation, SatClip is an auditable measurement with a receipt and an abstain option.
