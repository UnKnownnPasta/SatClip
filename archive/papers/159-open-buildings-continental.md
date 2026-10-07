---
id: 159
title: "Continental-Scale Building Detection from High Resolution Satellite Imagery"
authors: "Wojciech Sirko, Sergii Kashubin, Marvin Ritter, Abigail Annkah, Yasser Salah Eddine Bouchareb, Yann Dauphin, Daniel Keysers, Maxim Neumann, Moustapha Cisse, John Quinn"
year: 2021
venue: "arXiv preprint (arXiv:2107.12283, July 2021); no peer-reviewed venue listed on arXiv"
link: https://arxiv.org/abs/2107.12283
code: "No code release named in the abstract; the resulting Open Buildings dataset is public (dataset site not fetched)"
category: object-detection
era: recent
tags: [building-footprints, instance-segmentation, u-net, self-training, mixup, open-buildings, africa, 50cm-imagery, exposure-layer]
verified: "2026-10-07 via curl to https://export.arxiv.org/api/query?id_list=2107.12283 (title, authors, date, abstract); no journal_ref on arXiv; India coverage of later Open Buildings releases is from general knowledge and was not checked against a source"
takeaway: "Do not detect buildings from Sentinel; ingest a precomputed open footprint layer (Open Buildings or similar) as a versioned exposure layer so flood cards can say how many mapped buildings fall inside the water mask"
---

# Sirko et al. 2021, continental-scale building detection (Open Buildings)

## Problem
Building locations and footprints are basic inputs for planning, disaster response and population estimates, but in many developing regions no reliable building map exists. The authors want one model pipeline that works across an entire continent, rural and urban.

## Approach
- Starts from a U-Net for instance segmentation of buildings on 50 cm satellite imagery.
- Systematically tests changes to architecture, loss, regularisation, pre-training, self-training and post-processing.
- Two additions they single out as new for this task: mixup augmentation and self-training with a soft KL loss on unlabelled imagery.

## Data and benchmarks
- About 100k satellite images across Africa with 1.75M manually labelled building instances.
- Extra datasets for pre-training and self-training (details not re-checked here).

## Key results
- Mixup adds about 0.12 mAP and soft-KL self-training about 0.06 mAP (as stated in the abstract).
- The pipeline was used to produce the Open Buildings dataset: 516M detected footprints across Africa.
- Later releases extended the dataset beyond Africa, including South Asia; that extension is not part of this paper and was not verified here.

## Limitations
- Needs 50 cm commercial imagery, far finer than Sentinel-2's 10 m; the model is not transferable to SatClip's data.
- Footprints are a snapshot from a given imagery date, so they can be stale after rapid growth or destruction.
- Per-region accuracy varies with context; the abstract reports aggregate gains, not per-country error.

## What it means for SatClip
- **Adopt as a data layer, not a model.** Load a precomputed footprint layer for the district, record its version and imagery date on the card, and intersect it with the SAR water mask to report "N mapped buildings inside the flooded area".
- Mark that count as *inferred from an external layer*, separate from the measured water extent, and show the layer's own confidence threshold if one is published.
- **Avoid** promising building detection from Sentinel-1 or Sentinel-2 imagery; this paper shows the task needs sub-metre data and a large labelled set.
