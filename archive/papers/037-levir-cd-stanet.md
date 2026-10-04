---
id: 037
title: "A Spatial-Temporal Attention-Based Method and a New Dataset for Remote Sensing Image Change Detection"
authors: "Hao Chen, Zhenwei Shi"
year: 2020
venue: "Remote Sensing (MDPI), 12(10), 1662, DOI 10.3390/rs12101662"
link: https://www.mdpi.com/2072-4292/12/10/1662
code: https://justchenhao.github.io/LEVIR/
category: change-detection
era: recent
tags: [levir-cd, dataset, building-change, siamese, attention, stanet, very-high-resolution, optical-rgb, google-earth]
verified: "2026-10-04 via https://www.mdpi.com/2072-4292/12/10/1662"
takeaway: "LEVIR-CD (637 pairs, 0.5 m, Texas buildings) became the default CD benchmark; useful for language templates and model comparison but not for calibrating 10 m Sentinel instruments"
---

# A Spatial-Temporal Attention-Based Method and a New Dataset for Remote Sensing Image Change Detection

## Problem
Bitemporal change detection in very high resolution imagery is confused by illumination differences and small misregistration between dates, and the public datasets of the time were too small to train deep models well.

## Approach
STANet is a Siamese network with a spatial-temporal self-attention module that relates pixels across positions and across the two dates, so features become more robust to illumination and registration error. A basic attention module (BAM) and a pyramid attention module (PAM) that works at several scales are proposed. Changes are decided by metric learning: a distance between the two dates' feature maps is thresholded.

## Data and benchmarks
The paper introduces LEVIR-CD: 637 image pairs of 1024x1024 pixels at 0.5 m from Google Earth, covering 20 regions in Texas (Austin and nearby towns), with gaps of 5 to 14 years between 2002 and 2018 and more than 31,000 annotated building change instances (building growth and decline). Use is academic only and subject to Google Earth terms. The standard train/val/test split was not confirmed from the pages read.

## Key results
From the abstract: adding the attention module raised the baseline's F1 from 83.9 to 87.3 on LEVIR-CD at modest extra compute.

## Limitations
Single region (Texas suburbs), RGB only, only building changes, sub-metre commercial imagery with unclear licensing beyond academic use. Models trained on it do not transfer to Indian rural or peri-urban settings or to 10 m Sentinel-2 without retraining. No uncertainty output.

## What it means for SatClip
- Do not use LEVIR-CD to calibrate SatClip instruments: resolution (0.5 m vs 10 m), sensor and geography all mismatch, and the licence forbids commercial use.
- It is still the lingua franca for comparing learned CD models, so if SatClip ever reports a learned building-change component, cite LEVIR-CD F1 for comparability and then report separately on a Sentinel-2 set (OSCD, entry 035).
- STANet's emphasis on misregistration is a reminder to measure and log co-registration error between the two Sentinel scenes in the receipt.
- LEVIR-CD is the image source for LEVIR-CC (entry 040), the main change-captioning set.
