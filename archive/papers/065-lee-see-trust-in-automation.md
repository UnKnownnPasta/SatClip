---
id: 065
title: "Trust in Automation: Designing for Appropriate Reliance"
authors: "John D. Lee, Katrina A. See"
year: 2004
venue: "Human Factors 46(1): 50-80"
link: https://doi.org/10.1518/hfes.46.1.50_30392
code: none
category: human-factors
era: historical
tags: [trust, reliance, calibration, automation, decision-support, review, display-design]
verified: "2026-10-04 via https://journals.sagepub.com/doi/10.1518/hfes.46.1.50_30392"
takeaway: "Foundational review arguing that trust should match automation capability (calibrated trust), not be maximised; SatClip should design the evidence card to expose when and why instruments are reliable"
---

# Trust in Automation: Designing for Appropriate Reliance

## Problem
Automation fails to deliver its benefits when people misuse it (rely on it when it is wrong) or disuse it (ignore it when it is right). Because people respond to technology socially, trust becomes a key driver of reliance, especially when the system is too complex to fully understand.

## Approach
A broad integrative review drawing on organisational, sociological, interpersonal, psychological and neurological research on trust. The authors build a conceptual model of how trust forms and evolves, how context and the characteristics of the automation shape it, and how the way information is displayed affects whether trust ends up appropriate. Central ideas include calibration (does trust match actual capability?), resolution (does trust distinguish situations where the automation is good from where it is poor?) and specificity (is trust tied to particular functions and conditions rather than the whole system?). They describe trust as resting on the automation's performance, its process (how it works) and its purpose (why it was built).

## Data and benchmarks
Not applicable: a conceptual review and model, not an experiment.

## Key results
- The design goal is appropriate reliance, which means calibrated trust, not more trust.
- Displays that reveal how the automation works and where its limits are can improve calibration and resolution.
- Trust is dynamic: it drops sharply after visible failures and recovers slowly, and it depends on context such as workload and time pressure.

## Limitations
- Mostly drawn from studies of industrial, aviation and process-control automation, before modern ML and conversational AI.
- Offers design principles rather than tested, quantified interventions.
- We read the abstract and metadata on the publisher page; specific section claims above reflect the paper's widely cited framework and should be checked against the full text before quoting.

## What it means for SatClip
- Treat calibration and resolution as product goals: the evidence card should help an official tell a reliable answer (clear SAR water contrast, recent scene) from a weak one (wind-roughened water, old scene, heavy cloud), not just show one global confidence number.
- Show process as well as performance: a one-line "how this was measured" (instrument name, threshold, scene date) on every card supports the process basis of trust.
- Make trust specific to each instrument: separate confidence for flood extent versus land-cover labels, since users should not generalise trust from one to the other.
- Expect trust to crash after a visible mistake in a flood season; abstaining with a clear reason is better than a confident wrong number.
