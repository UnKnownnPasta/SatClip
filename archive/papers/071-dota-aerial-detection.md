---
id: 071
title: "DOTA: A Large-scale Dataset for Object Detection in Aerial Images"
authors: "Gui-Song Xia, Xiang Bai, Jian Ding, Zhen Zhu, Serge Belongie, Jiebo Luo, Mihai Datcu, Marcello Pelillo, Liangpei Zhang"
year: 2018
venue: "CVPR 2018"
link: https://arxiv.org/abs/1711.10398
code: https://captain-whu.github.io/DOTA/
category: object-detection
era: historical
tags: [dataset, aerial-imagery, oriented-bounding-box, benchmark, very-high-resolution, small-objects]
verified: "2026-10-04 via https://arxiv.org/abs/1711.10398, https://ar5iv.labs.arxiv.org/html/1711.10398 and https://captain-whu.github.io/DOTA/"
takeaway: "The standard oriented-box benchmark for aerial object detection (15 classes, very high resolution); useful context but its objects are mostly below Sentinel-2's 10 m pixel, so SatClip should not promise object counts"
---

# DOTA: A Large-scale Dataset for Object Detection in Aerial Images

## Problem
Object detection in aerial imagery lagged behind natural images because objects vary hugely in scale, orientation and shape, and existing aerial datasets were small and biased.

## Approach
A large dataset of aerial images from several sensors and platforms (including Google Earth), annotated by experts with arbitrary quadrilaterals (8 degrees of freedom), giving oriented bounding boxes (OBB) as well as derived horizontal boxes (HBB). The authors define OBB and HBB detection tasks and benchmark standard detectors, including a Faster R-CNN modified for oriented boxes.

## Data and benchmarks
- 2,806 images, roughly 800 by 800 to 4000 by 4000 pixels.
- 188,282 instances in 15 categories: plane, ship, storage tank, baseball diamond, tennis court, basketball court, ground track field, harbor, bridge, large vehicle, small vehicle, helicopter, roundabout, soccer ball field, swimming pool.
- Later versions (DOTA v1.5, v2.0) are listed on the project page; we did not verify their statistics here.

## Key results
- Best baseline in the paper: about 54.1% mAP for OBB and about 60.5% mAP for HBB, both from Faster R-CNN variants.
- Dense small objects and very large, arbitrarily rotated objects remained the hardest cases.

## Limitations
- Very high resolution optical imagery (sub-metre to a few metres); not Sentinel-2 and not SAR.
- Mostly urban and infrastructure classes; nothing on water, crops or land cover.
- Images are chips without consistent georeferencing for most sources, so results do not transfer directly to map products.

## What it means for SatClip
- Avoid object-count questions ("how many boats", "how many vehicles") at Sentinel-2 10 m resolution: most DOTA classes are smaller than a pixel there. SatClip should abstain and say why.
- Use DOTA's category list as a guide for what users might ask and what to explicitly scope out in the "what SatClip cannot do" text.
- If a future version adds high-resolution sources, oriented boxes (not horizontal) are the right output for ships and harbours, and DOTA is the benchmark to report on.
- Borrow the annotation lesson: expert-checked polygons and stated class definitions make a benchmark trustworthy, which we should copy for our Indian flood validation masks.
