---
id: 015
title: "FloodNet: A High Resolution Aerial Imagery Dataset for Post Flood Scene Understanding"
authors: "Maryam Rahnemoonfar, Tashnim Chowdhury, Argho Sarkar, Debvrat Varshney, Masoud Yari, Robin Roberson Murphy"
year: 2021
venue: "IEEE Access, vol. 9, pp. 89644-89654, DOI 10.1109/ACCESS.2021.3090981"
link: https://arxiv.org/abs/2012.02951
code: https://github.com/BinaLab/FloodNet-Supervised_v1.0
category: rs-benchmark
era: recent
tags: [flood, disaster, vqa, segmentation, uav, hurricane-harvey, counting]
verified: "2026-10-04 via https://arxiv.org/abs/2012.02951 and https://doaj.org/article/de2388e23953411c95be84c370c38d76"
takeaway: "Borrow the flood question taxonomy rescaled to 10 m Sentinel, and guard against flood versus permanent water confusion with a reference layer"
---

# FloodNet: A High Resolution Aerial Imagery Dataset for Post Flood Scene Understanding

## Problem
Disaster datasets were mostly satellite based, with coarse resolution and long revisit times, which makes fine post-flood assessment (which roads and buildings are flooded) hard.

## Approach
The authors collect UAV imagery after Hurricane Harvey and annotate it for three tasks: image classification (flooded or not), pixel-wise semantic segmentation, and VQA. They benchmark standard deep learning baselines for each.

## Data and benchmarks
- About 3,200 images at 4000x3000 px from DJI Mavic Pro drones over Fort Bend County, Texas, captured about 200 ft above ground (paper, ar5iv render).
- Classes include flooded and non-flooded building, flooded and non-flooded road, water, tree, vehicle, pool and grass.
- About 11,000 question/image pairs covering simple counting, complex counting and condition recognition (flooded or not).
- The public supervised repo lists 2,343 images under a permissive Community Data License Agreement; the gap from 3,200 was not reconciled.

## Key results
As read from the paper: ResNet50 classification about 93.7% test accuracy, PSPNet segmentation about 79.7% mIoU, and an MFB co-attention VQA model about 73% overall accuracy.

## Limitations
Single event, single US region, drone imagery only, so no direct transfer to Sentinel scale. Small objects (vehicles, pools) are hard. Separating flood water from natural water needs context the image may not contain. Nadir views hide some damage.

## What it means for SatClip
- Adopt its question taxonomy (counting, condition recognition) for our flood questions for district disaster officials, but rescale to what 10 m pixels can answer (area flooded, roads affected) rather than counting cars.
- The flood water versus permanent water confusion is our main risk; use a pre-event reference scene or JRC permanent water layer before declaring flooding.
- Sentinel-1 SAR sees through monsoon cloud where drones and optical fail; this is our advantage to stress.
- Use FloodNet only for qualitative or transfer tests, never as evidence of Sentinel performance.
- Return "condition" answers with a mask and confidence, since segmentation at about 80% mIoU still leaves room for error.
