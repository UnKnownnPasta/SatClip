---
id: 163
title: "Large Selective Kernel Network for Remote Sensing Object Detection"
authors: "Yuxuan Li, Qibin Hou, Zhaohui Zheng, Ming-Ming Cheng, Jian Yang, Xiang Li"
year: 2023
venue: "ICCV 2023 (IEEE/CVF International Conference on Computer Vision); extended as 'LSKNet: A Foundation Lightweight Backbone for Remote Sensing', IJCV 2024"
link: https://arxiv.org/abs/2303.09030
code: "https://github.com/zcablii/Large-Selective-Kernel-Network (named in the abstract; not fetched)"
category: object-detection
era: recent
tags: [oriented-detection, large-kernel, receptive-field, context, lightweight-backbone, dota, fair1m, hrsc2016]
verified: "2026-10-07 via curl to https://export.arxiv.org/api/query?id_list=2303.09030 (title, authors, abstract, results) and api.crossref.org (ICCV 2023 proceedings DOI 10.1109/iccv51070.2023.01540; IJCV 2024 extension DOI 10.1007/s11263-024-02247-9); extension content not read"
takeaway: "Shows that remote sensing objects need context from a wide, object-dependent window; useful as an RS-tuned backbone if detection is ever needed, but its results are on sub-metre imagery and do not transfer to Sentinel counts"
---

# Li et al. 2023, LSKNet (large selective kernels)

## Problem
Remote sensing detectors mostly improve how oriented boxes are represented and ignore a domain prior: small objects are easy to misread without long-range context, and how much context helps differs by object type.

## Approach
- A backbone that combines several large depth-wise kernels and learns, per location, how to weight them, so the effective receptive field adapts to the object.
- Presented as the first use of large and selective kernels for remote sensing detection.
- Plugged into standard oriented detectors.

## Data and benchmarks
- HRSC2016 (ships), DOTA-v1.0 and FAIR1M-v1.0 (oriented multi-class aerial detection).

## Key results
- HRSC2016: 98.46% mAP; DOTA-v1.0: 81.85% mAP; FAIR1M-v1.0: 47.87% mAP (as stated in the abstract).
- Second place in the 2022 Greater Bay Area International Algorithm Competition with a related method.

## Limitations
- All benchmarks are very high resolution optical imagery; nothing on SAR or 10 m data.
- The lower FAIR1M score shows fine-grained categories remain hard even for the best backbone.
- GPU-oriented results; CPU cost not reported in the abstract.

## What it means for SatClip
- **Cite for the context lesson**: even for SatClip's pixel instruments, decisions near ambiguous pixels (river edges, wet paddy) benefit from a wider window; this supports a neighbourhood or morphological clean-up step after Otsu thresholding, recorded in the receipt.
- **Avoid** as a default model: the CPU budget and 10 m data make it a poor fit. Consider it only if a sub-metre imagery source is ever added for very local questions.
- Use its FAIR1M figure in the scope argument: fine-grained object recognition is hard even at sub-metre scale, so SatClip keeps object questions out of scope at 10 m.
