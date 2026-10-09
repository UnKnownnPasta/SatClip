---
id: 208
title: "Beyond detection: cooperative multi-agent reasoning for rapid onboard EO crisis response"
authors: "Alejandro D. Mousist, Pedro Delgado de Robles Martín, Raquel Lladró Climent, Julian Cobos Aparicio"
year: 2026
venue: "Accepted for presentation at ESA 4S Symposium 2026 (per arXiv comment); arXiv:2603.19858 (v1 March 2026); authors at Thales Alenia Space España"
link: https://arxiv.org/abs/2603.19858
code: "None stated in the text read"
category: eo-agents
era: upcoming
tags: [onboard-ai, multi-agent, edge-computing, qwen2-vl-2b, qwen2.5-3b, quantized, sentinel-1-flood, sentinel-2-wildfire, routing, structured-json]
verified: "2026-10-09 via curl to https://export.arxiv.org/api/query?id_list=2603.19858 (title, authors, date, 4S Symposium comment, abstract) and curl of https://arxiv.org/html/2603.19858v1 (agent design, models and quantisation, flood specialist using Sentinel-1, IoU 0.554 on CEMS from SenForFlood, decision agent confidence definition, 27-sample testbench, conclusions); the numeric speed-up values in Table 1 did not survive HTML text extraction and are not reported here"
takeaway: "Small quantised models (Qwen2-VL-2B at 4-bit, Qwen2.5-3B at 8-bit) on a flight-representative edge board route Sentinel-2 scenes to wildfire or Sentinel-1 SAR flood specialists and fuse their JSON reports into an alert with an agreement-based confidence; shows compact VLM plus classical-tool agents with SAR flood tools run on constrained hardware, but the confidence is not calibrated"
---

# Mousist et al. 2026, onboard multi-agent EO crisis response

## Problem
Disaster alerts from satellites are slowed by downlink limits and by running every analysis on every scene. The authors want agents onboard that only run expensive analyses when a quick check suggests a hazard.

## Approach
- Early Warning agent: Qwen2-VL-2B, 4-bit quantised, looks at Sentinel-2 RGB and emits a short JSON hypothesis (suspected hazard type plus a brief explanation).
- Specialist agents run classical and ML tools, then a Qwen2.5-3B (8-bit) model summarises tool outputs into JSON:
  - Wildfire agent: Sentinel-2 SWIR and NIR tools, a DeepLabV3+ active-fire segmenter, spectral indices, and a burned-area tool requiring agreement of two indices.
  - Flood agent: Sentinel-1 SAR with an ML segmenter separating flood from permanent water and a fixed decision threshold.
- Decision agent fuses the early hypothesis and specialist reports into a final event type, a confidence score defined as the level of agreement across sources, and an explanation.
- Compared with a static pipeline that always runs every specialist.

## Data and benchmarks
- Proof-of-concept on the engineering model of an edge-computing platform described as currently deployed in orbit.
- 27 test samples (wildfire, flood, no event); the flood segmenter reports IoU 0.554 on the CEMS subset of SenForFlood.

## Key results
- Routing gives large speed-ups on no-event scenes (specialists skipped) and smaller gains on event scenes; on small scenes the early-warning overhead can make it slightly slower than the static baseline. The exact speed-up figures were not recovered from the HTML and should be read from Table 1 of the paper.
- Speed-up correlates with scene area within each regime.
- The authors report coherent decisions and improved semantic consistency, assessed qualitatively.

## Limitations
- Very small evaluation (27 samples) focused on compute, not detection accuracy; the authors say they did not benchmark the detection models themselves.
- Confidence is agreement between agents, not a calibrated probability, and there is no abstention path.
- Flood segmenter IoU of 0.554 is modest.
- The arXiv HTML still contains unedited draft notes in the related-work section, suggesting limited polishing; conference acceptance is for presentation at a symposium.

## What it means for SatClip
- Adopt: the routing idea. A cheap first check (cloud fraction, quick water index) deciding whether to run the SAR chain matches SatClip's automatic SAR fallback and keeps CPU time low.
- Adopt: small quantised models (2B to 3B) are enough for structured JSON hypotheses and summaries on constrained hardware, consistent with SatClip's CPU target.
- Beat: replace agreement-as-confidence with a calibrated score, and add an abstain outcome when optical and SAR disagree.
- Novelty: weakens the claim slightly. It shows that small VLM plus classical-tool agents with a Sentinel-1 SAR flood tool, structured outputs and a confidence field can run on resource-limited hardware, so "SAR flood on low-resource hardware with an LLM front end" is not new. The confidence is uncalibrated, there is no abstention, no receipt, no live archive retrieval and no non-expert user interface, so SatClip's combination claim stands.
