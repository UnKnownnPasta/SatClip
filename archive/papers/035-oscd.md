---
id: 035
title: "Urban Change Detection for Multispectral Earth Observation Using Convolutional Neural Networks"
authors: "Rodrigo Caye Daudt, Bertrand Le Saux, Alexandre Boulch, Yann Gousseau"
year: 2018
venue: "IGARSS 2018 (IEEE International Geoscience and Remote Sensing Symposium, Valencia)"
link: https://arxiv.org/abs/1810.08468
code: https://rcdaudt.github.io/oscd/
category: change-detection
era: historical
tags: [sentinel-2, multispectral, urban-change, dataset, oscd, siamese, early-fusion, pixel-level-labels, benchmark]
verified: "2026-10-04 via https://arxiv.org/abs/1810.08468"
takeaway: "OSCD is the small but standard Sentinel-2 urban change benchmark (24 pairs, 13 bands, pixel labels); use it to calibrate optical change thresholds, not to train large models"
---

# Urban Change Detection for Multispectral Earth Observation Using Convolutional Neural Networks

## Problem
Most change detection work used very high resolution aerial or commercial imagery. Free, global, regularly revisited Sentinel-2 data had no public benchmark with pixel-level change labels, so methods for it could not be trained or compared.

## Approach
The paper releases the Onera Satellite Change Detection (OSCD) dataset and trains two fully convolutional patch-based networks from scratch: an Early Fusion network that stacks both dates as input channels, and a Siamese network that processes each date with shared weights before comparison. It also studies how many spectral bands to use (RGB, RGB plus NIR, the 10 bands at 10 and 20 m, and all 13 bands).

## Data and benchmarks
OSCD contains 24 Sentinel-2 image pairs acquired between 2015 and 2018 over sites in Brazil, the USA, Europe, the Middle East and Asia, with all 13 bands at their native 10, 20 or 60 m resolutions. Labels mark urban change (new buildings, new roads) at pixel level. The official split is 14 training and 10 test pairs; test labels were initially withheld but are now public. Distributed via IEEE DataPort. Author list confirmed via the OpenAlex record for the arXiv DOI.

## Key results
From the ar5iv version of the paper: Early Fusion generally beat Siamese. With 13 bands, Early Fusion reached about 88.2% overall pixel accuracy with about 84.7% accuracy on change pixels; with 3 bands it reached about 83.6% overall and 82.1% on change pixels. Adding bands beyond RGB helped overall, though not monotonically (the 4-band Siamese was weakest at about 75.2% overall). Note these are per-class pixel accuracies; F1 values were not confirmed from the source read.

## Limitations
Only 24 pairs, so deep models overfit and results vary a lot between sites. Change class is heavily outnumbered by no-change pixels. At 10 m, small buildings are hard to see, and the authors note annotators disagreed on change boundaries. Labels cover urban change only (no flood, burn, crop or forest change). Sentinel-2 archive only starts in mid-2015.

## What it means for SatClip
- Use OSCD as the calibration and sanity-check set for SatClip's optical change instruments (NDBI/NDVI differencing and CVA magnitude): fit thresholds and the confidence calibration curve on the 14 train pairs, report on the 10 test pairs.
- Its India-relevant lesson: 10 m change maps miss single small houses, so the evidence card should state a minimum detectable change size (for example several contiguous 10 m pixels) and abstain on questions about individual buildings.
- The band study supports keeping SWIR bands (B11, B12) in the built-up instrument rather than RGB alone.
- Do not train a CNN on OSCD alone and present its output as a measurement; the dataset is too small to support a calibrated claim.
