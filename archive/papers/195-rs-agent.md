---
id: 195
title: "RS-Agent: Automating Remote Sensing Tasks through Intelligent Agent"
authors: "Wenjia Xu, Zijian Yu, Boyang Mu, Jiuniu Wang, Zhiwei Wei, Mugen Peng"
year: 2026
venue: "SCIENCE CHINA Information Sciences, 69(8), 180302 (2026), DOI 10.1007/s11432-026-5026-5; arXiv:2406.07089 (v1 June 2024, v4 July 2026)"
link: https://arxiv.org/abs/2406.07089
code: "Paper says code will be at https://github.com/IntelliSensing/RS-Agent (release status not checked)"
category: rs-vlm
era: recent
tags: [agents, task-planning, rag, dualrag, sar-tools, despeckling, qwen2.5-32b, langchain, vqa, counting]
verified: "2026-10-08 via curl to https://export.arxiv.org/api/query (title, authors, journal_ref, DOI, abstract), curl to https://api.crossref.org (journal title and DOI) and curl to https://arxiv.org/html/2406.07089v4 (default backbone, retrieval setup, SAR tool list); WebFetch permission request timed out"
takeaway: "A published 2026 RS agent that routes questions to 18 expert tools (including SAR despeckling and detection) with over 95% task-planning accuracy; it confirms LLM-as-router beats end-to-end MLLMs, but it returns tool outputs without scene provenance, calibrated confidence or abstention"
---

# Xu et al. 2026, RS-Agent

## Problem
RS multimodal LLMs follow instructions and describe images but struggle with tasks that need multi-source data, fine spatial reasoning and expert procedures.

## Approach
- Central Controller: an LLM (default Qwen2.5-32B-Instruct, built on LangChain) that reads intent and plans.
- Dynamic toolkit instantiated with 18 tasks, from low-level SAR despeckling to SAR and optical object detection, aircraft type recognition, land-cover classification, counting and VQA.
- Solution Space with Task-Aware Retrieval: identifies the task type and retrieves expert-written solution plans.
- Knowledge Space with DualRAG: weighted keyword plus global semantic retrieval over RS documents (m3e-base embeddings, FAISS).
- LLM-agnostic: tested with ChatGPT, LLaMA, Qwen and DeepSeek backbones.

## Data and benchmarks
Nine datasets covering 18 tasks; task-planning accuracy compared with Remote Sensing ChatGPT; DualRAG judged pairwise by GPT-4o-mini against LightRAG.

## Key results
- Average task-planning accuracy over seven tasks (Table 1): 95.68% versus 88.49% for Remote Sensing ChatGPT with gpt-4o-mini, and 84.89% versus 72.66% with gpt-3.5-turbo-1106. The gain is not uniform; on some tasks (for example scene classification with gpt-4o-mini) the baseline scores higher.
- Better than single MLLMs on scene classification, counting and RS VQA (abstract).

## Limitations
- Uses a 32B controller; not sized for CPU or offline use.
- Tools return outputs without uncertainty; there is no rule for refusing when a tool is unreliable.
- No flood mapping, change estimation over time or scene search from catalogues in the task set read.

## What it means for SatClip
- Adopt: task-type identification before retrieval is a simple, strong pattern for SatClip's intent parser (flood extent, flood change, crop change), and supports keeping the question set closed.
- Avoid: RAG over free text documents is not needed for SatClip's narrow scope and adds hallucination risk.
- Beat: RS-Agent routes and executes but does not tie answers to scene IDs and dates, report calibrated confidence or abstain; SatClip's claim remains open against this published system.
