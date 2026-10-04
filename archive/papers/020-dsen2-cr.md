---
id: 020
title: "Cloud removal in Sentinel-2 imagery using a deep residual neural network and SAR-optical data fusion"
authors: "Andrea Meraner, Patrick Ebel, Xiao Xiang Zhu, Michael Schmitt"
year: 2020
venue: "ISPRS Journal of Photogrammetry and Remote Sensing, vol. 166, pp. 333-346, DOI 10.1016/j.isprsjprs.2020.05.013"
link: https://doi.org/10.1016/j.isprsjprs.2020.05.013
code: https://github.com/ameraner/dsen2-cr
category: sar-optical-fusion
era: recent
tags: [cloud-removal, dsen2-cr, residual-network, sentinel-1, sentinel-2, cloud-adaptive-loss, sen12ms-cr, keras]
verified: "2026-10-04 via https://github.com/ameraner/dsen2-cr, https://paperswithcode.com/paper/cloud-removal-in-sentinel-2-imagery-using-a and https://www.asg.ed.tum.de/sipeo/news/article/eo-data-science-paper-wins-isprs-best-paper-of-2020-award/"
takeaway: "Baseline for SAR-guided cloud filling; flag reconstructed areas and skip indices there; too heavy for per-query CPU use"
---

# Cloud removal in Sentinel-2 imagery using a deep residual neural network and SAR-optical data fusion

## Problem
Optical Sentinel-2 imagery is often unusable because of clouds, which matters most in exactly the seasons when disasters and crop monitoring need it. Many earlier methods were trained on simulated clouds or failed on thick cloud.

## Approach
DSen2-CR is a deep residual convolutional network that takes a cloudy multispectral Sentinel-2 image together with a co-registered Sentinel-1 SAR image and predicts a cloud-free optical image. The residual design means the network learns corrections to the input, leaving clear pixels largely untouched. A cloud-adaptive loss focuses reconstruction on cloudy areas while encouraging the network to preserve clear-sky pixels. SAR, which sees through cloud, supplies the land surface structure under thick cloud.

## Data and benchmarks
- Trained and tested on a global, all-season set of real cloudy and cloud-free Sentinel-2 images with matching Sentinel-1, released as SEN12MS-CR (https://mediatum.ub.tum.de/1554803); the repo also provides the train, validation and test split CSV.
- Implemented in Keras/TensorFlow with pretrained checkpoints.

## Key results
The abstract states that the model beats baselines and can reconstruct the surface under optically thick clouds. Paper-specific metric values could not be confirmed from the fetched pages; Papers with Code lists DSen2-CR scores on SEN12MS-CR, but those come from later comparison tables and are not quoted here. The paper won the ISPRS Journal best paper award for 2020 and the U.V. Helava Award for 2020-2021.

## Limitations
Under thick cloud the output is a SAR-guided estimate, so spectral detail (for example crop health indices) may be unreliable there. Single-date input. Model weights are TensorFlow 1/Keras era and somewhat heavy for CPU use at tile scale. No per-pixel uncertainty in the original work.

## What it means for SatClip
- DSen2-CR is the standard baseline for SAR-guided cloud filling; if SatClip adds cloud handling, it should be compared against this.
- Borrow the residual plus cloud-adaptive loss idea: only touch cloudy pixels and keep observed pixels intact, so citations stay honest.
- Do not compute NDVI or crop advice on reconstructed pixels; flag them and lower or withhold confidence.
- Running it per query on CPU is likely too slow; consider precomputing for frequently queried districts or skipping in favour of SAR-native answers.
- Check the pretrained checkpoint's licence and framework before integrating.
