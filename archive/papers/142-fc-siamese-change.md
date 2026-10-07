---
id: 142
title: "Fully Convolutional Siamese Networks for Change Detection"
authors: "Rodrigo Caye Daudt, Bertrand Le Saux, Alexandre Boulch"
year: 2018
venue: "2018 25th IEEE International Conference on Image Processing (ICIP), Athens, pp. 4063-4067"
link: https://arxiv.org/abs/1810.08462
code: "https://github.com/rcdaudt/fully_convolutional_change_detection (commonly cited official repo; not opened, GitHub access blocked in this session)"
category: change-detection
era: historical
tags: [siamese, fully-convolutional, u-net, oscd, sentinel-2, air-change, baseline]
verified: "2026-10-07 via arXiv export API for 1810.08462 (title, authors, ICIP 2018 comment), Crossref 10.1109/ICIP.2018.8451652 (venue, pages 4063-4067), and the arXiv PDF for Table 1 numbers"
takeaway: "The standard small learned baseline for Sentinel-2 change (FC-EF, FC-Siam-conc, FC-Siam-diff); its modest OSCD F1 near 58 percent shows learned 10 m change maps are far from reliable enough to be SatClip's reported number"
---

# Daudt, Le Saux and Boulch 2018, FC-Siamese change detection

## Problem
Earlier deep change detectors classified patches one at a time, which was slow and imprecise at boundaries. The authors wanted end-to-end dense change maps from a co-registered image pair, trainable from scratch on small datasets.

## Approach
- FC-EF: a compact U-Net that takes the two images stacked as one input (early fusion).
- FC-Siam-conc: two weight-shared encoders, with skip connections from both dates concatenated in the decoder.
- FC-Siam-diff: the same, but skip connections carry the absolute difference of the two encoders' features, steering the net toward comparison.
- Class weights inversely proportional to frequency and simple flip and rotation augmentation; no post-processing.

## Data and benchmarks
- OSCD (Onera Satellite Change Detection, Sentinel-2, already in this archive as entry 035): 14 training and 10 test image pairs, tested with 3 RGB bands and with all 13 bands.
- Air Change dataset (RGB aerial), Szada/1 and Tiszadob/3 test cases.

## Key results
- OSCD, 13 bands, change-class F1: FC-Siam-diff 57.92, FC-EF 56.91, FC-Siam-conc 51.36, against 42.48 for the earlier patch-based early fusion.
- OSCD, 3 bands: FC-EF 48.89 and FC-Siam-diff 48.86, so the extra Sentinel-2 bands help noticeably.
- Inference under 0.1 s per image, reported as over 500 times faster than a compared method.
- Results on Air Change were mixed: FC-EF led on Tiszadob/3 while other published methods led on Szada/1.

## Limitations
- Very small training set (14 pairs), so variance across splits is likely high and is not reported.
- Precision on change stays below about 65 percent on OSCD; outputs are hard labels with no calibration.
- Urban change only; nothing on floods, crops or SAR (the authors list SAR as future work).

## What it means for SatClip
- These three architectures are the cheapest credible learned baseline to compare against SatClip's NDVI-difference and log-ratio instruments on Indian scenes.
- An F1 under 60 percent on the main Sentinel-2 change benchmark is a concrete reason why SatClip reports measured index differences with thresholds, not a network's mask, as its headline number.
- If ever used, its softmax scores must be temperature-calibrated before contributing to any confidence shown to an official.
