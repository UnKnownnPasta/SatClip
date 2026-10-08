---
id: 178
title: "Change Detection Meets Visual Question Answering"
authors: "Zhenghang Yuan, Lichao Mou, Zhitong Xiong, Xiao Xiang Zhu"
year: 2022
venue: "IEEE Transactions on Geoscience and Remote Sensing, vol. 60, 2022 (DOI 10.1109/TGRS.2022.3203314); arXiv:2112.06343"
link: https://doi.org/10.1109/TGRS.2022.3203314
code: "https://github.com/YZHJessica/CDVQA (stated in the paper; not fetched)"
category: rs-benchmark
era: recent
tags: [change-vqa, cdvqa, second-dataset, bi-temporal, aerial, automatic-qa-generation, change-ratio, benchmark]
verified: "2026-10-08 via curl to https://api.crossref.org/works/10.1109/tgrs.2022.3203314 (title, authors, journal, volume, year), export.arxiv.org API (abstract, DOI link) and https://arxiv.org/html/2112.06343v2 (dataset construction, splits, Tables V and VI); WebFetch permission request timed out"
takeaway: "The founding change-VQA benchmark: 2,968 aerial image pairs and about 122,000 template questions auto-generated from semantic change maps; the baseline gets about 65 to 69% overall but only 24 to 39% on change ratio and smallest change, which is why SatClip computes such numbers from masks instead of asking a model"
---

# Yuan et al. 2022, change detection based VQA (CDVQA)

## Problem
Change detection outputs are maps that non-experts struggle to read. The authors propose letting users ask plain questions about what changed between two dates and get a short answer.

## Approach
- Task: given two co-registered images and a question, output a natural-language answer chosen from a fixed answer set.
- Dataset built automatically from the SECOND semantic change detection dataset (bi-temporal aerial RGB, 0.5 to 3 m, Chinese cities; 2,968 public pairs), using its per-pixel before and after class maps.
- Question families: change or not (pair or single image), increase or decrease, change to what, largest or smallest change, and change ratio. Ratios are binned into 11 classes (0%, then 10-point bins).
- Baseline: shared CNN or ViT encoders for both dates, multi-temporal fusion, fusion with an RNN question embedding, classifier over answers; plus a change-enhancing module.

## Data and benchmarks
More than 122,000 question-answer pairs. Splits by image pair and location: 1,600 pairs for training (65,967 QA), 400 for validation (16,441 QA) and 968 for two test sets (39,686 and 31,036 QA). Test set 2 has a shifted, harder answer distribution with more change-to-what and ratio questions.

## Key results
- ResNet-101 with the change-enhancing module: overall accuracy 69.0% on test set 1 and 65.1% on test set 2; average accuracy about 60%.
- Weakest families: change ratio (about 39%) and smallest change (24 to 31%). Change-or-not is easiest (about 81 to 83%).
- Concatenation beat subtraction and other fusion operators, so naive feature differencing did not capture change well.

## Limitations
- Aerial RGB only, six land-cover classes, Chinese urban scenes; no SAR, no Sentinel data, no water-specific class for floods.
- Answers are classification over a closed set; no masks, no locations, no confidence or abstention.
- Templates are generated from labels, so question language is narrow and answer priors are strong.

## What it means for SatClip
- Adopt: the question taxonomy (change or not, increase or decrease, change to what, largest change, change ratio) maps directly onto SatClip's crop-change and flood-change intents and is a good checklist for the intent parser.
- Avoid: letting a learned VQA head produce ratios or rankings; the 24 to 39% accuracy on those families is the clearest historical argument for computing them from masks in code, as entry 172 later confirms.
- Beat: SatClip returns the mask, the scene IDs and a calibrated confidence alongside the answer, none of which CDVQA provides.
