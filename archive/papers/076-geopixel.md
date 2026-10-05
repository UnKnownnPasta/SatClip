---
id: 076
title: "GeoPixel: Pixel Grounding Large Multimodal Model in Remote Sensing"
authors: "Akashah Shabbir, Mohammed Zumri, Mohammed Bennamoun, Fahad S. Khan, Salman Khan"
year: 2025
venue: "ICML 2025"
link: https://arxiv.org/abs/2501.13925
code: https://github.com/mbzuai-oryx/GeoPixel
category: rs-vlm
era: recent
tags: [vlm, pixel-grounding, segmentation, grounded-conversation, high-resolution, sam2, internlm, optical-rgb]
verified: "2026-10-05 via https://arxiv.org/abs/2501.13925, https://arxiv.org/html/2501.13925 and https://github.com/mbzuai-oryx/GeoPixel (README states ICML 2025 acceptance)"
takeaway: "First RS chat model that emits masks inside its answer; useful pattern for linking each claim to a region, but masks are about 52 mIoU so SatClip's region mask must still come from instruments"
---

# GeoPixel: Pixel Grounding Large Multimodal Model in Remote Sensing

## Problem
Grounded multimodal models from the natural image world (LISA, PixelLM, GLaMM) do poorly on overhead imagery: objects are tiny, densely packed and vary greatly in scale, and image resolution is far above what a standard vision encoder accepts. There was also no RS dataset where phrases in a conversation are linked to pixel masks.

## Approach
GeoPixel is a 7B large multimodal model initialized from InternLM-XComposer-2.5 (InternLM2 7B language model, frozen CLIP ViT-L at 560x560). An adaptive image divider splits a high-resolution scene into local patches plus a global view, so inputs up to 4K in any aspect ratio can be encoded. A second grounding encoder initialized from SAM-2, plus a pixel decoder, turns special segmentation tokens in the generated text into masks, so the model produces "grounded conversation": a description where each mentioned object or group is tied to a mask. The LLM is tuned with LoRA; training took about 3 days on two A6000 GPUs.

## Data and benchmarks
GeoPixelD is built semi-automatically from iSAID (cropped to 800x800 tiles) using set-of-marks prompting and spatial priors: 53,816 grounded phrases linked to 600,817 object masks, with three tiers of annotation (whole scene, individual instances, dense groups). Captions were drafted by InternLM-XComposer and then structured. Evaluation covers RS grounded conversation generation (RS-GCG) on GeoPixelD and referring segmentation on RRSIS-D.

## Key results
From the paper's tables:
- RS-GCG overall: AP50 19.0, mIoU 52.3, mask recall 38.8, CIDEr 21.6, versus GLaMM fine-tuned on the same data at AP50 12.5, mIoU 46.4. Zero-shot GLaMM is near zero (AP50 0.5).
- RRSIS-D referring segmentation (fine-tuned): test P@0.5 83.33, oIoU 84.90, mIoU 67.30, ahead of the specialist RMSIN (test mIoU 64.20).
- More inference patches improve every metric, so resolution matters.

## Limitations
The authors report wrong mask association, confusion between instance and semantic (group) masks, repeated descriptions of similar objects, and fragmented or overlapping masks in crowded scenes. It is RGB optical only (iSAID imagery), 7B parameters, GPU-bound, and its grounding data comes from one source dataset of mostly urban, high-resolution scenes. No confidence or abstention mechanism is described.

## What it means for SatClip
- Adopt the output pattern, not the model: GeoPixel shows that linking each phrase of an explanation to a specific mask is what users of RS assistants now expect. SatClip can do the same cheaply by having the VLM cite region IDs that point to masks already produced by SAR thresholding or NDVI differencing.
- Avoid using a VLM-generated mask as the evidence region. A best-in-class overall mIoU near 52 and mask recall under 40% on its own benchmark is far too loose for a district flood area figure.
- It is optical only and built on 0.5 m class urban imagery; it says nothing about 10 m Sentinel-1 under monsoon cloud, which is SatClip's core case.
- Comparison point for the pitch: GeoPixel grounds words in pixels but does not measure anything, attach scene IDs or dates, or abstain. SatClip's evidence card grounds numbers in instruments, which is a different and more auditable kind of grounding.
