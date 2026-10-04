---
id: 023
title: "Remote Sensing ChatGPT: Solving Remote Sensing Tasks with ChatGPT and Visual Models"
authors: "Haonan Guo, Xin Su, Chen Wu, Bo Du, Liangpei Zhang, Deren Li"
year: 2024
venue: "IGARSS 2024 (arXiv comment says submitted; README indicates acceptance)"
link: https://arxiv.org/abs/2401.09083
code: https://github.com/HaonanGuo/Remote-Sensing-ChatGPT
category: eo-agents
era: recent
tags: [llm-agent, tool-use, chatgpt, task-decomposition, captioning, detection, segmentation]
verified: "2026-10-04 via https://arxiv.org/abs/2401.09083 and https://github.com/HaonanGuo/Remote-Sensing-ChatGPT"
takeaway: "Simple LLM plan-and-call-tools loop with no quantitative evaluation; copy the loop with an open CPU LLM and add confidence propagation and abstention"
---

# Remote Sensing ChatGPT: Solving Remote Sensing Tasks with ChatGPT and Visual Models

## Problem
Non-experts cannot easily chain remote sensing models to answer a question about an image, and a text-only LLM cannot see pixels.

## Approach
ChatGPT acts as a planner: it parses the user request, splits it into subtasks, calls specialist vision models one at a time, and merges their outputs into a natural language answer. Visual cues (text summaries of the image produced by vision models) are injected into the prompt so the LLM can reason about content it cannot perceive directly. The design is meant to be extensible to new tools such as foundation models.

## Data and benchmarks
No benchmark dataset is introduced. The repository lists the plugged-in tools: BLIP captioning, ResNet scene classification, YOLOv5 detection and counting, Swin plus UperNet segmentation, HRNet land-use classification and Canny edges. GPT-4 is supported for multi-round chat.

## Key results
The abstract and README show qualitative demos only. No quantitative accuracy, latency or task success figures were found on the fetched pages, so none are reported here.

## Limitations
No systematic evaluation, so reliability is unknown. Depends on a closed, paid API. Tools are optical RGB models; there is no SAR, multispectral, temporal or georeferenced handling, and no confidence or abstention mechanism. Errors from one tool propagate silently into the final answer.

## What it means for SatClip
- Adopt the plan, call tools, summarise loop as a simple architecture, but replace ChatGPT with a small open LLM that can run on CPU.
- Carry each tool's confidence and scene metadata through the chain; abstain if any critical step is below threshold, which this system does not do.
- Beat it by adding Sentinel-1/2 aware tools (water index, SAR flood mask, change detection) fed from STAC.
- Build a small labelled query set with task success metrics from day one, since the lack of evaluation is this paper's main weakness.
- Keep tool outputs visible to the user (masks, counts) so the narrative answer can be checked.
