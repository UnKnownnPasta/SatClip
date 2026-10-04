---
id: 040
title: "Remote Sensing Image Change Captioning With Dual-Branch Transformers: A New Method and a Large Scale Dataset"
authors: "Chenyang Liu, Rui Zhao, Hao Chen, Zhengxia Zou, Zhenwei Shi"
year: 2022
venue: "IEEE Transactions on Geoscience and Remote Sensing (TGRS), vol. 60, 5633520, DOI 10.1109/TGRS.2022.3218921"
link: https://doi.org/10.1109/TGRS.2022.3218921
code: https://github.com/Chen-Yang-Liu/RSICC
category: change-detection
era: recent
tags: [change-captioning, levir-cc, vision-language, transformer, rsiccformer, natural-language, building-change, optical-rgb]
verified: "2026-10-04 via https://research.buaa.edu.cn/en/publications/remote-sensing-image-change-captioning-with-dual-branch-transform/"
takeaway: "LEVIR-CC (10,077 pairs, 50,385 captions, half no-change) is the standard change-captioning set; good template data for SatClip's explanation layer, but captions carry no measured quantities"
---

# Remote Sensing Image Change Captioning With Dual-Branch Transformers: A New Method and a Large Scale Dataset

## Problem
Change maps are hard for non-experts to read. The task here is to generate a natural-language sentence describing what changed between two images of the same place, which needs a model that can tell real changes from irrelevant ones such as lighting.

## Approach
RSICCformer has three parts: a CNN that extracts features from each image, a dual-branch transformer encoder that models each date and their differences to highlight changed regions, and a transformer caption decoder that writes the sentence.

## Data and benchmarks
LEVIR-CC is built from LEVIR-CD (entry 037) imagery: 10,077 bitemporal pairs of 256x256 pixels at 0.5 m over 20 Texas regions with 5 to 15 year gaps, and 50,385 sentences (5 per pair). It is balanced: 5,038 change pairs and 5,039 no-change pairs. Split: 6,815 train, 1,333 validation, 1,929 test. Annotators were told to describe significant changes and ignore irrelevant ones like illumination. Metrics: BLEU, METEOR, ROUGE-L, CIDEr-D.

## Key results
From the paper PDF on the LEVIR lab site: on the LEVIR-CC test set RSICCformer reaches BLEU-4 62.77, METEOR 39.61, ROUGE-L 74.12 and CIDEr-D 134.12. The abstract reports gains of 4.98 BLEU-4 and 9.86 CIDEr-D points over prior methods.

## Limitations
Captions are qualitative ("many houses were built along the road") and contain no measured area, count or confidence. N-gram metrics reward phrasing similar to references, not factual correctness. Single region, RGB, sub-metre imagery, buildings and roads only. The authors themselves list weak handling of objects at varied sizes and of deciding whether a change of interest happened at all.

## What it means for SatClip
- Use LEVIR-CC's balanced change/no-change design as the template for SatClip's explanation evaluation: the language layer must say "no meaningful change" as often as it describes change, and be tested on both.
- Reuse its caption style (object plus change type plus location) for SatClip explanation templates, but fill numbers only from instrument outputs ("water gained 3.2 sq km in the north-east of the block, confidence 0.87").
- Do not let a captioning model state quantities; LEVIR-CC captions were never tied to measurements, so any number it emits is ungrounded.
- Evaluate SatClip explanations on factual consistency with the instrument output, not BLEU or CIDEr.
