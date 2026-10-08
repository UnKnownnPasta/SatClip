---
id: 193
title: "Agentic AI for Remote Sensing: Technical Challenges and Research Directions"
authors: "Muhammad Akhtar Munir, Muhammad Umer Sheikh, Akashah Shabbir, Muhammad Haris Khan, Fahad Khan, Xiao Xiang Zhu, Begüm Demir, Salman Khan"
year: 2026
venue: "arXiv preprint, position paper (arXiv:2604.24919, v1 27 April 2026, v3 1 June 2026); no peer-reviewed venue listed"
link: https://arxiv.org/abs/2604.24919
code: "Not applicable (position paper)"
category: rs-vlm
era: upcoming
tags: [agents, position-paper, geospatial-state, provenance, verifier, uncertainty, failure-modes, flood-area, tool-use, evaluation]
verified: "2026-10-08 via curl to https://export.arxiv.org/api/query (title, authors, dates, abstract, comment 'Position Paper') and curl to https://arxiv.org/html/2604.24919v3 (state definition, verifier checks, flood-area example, calibration discussion); WebFetch permission request timed out; the paper has no experiments, so no numbers are reported"
takeaway: "A 2026 position paper that argues EO agents must carry CRS, time window, provenance and an uncertainty descriptor in their state and check every step with verifiers, using flood-area estimation as its main failure example; it describes SatClip's design goals but builds no system, so it is citable support rather than prior art"
---

# Munir et al. 2026, Agentic AI for remote sensing (position paper)

## Problem
Generic tool-using LLM agents assume stateless, cheap, text-checkable tool calls. EO workflows are stateful: reprojection, resampling, compositing and aggregation change the data, so a wrong step can pass silently and produce a plausible but invalid final answer.

## Approach
- Lists assumptions of generic agent designs (planner-executor-verifier pipelines, SFT on trajectories, RL with simple rewards) and shows where they break for EO.
- Catalogues EO failure modes: temporal-window mismatch, wrong transformation order, CRS mismatch, unit errors, silent propagation of preprocessing mistakes, and outputs that look right but violate physics.
- Proposes an EO-native formulation: a structured geospatial state that holds data type (raster, mask, vector), CRS, GSD, extent, time window, modality, a reliability or uncertainty descriptor, provenance and tool history; actions are parameterised tool calls; verifiers score admissibility and the validity of each state transition (geometric, temporal, radiometric or physical, provenance and statistical checks).
- Argues that routine steps (radiometric calibration, reprojection, index computation, tiling) should be fixed execution, not agent decisions, and that learned tools may need regional recalibration or threshold re-estimation under domain shift.

## Data and benchmarks
None; it is a conceptual paper. It recommends trajectory-level evaluation rather than final-answer accuracy.

## Key results
- Main illustration contrasts a generic agent trace and an EO-native trace for flood-area estimation from pre and post imagery: the generic one reaches a plausible but invalid area through window, CRS and unit errors.
- States that correct tool orchestration cannot fix a miscalibrated learned model working outside its training distribution.

## Limitations
- No implementation, benchmark or measured gains; claims are argued, not tested.
- Does not specify how the uncertainty descriptor should be computed or calibrated, nor when an agent should refuse to answer.

## What it means for SatClip
- Adopt: use its state schema as a checklist for SatClip's answer record (CRS, pixel spacing, extent, time window, sensor, provenance, uncertainty) and its verifier list as unit tests on every pipeline step.
- Adopt: its point that fixed steps should not be left to an LLM backs SatClip's choice to keep the VLM to intent parsing and explanation.
- Novelty check: this is the closest statement of SatClip's philosophy found so far, including a flood-area example, but it is a position paper with no system, calibration method or abstention rule; SatClip can cite it as motivation and claim the working, calibrated, abstaining implementation.
