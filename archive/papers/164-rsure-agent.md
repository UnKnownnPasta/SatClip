---
id: 164
title: "RSure-Agent: Reliable Use of Tool Observations for Remote Sensing Agents"
authors: "Fuyuan Liu, Nayu Liu, Wenhao Yu, Peijin Wang, Yingchao Feng, Fanglong Yao, Liang Wan, Wei Feng"
year: 2026
venue: "arXiv preprint (arXiv:2610.04836, October 2026); no peer-reviewed venue yet"
link: https://arxiv.org/abs/2610.04836
code: "https://github.com/airs101/RSure-Agent (demo per arXiv comment; code not yet released; not fetched)"
category: eo-agents
era: upcoming
tags: [tool-agents, verification, tool-observations, error-propagation, reliability-prior, process-evidence, reject-option, earthbench, thinkgeo]
verified: "2026-10-07 via curl to https://export.arxiv.org/api/query?id_list=2610.04836 (title, authors, date, comment, abstract); all numbers below are from the abstract"
takeaway: "The closest prior art to SatClip's 'trust the instrument only with evidence' idea: it shows tool outputs are wrong in over a fifth of tool-dependent tasks and adds accept, ask-for-more or reject decisions, but it serves the agent, not a non-expert user, and gives no calibrated confidence or receipt"
---

# Liu et al. 2026, RSure-Agent (verifying tool observations)

## Problem
EO agents trust what their tools return (a detection, an area, a class). Tools can run without error and still be wrong, and the agent then builds its answer on the wrong value.

## Approach
- Measures the problem on 1,229 execution trajectories from three RS agent benchmarks.
- A *verifiable observation protocol*: each tool must return process evidence along with its result, so the agent can check how the value was produced.
- A *task-tool reliability prior* learned offline from task feedback: how well each tool configuration has done on each task type.
- Using both, the agent accepts an observation, requests more evidence, or rejects it.

## Data and benchmarks
- EarthBench (Earth-Agent, entry 094), ThinkGeo (entry 092), TerraLogic, and the CHOICE-420 set.

## Key results
- On each benchmark at least 88.1% of tasks depend on tool observations; at least 22.7% of those contain an incorrect observation even though the tool ran; in at least 82.0% of affected tasks the error reaches the final answer.
- Cuts the error propagation rate by 21.3 to 25.9 percentage points versus the same system with verification and prior switched off.
- On CHOICE-420, plus 5.71 points accuracy over direct answering, averaged over 11 backbones; on EarthBench, 25.9% fewer tool calls than Earth-Agent.

## Limitations
- Very new preprint; code not yet released.
- The reliability prior is a per-tool, per-task summary, not a calibrated probability for the specific answer, and is not shown to the user.
- Rejecting an observation is an internal agent decision; the abstract does not describe user-facing abstention, provenance (scene IDs, dates) or a re-runnable record.

## What it means for SatClip
- **Strongest external support** for SatClip's design: published numbers that tool errors silently propagate in RS agents, which is exactly what SatClip's per-tile calibrated confidence and abstention guard against.
- **Adopt** the idea that each instrument returns process evidence (threshold value, histogram bimodality, valid-pixel share) and that SatClip keeps a per-instrument, per-question-type reliability table from its calibration sets.
- **Beat it** on the user side: SatClip turns the accept or reject decision into a visible calibrated confidence and an abstain message on the card, with scene IDs and a receipt, for a non-GIS official.
