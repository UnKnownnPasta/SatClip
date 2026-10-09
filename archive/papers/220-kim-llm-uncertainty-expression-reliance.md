---
id: 220
title: "\"I'm Not Sure, But...\": Examining the Impact of Large Language Models' Uncertainty Expression on User Reliance and Trust"
authors: "Sunnie S. Y. Kim, Q. Vera Liao, Mihaela Vorvoreanu, Stephanie Ballard, Jennifer Wortman Vaughan"
year: 2024
venue: "FAccT 2024 (ACM Conference on Fairness, Accountability, and Transparency), pp. 822-835, DOI 10.1145/3630106.3658941; arXiv:2405.00623"
link: https://doi.org/10.1145/3630106.3658941
code: "None found"
category: human-factors
era: recent
tags: [uncertainty-expression, natural-language-hedging, overreliance, appropriate-reliance, trust, user-study, pre-registered, llm-search]
verified: "2026-10-09 via curl to api.crossref.org (title, five authors, FAccT 2024, pages 822-835, DOI), curl to export.arxiv.org (arXiv comment 'Accepted to FAccT 2024'), and WebFetch of arxiv.org/abs/2405.00623 (participants, task, conditions, findings); effect sizes not read from the full text"
takeaway: "In a pre-registered study with 404 people, first-person hedges ('I'm not sure, but...') lowered agreement with an LLM and raised accuracy by cutting overreliance on wrong answers; impersonal hedges had weaker, non-significant effects, so SatClip's low-confidence wording must be user-tested, not assumed"
---

# Kim et al. 2024, Natural-language uncertainty and reliance

## Problem
LLM answers are fluent and confident in tone even when wrong, which encourages overreliance. Expressing uncertainty in words is an obvious fix, but it was unclear whether it changes behaviour and whether the exact phrasing matters.

## Approach
- Large-scale, pre-registered online experiment.
- Participants answered medical questions with or without a fictional LLM-infused search engine.
- The system's answers varied in uncertainty expression: none, first-person ("I'm not sure, but..."), or general perspective ("It's not clear, but...").
- Measured behavioural reliance (agreement), self-reported trust and confidence, and task accuracy.

## Data and benchmarks
- 404 participants.
- Medical question-answering task with system responses controlled by the researchers (correct and incorrect answers both present).

## Key results
- First-person uncertainty lowered participants' confidence in the system and their agreement with its answers, and raised their accuracy.
- Exploratory analysis attributes the accuracy gain to less overreliance on incorrect answers; overreliance fell but did not disappear.
- General-perspective phrasing gave similar but weaker effects that were not statistically significant.
- Authors conclude that wording matters and should be tested with users before deployment. Exact effect sizes were not checked in this session.

## Limitations
- One domain (medical questions), one simulated system, crowd participants; not experts deciding under time pressure.
- Uncertainty was expressed in words only, without numeric confidence or calibrated probabilities.
- Hedging was manipulated independently of correctness in a controlled way; real systems hedge imperfectly.
- Underreliance on correct but hedged answers is a cost to watch.

## What it means for SatClip
- Adopt: pair the numeric confidence meter with a short plain-language hedge when confidence is in the middle band, and test first-person ("I am not certain...") against impersonal ("The imagery is not clear...") phrasing with district officials and fact-checkers in Hindi and English; this study shows the choice changes behaviour.
- Adopt: drive hedge wording strictly from the calibrated probability band (entry 070 showed confidence displays help calibrate trust only when accurate), never from the language model's own tone.
- Adopt: log, in the receipt, which hedge template was shown, so later audits can check whether users acted on hedged cards differently.
- Avoid: do not rely on hedging alone to prevent misuse; overreliance only dropped, so keep the hard abstention threshold and the "next step" text.
