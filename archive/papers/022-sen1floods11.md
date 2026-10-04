---
id: 022
title: "Sen1Floods11: A Georeferenced Dataset to Train and Test Deep Learning Flood Algorithms for Sentinel-1"
authors: "Derrick Bonafilia, Beth Tellman, Tyler Anderson, Erica Issenberg"
year: 2020
venue: "CVPR Workshops 2020 (pp. 210-211)"
link: https://openaccess.thecvf.com/content_CVPRW_2020/html/w11/Bonafilia_Sen1Floods11_A_Georeferenced_Dataset_to_Train_and_Test_Deep_Learning_CVPRW_2020_paper.html
code: https://github.com/cloudtostreet/Sen1Floods11
category: sar-optical-fusion
era: recent
tags: [sentinel-1, sentinel-2, flood-mapping, segmentation, weak-labels, dataset, south-asia]
verified: "2026-10-04 via https://openaccess.thecvf.com/content_CVPRW_2020/papers/w11/Bonafilia_Sen1Floods11_A_Georeferenced_Dataset_to_Train_and_Test_Deep_Learning_CVPRW_2020_paper.pdf"
takeaway: "Standard Sentinel-1 flood baseline (11 events, none in India); keep an Otsu VH threshold as a sanity check and build an Indian held-out test"
---

# Sen1Floods11: A Georeferenced Dataset to Train and Test Deep Learning Flood Algorithms for Sentinel-1

## Problem
Radar sees floods through cloud, but deep learning flood mappers lacked a public, georeferenced, globally varied training and test set, and it was unclear whether cheap automatic labels could replace costly hand labels.

## Approach
The authors build paired Sentinel-1 and Sentinel-2 chips at 10 m and train a fully convolutional network (ResNet50 backbone) on four label sources: hand labels, Sentinel-1 derived weak labels, Sentinel-2 derived weak labels and permanent water from Landsat. They compare against an Otsu threshold on VH backscatter.

## Data and benchmarks
4,831 chips of 512 x 512 pixels covering about 120,406 km2 across 11 flood events on six continents: 446 hand labeled and 4,385 weakly labeled. Events are in Bangladesh, Pakistan, Nigeria, South Sudan, Cambodia, Bolivia, Brazil, Colombia, Paraguay, Spain and Uruguay. India is not included, though Bangladesh and Pakistan are neighbouring monsoon plains. Bolivia is held out entirely to test generalisation. Data is about 14 GB on a public Google Cloud bucket.

## Key results
Mean IoU for water on the hand-labeled test set (10 events): Sentinel-2 weak labels scored best for flood water (0.339) and all water (0.408), while Otsu VH thresholding scored best on permanent water (0.457). On the unseen Bolivia event, Sentinel-1 weak labels led on all water (0.387), with Otsu very close (0.386). Hand labels did not beat weak labels in either table.

## Limitations
Only 11 events, no urban floods in validation, minimal hyperparameter tuning, and the authors frame results as preliminary. Absolute IoU values are modest, and simple thresholding remains competitive.

## What it means for SatClip
- Use Sen1Floods11 as a standard SAR flood baseline, but build our own small hand-labeled Indian test set (e.g. Assam, Bihar, Kerala) since India is absent.
- Keep an Otsu VH threshold as a transparent fallback and sanity check; if our model disagrees strongly, lower confidence or abstain.
- Weak labels from Sentinel-2 can scale training cheaply; adopt that for India where cloud-free optical pairs exist.
- Report IoU on a geographically held-out event, as they did with Bolivia, to avoid overstating accuracy to officials.
- Ship flood masks with scene ID and date per chip, mirroring their georeferenced design.
