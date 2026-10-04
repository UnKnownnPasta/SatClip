---
id: 026
title: "On Calibration of Modern Neural Networks"
authors: "Chuan Guo, Geoff Pleiss, Yu Sun, Kilian Q. Weinberger"
year: 2017
venue: "ICML 2017"
link: https://arxiv.org/abs/1706.04599
code: none
category: trust-calibration
era: historical
tags: [calibration, temperature-scaling, ece, reliability-diagram, platt-scaling, post-hoc]
verified: "2026-10-04 via https://arxiv.org/abs/1706.04599"
takeaway: "Modern deep nets are overconfident; fit one temperature on held-out data to calibrate any score, report ECE and a reliability diagram, accuracy is unchanged"
---

# On Calibration of Modern Neural Networks

## Problem
A classifier's confidence should match how often it is right: of all predictions made at 80% confidence, about 80% should be correct. The authors observe that modern deep networks, though more accurate than older ones, are noticeably worse calibrated and tend to be overconfident.

## Approach
They study which training choices drive miscalibration (depth, width, weight decay, batch normalization) and then compare post-hoc fixes fitted on a held-out validation set: histogram binning, isotonic regression, Bayesian Binning into Quantiles, Platt scaling, matrix and vector scaling, and temperature scaling. Temperature scaling divides all logits by one learned scalar T before the softmax. They measure calibration with Expected Calibration Error (ECE: the bin-weighted gap between accuracy and mean confidence) and visualise it with reliability diagrams.

## Data and benchmarks
Image classification (CIFAR-10, CIFAR-100, SVHN, ImageNet, among others) and document classification datasets, across several modern architectures such as ResNets, Wide ResNets and DenseNets.

## Key results
Temperature scaling, the simplest method with a single parameter, was found to be surprisingly effective on most datasets, often matching or beating more complex calibrators. Because dividing by T does not change which class has the highest score, accuracy is unchanged. The paper reports per-model ECE tables (for example ResNet-110 on CIFAR-100 improves substantially), but exact figures were not confirmed from the fetched page, so none are quoted here.

## Limitations
Calibration is only guaranteed in-distribution: a temperature fitted on one data distribution can drift under domain shift. A single global T cannot fix class-dependent or input-dependent miscalibration. ECE depends on binning choices and can hide errors in sparse confidence regions. The work covers classification, not regression or segmentation.

## What it means for SatClip
- Adopt temperature scaling (or Platt scaling for binary instrument outputs such as "flooded or not") as the default calibrator for every score that feeds the evidence card's confidence, including RemoteCLIP similarities and any learned segmenter.
- Fit the temperature on a held-out Indian validation set, separately per instrument and ideally per season (monsoon versus dry), since a single global value will not survive the Europe-to-India and dry-to-wet shifts.
- Publish ECE and a reliability diagram per instrument in the evaluation report; a "calibrated confidence" claim without them is not credible to judges.
- Note that SAR thresholding and spectral indices produce no probability at all: SatClip needs a mapping (for example logistic regression on margin-from-threshold plus scene quality features) before this method applies.
