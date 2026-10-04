---
id: 066
title: "Guidelines for Human-AI Interaction"
authors: "Saleema Amershi, Dan Weld, Mihaela Vorvoreanu, Adam Fourney, Besmira Nushi, Penny Collisson, Jina Suh, Shamsi Iqbal, Paul N. Bennett, Kori Inkpen, Jaime Teevan, Ruth Kikin-Gil, Eric Horvitz"
year: 2019
venue: "CHI 2019 (Proceedings of the 2019 CHI Conference on Human Factors in Computing Systems, pp. 1-13)"
link: https://doi.org/10.1145/3290605.3300233
code: none
category: human-factors
era: historical
tags: [hci, design-guidelines, human-ai-interaction, ux, error-handling, expectations, chi]
verified: "2026-10-04 via https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/ and Crossref record for 10.1145/3290605.3300233"
takeaway: "18 validated design guidelines for AI products; SatClip should use them as a checklist for its chat UI and evidence card, especially setting expectations, scoping when unsure and supporting correction"
---

# Guidelines for Human-AI Interaction

## Problem
AI features behave probabilistically and can be wrong in confusing ways, and designers lacked a consolidated, tested set of guidelines for how such systems should behave with users.

## Approach
The authors gathered over two decades of human-AI interaction recommendations, synthesised them into a candidate list and refined it through several rounds of evaluation. The final set of 18 guidelines is grouped by when they apply: initially (before use), during interaction, when the system is wrong, and over time. Examples include making clear what the system can do and how well it can do it, scoping services when in doubt, supporting efficient correction and dismissal, making clear why the system did what it did, and learning from user behaviour carefully.

## Data and benchmarks
A user study with 49 design practitioners who checked the guidelines against 20 popular AI-infused products, rating whether each product applied or violated each guideline.

## Key results
- The 18 guidelines were judged clear and applicable across a wide range of AI products.
- Many popular products violated guidelines, notably those about communicating capability and handling errors.
- Received a CHI 2019 Honorable Mention award (per the Microsoft Research page).

## Limitations
- Evaluated by designers inspecting products, not by measuring outcomes for end users.
- Generic guidelines: they say what to do, not how to do it for a specific domain like flood mapping.
- The ACM DL page returned 403 to our fetcher; we verified metadata via Microsoft Research and Crossref, not the ACM page itself.

## What it means for SatClip
- "Make clear what the system can do": the first screen should state plainly what SatClip answers (flood extent, vegetation change, land cover from Sentinel-1/2) and what it does not (individual buildings, crop yield, real-time alerts).
- "Make clear how well the system can do it": show calibrated confidence on every evidence card and link a short page on known failure modes (cloud, wind on water, terrain shadow).
- "Scope services when in doubt": our abstention rule is a direct implementation; the abstain message should suggest a narrower question or a different date rather than just refusing.
- "Support efficient correction": let users redraw the region or pick another scene date in one click, and let them flag a wrong answer for review.
- Use the 18 items as a review checklist before each demo, scoring our UI the way the 49 practitioners scored products.
