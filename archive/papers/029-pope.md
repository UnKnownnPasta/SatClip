---
id: 029
title: "Evaluating Object Hallucination in Large Vision-Language Models"
authors: "Yifan Li, Yifan Du, Kun Zhou, Jinpeng Wang, Wayne Xin Zhao, Ji-Rong Wen"
year: 2023
venue: "EMNLP 2023"
link: https://arxiv.org/abs/2305.10355
code: https://github.com/RUCAIBox/POPE
category: trust-calibration
era: recent
tags: [hallucination, lvlm, benchmark, yes-no-probing, pope, evaluation]
verified: "2026-10-04 via https://arxiv.org/abs/2305.10355"
takeaway: "LVLMs often claim objects that are not there, especially frequent or co-occurring ones; POPE's yes/no probing with adversarial negatives is a cheap template for SatClip's hallucination tests"
---

# Evaluating Object Hallucination in Large Vision-Language Models

## Problem
Large vision-language models (LVLMs) frequently describe objects that do not appear in the image. Earlier caption-based hallucination metrics were unstable, sensitive to instructions and to how long or in what style a model writes.

## Approach
The authors first study hallucination systematically across several LVLMs and analyse its causes. They then propose POPE (Polling-based Object Probing Evaluation): ask the model binary questions of the form "Is there a X in the image?" for objects that are present (positives) and absent (negatives). Negatives are drawn in three settings: random, popular (objects frequent in the dataset) and adversarial (objects that often co-occur with the true objects). Metrics are accuracy, precision, recall, F1 and the ratio of "yes" answers.

## Data and benchmarks
MS COCO 2014 validation images, using ground-truth annotations or automatic segmentation (SEEM) to obtain object lists.

## Key results
Most LVLMs tested showed serious object hallucination. Objects that appear often in visual instruction data, or that commonly co-occur with objects in the image, were more likely to be hallucinated. POPE was shown to be more stable and flexible than caption-based evaluation. Per-model scores are in the paper; they were not extracted from the fetched pages, so none are quoted here.

## Limitations
Only object existence is probed, not attributes, counts, relations or quantities. Yes/no answers can be gamed by a model biased toward "no". Natural photos only: no remote sensing, no SAR, no multi-temporal imagery. Ground-truth quality depends on COCO labels or the segmentation tool.

## What it means for SatClip
- Build a small SatClip-POPE: yes/no probes on Indian Sentinel tiles ("Is there standing water in this village polygon?", "Is there a river here?") with adversarial negatives that co-occur in Indian scenes (canals near paddy, brick kilns near towns).
- Run it against the VLM explanation layer to prove the architectural point: when asked directly, the VLM hallucinates, which is why SatClip never lets it produce the measurement.
- Track the yes-ratio: a VLM that over-answers "yes" to "is it flooded?" is the dangerous failure for disaster officials.
- Use the co-occurrence finding as a test design rule: paddy fields in monsoon look like water to a careless model, so include them as hard negatives.
