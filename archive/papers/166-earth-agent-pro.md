---
id: 166
title: "Earth-Agent-Pro: Towards Real-World Full-Chain Earth Observation with Agents"
authors: "Zhutao Lv, Chenhao Dang, Yi Feng, Yanpei Gong, Xiaolei Wang, Junyan Ye, Conghui He, Weijia Li"
year: 2026
venue: "arXiv preprint (arXiv:2609.12533, September 2026); no peer-reviewed venue yet"
link: https://arxiv.org/abs/2609.12533
code: "Not released (arXiv comment says code and datasets will be released soon)"
category: eo-agents
era: upcoming
tags: [tool-agents, plan-and-execute, expert-skills, structured-memory, data-acquisition, grpo, verifiable-rewards, qwen, earth-bench-pro]
verified: "2026-10-07 via curl to https://export.arxiv.org/api/query?id_list=2609.12533 (title, authors, date, comment, abstract); numbers from the abstract only"
takeaway: "The strongest full-chain EO agent so far (finds and prepares its own data, records accepted evidence in structured memory) moves toward SatClip's design with expert-authored skills, yet still reaches only about two thirds accuracy with GPT-5 and half with a 9B open model, and has no user-facing confidence or abstention"
---

# Lv et al. 2026, Earth-Agent-Pro (full-chain EO agent)

## Problem
Earlier EO agents, including Earth-Agent (entry 094), start from data that is already supplied, and benchmarks give prepared inputs or answer options. Real questions require the agent to find observations, prepare them, compute, and conclude from what it actually measured.

## Approach
- Plan-and-Execute framework where **expert-authored skills** constrain planning and tool use.
- Workflow-centred structured memory stores planned steps, *accepted evidence* and their dependencies; when new evidence invalidates a step, only the dependent remainder of the workflow is repaired.
- Separate LLM adapters: supervised fine-tuning for the planner, and GRPO with locally verifiable rewards for the executor's tool-argument grounding.

## Data and benchmarks
- Earth-Bench-Pro: 248 expert task cores posed as 744 questions in three regimes; the 248 open-world execution questions cover RGB, spectral data and RS products, with executable reference trajectories and open-ended answers grounded in execution evidence.

## Key results
- With a GPT-5 backbone: 66.13% LLM-as-judge accuracy, 20.95 points above ReAct, and 24.44 points better on tools-in-order.
- Tuning both adapters lifts Qwen3.5-9B from 38.31% to 50.00% (an 11.69-point gain).
- Planner adapter helps workflow composition; executor adapter helps argument grounding.

## Limitations
- Accuracy is judged by an LLM, not by exact numeric checks; one in three answers is still wrong with the best backbone.
- No calibrated confidence, abstention or user-visible provenance described in the abstract; the evidence memory serves the agent's own repair loop.
- Code and data not yet released; heavy models, not CPU-friendly.

## What it means for SatClip
- **Convergent evidence**: the best-performing EO agent now constrains planning with expert-written workflows, which is a move toward SatClip's fixed instrument recipes; cite it as support, not competition.
- **Adopt** the "accepted evidence plus dependencies" record: SatClip's receipt already lists scenes and parameters; adding which step depends on which makes partial re-runs and audits easier.
- **Beat it** on reliability for a narrow scope: a fixed router plus calibrated instruments should exceed 66% on flood and crop questions and abstain on the rest; report exact-match accuracy, not LLM-as-judge.
