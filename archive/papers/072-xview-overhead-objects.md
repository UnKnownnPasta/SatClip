---
id: 072
title: "xView: Objects in Context in Overhead Imagery"
authors: "Darius Lam, Richard Kuzma, Kevin McGee, Samuel Dooley, Michael Laielli, Matthew Klaric, Yaroslav Bulatov, Brendan McCord"
year: 2018
venue: "arXiv preprint (arXiv:1802.07856, February 2018)"
link: https://arxiv.org/abs/1802.07856
code: https://github.com/DIUx-xView/xView1_baseline
category: object-detection
era: historical
tags: [dataset, worldview-3, overhead-imagery, fine-grained, small-objects, axis-aligned-boxes, humanitarian]
verified: "2026-10-04 via https://export.arxiv.org/api/query?id_list=1802.07856 and https://ar5iv.labs.arxiv.org/html/1802.07856"
takeaway: "Over 1 million objects in 60 classes from 0.3 m WorldView-3 imagery, with a weak SSD baseline; shows how hard fine-grained small-object detection is even at 0.3 m, reinforcing that SatClip should not count objects in Sentinel data"
---

# xView: Objects in Context in Overhead Imagery

## Problem
Overhead object detection lacked a large, diverse, fine-grained public dataset, which limited progress on small objects, rare classes and applications such as disaster response.

## Approach
Experts annotated WorldView-3 imagery with axis-aligned bounding boxes using QGIS and an in-house plugin. A three-stage quality-control process (peer review, supervisor checks for duplicates and invalid geometry, expert validation against gold-standard samples) gated each batch on precision and recall thresholds. The paper trains a Single Shot MultiBox Detector (SSD) baseline on several preprocessing variants.

## Data and benchmarks
- Over 1 million objects, 60 classes, over 1,400 square kilometres.
- WorldView-3 at 0.3 m ground sample distance, provided as RGB and 8-band multispectral.
- Object sizes range from about 3 m to over 3 km.
- Used for the DIUx xView 2018 Detection Challenge.

## Key results
- Best baseline SSD reached about 0.26 mAP overall, with high scores for large distinct classes (passenger or cargo plane about 0.67) and near-zero for some frequent fine-grained classes (pickup truck under 1%).
- Small, clustered and fine-grained objects were the main failure modes; large objects cut at chip edges also hurt.

## Limitations
- Axis-aligned boxes fit rotated objects poorly (compare DOTA, entry 071).
- Commercial very high resolution imagery; access and licensing differ from open Sentinel data.
- The paper is an arXiv preprint; we found no peer-reviewed venue for it.

## What it means for SatClip
- Reinforces scoping: even at 0.3 m a strong detector struggled on vehicles, so at 10 m SatClip must refuse counts of vehicles, boats or buildings and say this plainly in the abstain message.
- Copy the QC recipe for our own validation sets: peer review, geometry checks and a gold-standard sample with explicit pass thresholds before a flood mask enters the benchmark.
- Note the humanitarian motivation: xView-style data suits building damage work (see xBD, entry 039), which SatClip can point users to rather than attempt itself.
- If we ever display detection outputs, report per-class performance, not a single mAP, since averages hide classes that fail completely.
