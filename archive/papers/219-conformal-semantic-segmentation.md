---
id: 219
title: "Conformal Semantic Image Segmentation: Post-hoc Quantification of Predictive Uncertainty"
authors: "Luca Mossina, Joseba Dalmau, Léo Andéol"
year: 2024
venue: "2024 IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW), pp. 3574-3584, DOI 10.1109/CVPRW63382.2024.00361; arXiv:2405.05145 (April 2024)"
link: https://arxiv.org/abs/2405.05145
code: "https://github.com/deel-ai-papers/conformal-segmentation (named in the paper; repository not opened from this session)"
category: trust-calibration
era: recent
tags: [conformal-risk-control, semantic-segmentation, multi-class-pixel-sets, uncertainty-heatmap, varisco, loveda, remote-sensing, post-hoc]
verified: "2026-10-09 via curl to export.arxiv.org/api/query?id_list=2405.05145 (title, authors, date, abstract), curl to api.crossref.org (CVPRW 2024, pages 3574-3584, DOI), and WebFetch of arxiv.org/html/2405.05145 (method, losses, datasets, Tables 1 and 2, code URL, limitations)"
takeaway: "Applies Conformal Risk Control to multi-class segmentation so each pixel gets a set of plausible classes with an image-level risk guarantee, and turns set size into a heatmap; tested on LoveDA aerial land cover, so SatClip can reuse it for class-level masks and an 'ambiguous pixels' layer"
---

# Mossina, Dalmau and Andéol 2024, Conformal semantic segmentation

## Problem
Segmentation networks output one label per pixel with uncalibrated softmax scores. Users get no statement about how often the mask is wrong or where the ambiguity sits, and existing conformal work mostly treats whole images or binary masks.

## Approach
- Post-hoc and model-agnostic: uses a pretrained segmentation model's softmax and a held-out calibration split.
- Per pixel, the prediction set includes every class whose softmax score clears a threshold set by lambda (the LAC parametrisation); the top-1 class is always kept so no pixel is empty.
- Lambda is calibrated with Conformal Risk Control (entry 133) so that the expected image-level loss is at most alpha. Losses: a binary loss (fail if pixel coverage in the image drops below a threshold tau), a pixel miscoverage loss (share of ground-truth labels not covered) and a class-weighted variant.
- Visualisation: the "varisco" heatmap colours each pixel by how many classes are in its set, normalised by the class count.

## Data and benchmarks
- Cityscapes (19 classes, PSPNet), ADE20K (150 classes, SegFormer) and LoveDA (7 land-cover classes, aerial imagery, PSPNet), via MMSegmentation pretrained weights.
- Validation data split into calibration and test, averaged over ten shuffles.
- Metrics: empirical test risk (should be near alpha) and activation ratio (mean classes per labelled pixel, i.e. set size).

## Key results
- Empirical risk lands near alpha across settings; for LoveDA with the thresholded binary loss (alpha 0.1, tau 0.90) risk was 0.092 with about 3.9 classes per pixel on average.
- With the miscoverage loss on LoveDA at alpha 0.005, risk was 0.003 with about 6.8 of 7 classes per pixel: valid but almost uninformative.
- One Cityscapes setting (alpha 0.1, tau 0.99) showed mean risk 0.106, slightly above target, within its spread.
- Stricter losses or small alpha push sets toward all classes, which the authors read as a sign the model is not good enough.

## Limitations
- Guarantee is marginal and per image, not per pixel or per class.
- Requires exchangeable calibration and test data, separate from training data.
- Heatmaps track softmax ambiguity and are only comparable across models calibrated at the same alpha; the reading of edge versus interior uncertainty is a heuristic.
- Class-conditional guarantees, panoptic segmentation and video are left for future work.

## What it means for SatClip
- Adopt: for land-cover style questions (cropland, built-up, water), output per-pixel class sets calibrated with CRC and report area as a range: the lower end counts pixels whose set is only the target class, the upper end counts pixels whose set contains it.
- Adopt: render the set-size heatmap as an optional "ambiguous pixels" layer on the evidence card, labelled with the alpha it was calibrated for.
- Adopt: if the calibrated sets cover most classes over the region mask, abstain with a next step (for example, wait for a cloud-free Sentinel-2 pass or use the Sentinel-1 water product) instead of reporting a near-meaningless range.
- Watch: LoveDA is high-resolution aerial RGB; set sizes at 10 m Sentinel-2 resolution with mixed pixels will likely be larger and must be measured on Indian labels.
