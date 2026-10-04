---
id: 073
title: "Object Detection in Optical Remote Sensing Images: A Survey and A New Benchmark"
authors: "Ke Li, Gang Wan, Gong Cheng, Liqiu Meng, Junwei Han"
year: 2020
venue: "ISPRS Journal of Photogrammetry and Remote Sensing 159: 296-307"
link: https://arxiv.org/abs/1909.00133
code: none
category: object-detection
era: recent
tags: [dataset, survey, optical-remote-sensing, benchmark, horizontal-boxes, google-earth, multi-resolution]
verified: "2026-10-04 via https://arxiv.org/abs/1909.00133 and full text PDF https://arxiv.org/pdf/1909.00133"
takeaway: "Survey plus the DIOR benchmark (23,463 images, 20 classes, 0.5 to 30 m); a reference for mixed-resolution detection, but SatClip should cite it only to justify scoping out object-level questions"
---

# Object Detection in Optical Remote Sensing Images: A Survey and A New Benchmark

## Problem
Existing optical remote sensing detection datasets were small, had few classes and little variation in imaging conditions, which saturated results and limited progress for deep learning methods.

## Approach
The paper reviews deep learning detectors in computer vision and Earth observation, then introduces DIOR, a benchmark collected from Google Earth by domain experts and annotated with horizontal bounding boxes in LabelMe. Classes were chosen to cover both urban and suburban infrastructure (adding dams and wind mills). Twelve representative detectors are benchmarked.

## Data and benchmarks
- 23,463 images of 800 by 800 pixels, spatial resolution 0.5 m to 30 m.
- 192,472 instances in 20 classes: airplane, airport, baseball field, basketball court, bridge, chimney, dam, expressway service area, expressway toll station, harbor, golf course, ground track field, overpass, ship, stadium, storage tank, tennis court, train station, vehicle, wind mill.
- Split: 11,725 trainval images and 11,738 test images.

## Key results
- RetinaNet with ResNet-101 and PANet with ResNet-101 tied for best at 66.1% mAP.
- Feature pyramid designs (FPN, PANet) clearly helped; deeper backbones generally did better.
- Large variation in object size and high inter-class similarity remained the main difficulties.

## Limitations
- Horizontal boxes only; no orientation.
- Google Earth mosaics, not calibrated Sentinel bands, and no SAR.
- Images are not tied to dates or scene IDs, so temporal questions cannot be posed.

## What it means for SatClip
- DIOR includes resolutions down to 30 m, but detectable objects at coarse resolution are large ones (airports, dams, stadiums); at most, SatClip could answer "is there a large reservoir or dam here", and even then a land-cover or water instrument is a better fit than a detector.
- Use the survey as a quick primer for judges who ask "why not object detection": cite the gap between 66% mAP on curated chips and the reliability we need for evidence cards.
- Copy DIOR's practice of an even trainval/test split with similar class distributions when building our Indian flood and crop validation sets.
- Keep detectors out of the CPU budget unless a concrete user question requires one.
