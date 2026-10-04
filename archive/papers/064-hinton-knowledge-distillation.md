---
id: 064
title: "Distilling the Knowledge in a Neural Network"
authors: "Geoffrey Hinton, Oriol Vinyals, Jeff Dean"
year: 2015
venue: "NIPS 2014 Deep Learning Workshop (arXiv:1503.02531, March 2015)"
link: https://arxiv.org/abs/1503.02531
code: none
category: efficient-inference
era: historical
tags: [knowledge-distillation, model-compression, soft-targets, temperature, cpu-inference, ensembles, specialists]
verified: "2026-10-04 via https://arxiv.org/abs/1503.02531 and https://ar5iv.labs.arxiv.org/html/1503.02531"
takeaway: "Classic recipe for training a small student model on a large teacher's softened outputs; SatClip can use it to shrink a CLIP land-cover head or a question parser so it runs fast on CPU"
---

# Distilling the Knowledge in a Neural Network

## Problem
Large models and ensembles give the best accuracy, but they are too slow and heavy to deploy to many users or on modest hardware. The question is how to move what a big model has learned into a small one that is cheap at inference time.

## Approach
Train the big "teacher" (or ensemble) normally, then train a small "student" to match the teacher's class probabilities produced with a raised softmax temperature. High temperature softens the distribution so the student also learns how the teacher ranks wrong classes (which carry information about similarity between classes). The student loss mixes these soft targets with the usual hard labels; the paper notes the soft-target gradient should be scaled by the square of the temperature. The paper also proposes "specialist" models trained on confusable subsets of classes, alongside one generalist, for very large label spaces.

## Data and benchmarks
- MNIST (small fully connected nets).
- A production speech acoustic model (Android voice search).
- Google's internal JFT dataset (about 100M images, 15K labels) for the specialist experiments.

## Key results
- MNIST: a large net made 67 test errors; a smaller net trained normally made 146; the same small net distilled (temperature 20) made 74.
- Speech: a 10-model ensemble improved frame accuracy from 58.9% to 61.1% (word error rate 10.9% to 10.7%); a single distilled model reached 60.8% and 10.7%, keeping most of the ensemble's gain.
- Soft targets act as a regulariser: with only 3% of the speech training data, a model trained on soft targets reached 57.0% frame accuracy versus 44.5% with hard labels.
- JFT: 61 specialists raised accuracy from 25.0% to 26.1% (a modest relative gain).

## Limitations
- Workshop paper with few, mostly internal benchmarks (speech and JFT results are not reproducible by outsiders).
- No study of calibration of the distilled student, and no measurement of CPU latency or memory.
- The specialist method was not itself distilled back into one model in the paper.

## What it means for SatClip
- Adopt distillation as the main route if the zero-shot CLIP land-cover instrument is too slow on CPU: distil a large CLIP image encoder into a small student on Indian Sentinel-2 chips, keeping the same class prompts as targets.
- Re-check calibration after any distillation or quantization step: the student's confidence feeds the evidence card and the abstention threshold, so we must refit temperature scaling on held-out data rather than trust the teacher's calibration.
- Use soft targets from the teacher on unlabelled Indian scenes as cheap supervision; the 3% data result suggests this helps when labelled data is scarce.
- Keep distillation away from the deterministic instruments (Otsu water, log-ratio, NDVI difference): those are already cheap and must stay exact and auditable.
- Record in the receipt which model variant (teacher or distilled student, plus version) produced a land-cover label.
