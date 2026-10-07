---
id: 137
title: "Explanations Can Reduce Overreliance on AI Systems During Decision-Making"
authors: "Helena Vasconcelos, Matthew Jörke, Madeleine Grunde-McLaughlin, Tobias Gerstenberg, Michael S. Bernstein, Ranjay Krishna"
year: 2023
venue: "Proceedings of the ACM on Human-Computer Interaction 7(CSCW1), pp. 1-38 (CSCW 2023)"
link: https://arxiv.org/abs/2212.06823
code: "none found"
category: human-factors
era: recent
tags: [overreliance, explanations, cost-benefit, verification-cost, appropriate-reliance]
verified: "2026-10-07 via arXiv API for 2212.06823 (title, authors, abstract) and https://api.crossref.org/works/10.1145/3579605 (journal, volume 7, issue CSCW1, pages 1-38, date 2023-04-14); explanation types checked in the arXiv PDF"
takeaway: "Explanations only cut overreliance when they make checking the AI cheaper than trusting it, so SatClip's evidence (scene chips, before/after thumbnails) must let an official verify the headline number in seconds"
---

# Vasconcelos et al. 2023, explanations that lower verification cost

## Problem
Earlier studies found that AI explanations do not reduce overreliance (accepting wrong AI answers) compared with showing predictions alone. Some attribute this to unavoidable cognitive bias. The authors argue people make a strategic choice about whether to engage with an explanation.

## Approach
- Cost-benefit framework: people weigh the effort and reward of checking the task themselves (with the help of the explanation) against simply relying on the AI.
- Maze-solving task with a simulated AI that suggests an exit path, sometimes wrongly.
- Manipulations: task difficulty (maze size), explanation type and difficulty (highlighted path that is easy to check, written step lists that are harder, plus incomplete and salient highlight variants), and monetary bonus for accuracy.
- A final study adapts the Cognitive Effort Discounting paradigm to measure how much people value each explanation type.

## Data and benchmarks
Five online studies with 731 participants in total, all using the maze task.

## Key results
- Harder tasks raised overreliance; easier-to-check explanations reduced it compared with harder explanations; higher monetary rewards for correctness reduced it.
- Utility measurements supported the cost-benefit account.
- Suggests that some prior null results came from explanations that did not lower the cost of verifying the AI.

## Limitations
- Artificial maze task where the ground truth is fully visible and checkable, unlike many real decisions.
- Simulated AI; crowd participants.
- Exact effect sizes per study are not restated here.

## What it means for SatClip
- Design evidence for verifiability, not persuasion: a before/after Sentinel-1 thumbnail pair with the flood mask outline lets a user check "is that really water" faster than reading a paragraph of VLM rationale.
- Scene ID and date chips should be one tap away from the actual image, so checking is cheap.
- Where checking is inherently hard (for example crop stress from subtle index changes), expect more overreliance and lean more on calibrated confidence and abstention.
- Complements 136 (Buçinca): instead of forcing effort, lower the effort needed to verify.
