---
id: 009
title: "RS5M and GeoRSCLIP: A Large Scale Vision-Language Dataset and A Large Vision-Language Model for Remote Sensing"
authors: "Zilun Zhang, Tiancheng Zhao, Yulong Guo, Jianwei Yin"
year: 2024
venue: "IEEE Transactions on Geoscience and Remote Sensing (TGRS), 2024, DOI 10.1109/TGRS.2024.3449154"
link: https://arxiv.org/abs/2306.11300
code: https://github.com/om-ai-lab/RS5M
category: eo-foundation
era: recent
tags: [clip, dataset, peft, zero-shot, retrieval, semantic-localization, domain-adaptation, rs5m]
verified: "2026-10-04 via https://arxiv.org/abs/2306.11300"
takeaway: "Bake off GeoRSCLIP against RemoteCLIP; its PEFT results back the LoRA plan, but keep eval captions human-written"
---

# RS5M and GeoRSCLIP: A Large Scale Vision-Language Dataset and A Large Vision-Language Model for Remote Sensing

## Problem
General vision-language models are trained on everyday objects. The question is how to transfer them efficiently to a specialised domain like remote sensing, where large paired image-text data did not exist.

## Approach
The paper proposes an intermediate Domain pre-trained Vision-Language Model (DVLM) sitting between a general model and domain-specific downstream tasks. To train it, the authors assemble RS5M, then fine-tune CLIP fully and also test several parameter-efficient fine-tuning (PEFT) methods. The resulting model is GeoRSCLIP.

## Data and benchmarks
- RS5M: about 5 million remote sensing images with English descriptions, described as the first large-scale RS image-text dataset.
- Built two ways: filtering public web-scale image-text datasets for RS content, and captioning label-only RS datasets with a pre-trained VLM.
- Evaluated on zero-shot classification (ZSC), cross-modal text-image retrieval (RSCTIR) and semantic localisation (SeLo).

## Key results
From the abstract, GeoRSCLIP improves on the baseline or previous best by:
- 3% to 20% in zero-shot classification,
- 3% to 6% in text-image retrieval,
- 4% to 5% in semantic localisation.
Per-dataset numbers were not checked on the fetched page.

## Limitations
- Many captions are machine-generated, so text noise and model bias propagate into training.
- Web-filtered images vary in source and resolution; Sentinel-class 10 m data is not the focus.
- RGB only, no SAR.
- Gains are reported as ranges; per-task variance matters when picking a backbone.

## What it means for SatClip
- Benchmark GeoRSCLIP head to head with RemoteCLIP on the same Indian Sentinel-2 test set and pick the winner as the CPU backbone, rather than assuming either.
- The PEFT results support our plan to adapt with LoRA instead of full fine-tuning.
- Use the semantic localisation task as a cheap route to coarse region masks from text queries.
- Treat RS5M as a candidate pretraining pool, but audit licence and caption quality before use.
- Avoid relying on auto-captions for evaluation data; keep SatClip's test set human-written.
