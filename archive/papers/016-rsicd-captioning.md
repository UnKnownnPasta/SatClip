---
id: 016
title: "Exploring Models and Data for Remote Sensing Image Caption Generation"
authors: "Xiaoqiang Lu, Binqiang Wang, Xiangtao Zheng, Xuelong Li"
year: 2018
venue: "IEEE Transactions on Geoscience and Remote Sensing (TGRS), vol. 56, pp. 2183-2195, DOI 10.1109/TGRS.2017.2776321"
link: https://arxiv.org/abs/1712.07835
code: https://github.com/201528014227051/RSICD_optimal
category: historical
era: historical
tags: [captioning, rsicd, dataset, annotation-guidelines, lstm, attention, bleu, cider, google-earth]
verified: "2026-10-04 via https://arxiv.org/abs/1712.07835, https://ar5iv.labs.arxiv.org/html/1712.07835 and Semantic Scholar API record"
takeaway: "Use its caption annotation rules as SatClip's caption style guide; do not trust BLEU or CIDEr without a grounding check"
---

# Exploring Models and Data for Remote Sensing Image Caption Generation

## Problem
By 2017, remote sensing work focused on scene classification and target detection, but there was no good way to describe an overhead image in a full, accurate sentence. Existing caption sets (UCM-captions, Sydney-captions) were small and unbalanced.

## Approach
The authors first wrote annotation rules tailored to overhead imagery: describe all salient parts, avoid vague size words (large, tall, many) without context, prefer relational terms such as "near" or "next to" over compass directions, and keep sentences at least six words long. These rules target scale ambiguity, category mixing and rotation invariance. They then benchmarked two caption families: a multimodal encoder plus RNN/LSTM decoder, and soft/hard attention decoders, with handcrafted features (SIFT, BoW, Fisher Vector, VLAD) and ImageNet CNNs (AlexNet, VGG16/19, GoogLeNet).

## Data and benchmarks
- RSICD: 10,921 images of 224x224 px from Google Earth, Baidu Map, MapABC and Tianditu, covering land-use scene categories such as airport, farmland, forest and residential (exact class count not confirmed: the fetched render suggested 25, other sources cite 30); about 54,605 sentences (five per image, with duplicates used to fill gaps).
- Also evaluated on UCM-captions (2,100 images, 21 classes) and Sydney-captions (613 images, 7 classes).

## Key results
On RSICD (as read from ar5iv tables), the best attention setting (GoogLeNet, hard attention) reached BLEU-4 about 0.373 and CIDEr about 2.02. The best handcrafted-feature setting (LSTM with VLAD) reached BLEU-4 about 0.178 and CIDEr about 1.18, so CNN features plus attention were clearly ahead.

## Limitations
Imagery is RGB from web map services, not calibrated Sentinel data. Duplicated sentences inflate n-gram scores and caused unstable results at some training ratios. Generated captions copy frequent co-occurrence patterns from training text even when the image disagrees. No grounding, confidence or abstention.

## What it means for SatClip
- Reuse the annotation rules (no unanchored size words, relational phrasing) as the style guide for SatClip captions and LoRA training targets.
- Treat RSICD as a captioning sanity benchmark only; it is RGB, very high resolution, and China-centric, so it says little about 10 m Sentinel-2 over India.
- Do not trust BLEU or CIDEr alone: duplicated references inflate them. Pair them with a factual grounding check against the region mask.
- The co-occurrence hallucination they observed is exactly what calibrated abstention must catch; log caption claims that are not backed by a detector or classifier output.
- RemoteCLIP and later RS VLMs are trained partly on RSICD, so hold it out when testing generalisation to avoid leakage.
