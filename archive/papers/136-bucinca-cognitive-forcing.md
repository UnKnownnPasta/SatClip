---
id: 136
title: "To Trust or to Think: Cognitive Forcing Functions Can Reduce Overreliance on AI in AI-assisted Decision-making"
authors: "Zana Buçinca, Maja Barbara Malaya, Krzysztof Z. Gajos"
year: 2021
venue: "Proceedings of the ACM on Human-Computer Interaction 5(CSCW1), pp. 1-21 (CSCW 2021)"
link: https://arxiv.org/abs/2102.09692
code: "none found"
category: human-factors
era: recent
tags: [overreliance, cognitive-forcing, explainable-ai, appropriate-reliance, need-for-cognition]
verified: "2026-10-07 via arXiv API for 2102.09692 (title, authors, abstract, DOI 10.1145/3449287), https://api.crossref.org/works/10.1145/3449287 (journal, volume 5, issue CSCW1, pages 1-21, year 2021) and the arXiv PDF (condition names, nutrition task, MTurk)"
takeaway: "Making users commit to their own guess or ask for the AI answer reduces blind acceptance but is disliked, so SatClip could offer an optional 'check it yourself first' step for high-stakes cards and should keep the default card fast"
---

# Buçinca et al. 2021, cognitive forcing against overreliance

## Problem
People using AI decision aids often accept wrong suggestions. Adding explanations has not reliably reduced this, and may increase it. The authors argue, from dual-process theory, that people do not analyse each recommendation but form shortcuts about when to follow the AI.

## Approach
- Three cognitive forcing designs adapted from medical decision-making: on demand (the AI suggestion is hidden until the user asks for it), update (the user decides alone first, then sees the AI and may revise), and wait (the AI answer appears only after a delay, giving time to think).
- Compared against two simple explainable AI conditions (suggestion with explanation, with or without shown AI confidence) and a no-AI baseline.
- Audited whether effects differed by Need for Cognition, a measure of how much people enjoy effortful thinking.

## Data and benchmarks
Online experiment on Amazon Mechanical Turk with 199 participants. Task: from a meal photo, replace the ingredient highest in carbohydrates with a low-carb but similar-flavoured one, helped by a simulated AI that was sometimes deliberately wrong.

## Key results
- All three forcing designs significantly reduced overreliance compared with the simple explanation conditions.
- Trade-off: the designs that reduced overreliance most received the least favourable subjective ratings.
- People higher in Need for Cognition benefited more, so such interventions can widen gaps between users.

## Limitations
- Lay task and crowd workers, not experts with domain stakes.
- Simulated AI with controlled error placement.
- Short session; long-term habituation to forcing steps not studied.

## What it means for SatClip
- Explanations alone (heatmaps, VLM rationales) should not be expected to stop officials over-trusting a wrong flood number; this agrees with Bansal (067) and Zhang (070) in this archive.
- Consider an optional "estimate first" or "reveal answer" mode for high-stakes uses (relief allocation, published news figures), not for every query, given the user dislike finding.
- The abstention state is itself a strong forcing function: when SatClip says "not enough evidence", the user must think. Make sure it is used where confidence is truly low, not as decoration.
- Watch for unequal benefit: busy field officers may skip effortful steps, so the default card must be safe even when read in a few seconds.
