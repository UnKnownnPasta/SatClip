---
id: 088
title: "UnCRtainTS: Uncertainty Quantification for Cloud Removal in Optical Satellite Time Series"
authors: "Patrick Ebel, Vivien Sainte Fare Garnot, Michael Schmitt, Jan Dirk Wegner, Xiao Xiang Zhu"
year: 2023
venue: "CVPR 2023 Workshops (EarthVision), pp. 2086-2096"
link: https://openaccess.thecvf.com/content/CVPR2023W/EarthVision/html/Ebel_UnCRtainTS_Uncertainty_Quantification_for_Cloud_Removal_in_Optical_Satellite_Time_CVPRW_2023_paper.html
code: "not confirmed (a PatrickTUM/UnCRtainTS GitHub repository is commonly cited but could not be fetched)"
category: sar-optical-fusion
era: recent
tags: [cloud-removal, uncertainty, aleatoric, calibration, uce, negative-log-likelihood, l-tae, sen12ms-cr-ts, sentinel-1, sentinel-2, selective-prediction]
verified: "2026-10-05 via https://openaccess.thecvf.com/content/CVPR2023W/EarthVision/html/Ebel_UnCRtainTS_Uncertainty_Quantification_for_Cloud_Removal_in_Optical_Satellite_Time_CVPRW_2023_paper.html, https://arxiv.org/abs/2304.05464v1 and https://ar5iv.labs.arxiv.org/html/2304.05464"
takeaway: "Calibrated per-pixel variance lets you discard the most uncertain half of outputs and nearly halve error; the same rank-and-reject logic is SatClip's abstain rule"
---

# UnCRtainTS: Uncertainty Quantification for Cloud Removal in Optical Satellite Time Series

## Problem
Cloud removal networks output plausible pixels everywhere, including under thick cloud where they are guessing. Users and downstream models have no signal of which reconstructions to trust.

## Approach
- Architecture: a shared per-date encoder of MBConv blocks at full resolution, an L-TAE (lightweight temporal attention) aggregator that computes attention on downsampled 32 x 32 features and applies it at full resolution, and an MBConv decoder.
- Inputs: Sentinel-1 (2 channels) plus Sentinel-2 (13 channels) per date.
- Uncertainty: each pixel's output is a multivariate Normal with diagonal covariance; the network outputs a mean and a variance per band and is trained with negative log-likelihood (aleatoric uncertainty only).

## Data and benchmarks
SEN12MS-CR-TS ([[087-sen12ms-cr-ts]], T = 3 input dates in main experiments) and the single-date SEN12MS-CR ([[019-sen12ms-cr]]). Calibration is measured with uncertainty calibration error (UCE) at pixel and image level.

## Key results
- SEN12MS-CR-TS, T = 3: PSNR 27.84 dB and SSIM 0.866 versus 27.05 dB and 0.849 for a U-TAE baseline; SAM 10.16 versus 11.65 degrees; RMSE equal at 0.051 (as read on ar5iv).
- UCE 0.007 per pixel and 0.010 per image, reported as several times smaller than the mean reconstruction error.
- Predicted uncertainty rises monotonically with actual error; discarding the most uncertain 50% of reconstructions nearly halves the remaining error.
- Training with NLL costs a small amount of RMSE compared with plain L2.

## Limitations
- Aleatoric only; no epistemic uncertainty, so out-of-distribution scenes (for example, a novel flood) may still get confident wrong outputs.
- Diagonal covariance ignores band correlations.
- Only short sequences (T = 3) explored.

## What it means for SatClip
- The key idea transfers even if we never run cloud removal: have every instrument emit a spread, rank answers by it, and check on a validation set that error drops as we reject the most uncertain ones. That curve is the evidence that SatClip's abstain threshold is meaningful.
- Report a calibration metric (UCE or ECE) for SatClip's confidence, not just accuracy, and stratify by cloud fraction and season.
- If an optical reconstruction is ever shown, show its per-pixel variance map in the region mask and exclude high-variance pixels from area totals.
- Remember the aleatoric-only gap: add an explicit out-of-distribution check (for example, failed bimodality, from [[086-chini-hsba-thresholding]]) rather than trusting a model's own variance.
