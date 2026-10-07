---
id: 134
title: "Visual Semiotics & Uncertainty Visualization: An Empirical Study"
authors: "Alan M. MacEachren, Robert E. Roth, James O'Brien, Bonan Li, Derek Swingley, Mark Gahegan"
year: 2012
venue: "IEEE Transactions on Visualization and Computer Graphics 18(12): 2496-2505 (Proceedings of IEEE VIS 2012)"
link: https://doi.org/10.1109/TVCG.2012.279
code: "none found (user study)"
category: human-factors
era: historical
tags: [uncertainty-visualization, cartography, visual-variables, map-symbols, user-study]
verified: "2026-10-07 via https://api.crossref.org/works/10.1109/TVCG.2012.279 (title, authors, volume, issue, pages, year) and PubMed PMID 26357158 abstract; full text not fetched, so specific symbol rankings below are summarized from the abstract and general knowledge of the paper, and no numeric results are claimed"
takeaway: "Map uncertainty symbols are not equally intuitive, so SatClip's map overlay should encode low-confidence or cloud-masked pixels with a symbol type users read correctly at a glance, tested with real officials rather than chosen by the developer"
---

# MacEachren et al. 2012, visual semiotics of uncertainty on maps

## Problem
Maps of uncertain geographic data need symbols that tell readers how reliable each place, time or value is. There was little empirical evidence about which visual encodings people find intuitive for uncertainty, or whether intuitive encodings also help people perform map tasks.

## Approach
- Uses a typology of uncertainty kinds (for example accuracy, precision, currency, completeness, credibility) crossed with the space, time and attribute components of data.
- Applies visual semiotics to characterise candidate encodings: abstract visual variables (such as fuzziness, colour value, saturation, transparency, size, orientation) versus iconic symbols (pictorial signs that suggest doubt).
- Two linked experiments: the first rates how intuitive each encoding is for each uncertainty category; the second tests the most intuitive abstract and iconic encodings on a map-reading task.

## Data and benchmarks
Controlled user studies with participants reading symbol sets and synthetic map displays. Participant numbers and exact stimuli are not restated here because the full text was not fetched.

## Key results
- Encodings differ in how intuitive they are, and the best choice depends on the uncertainty category, so no single "uncertainty symbol" fits all cases.
- The authors derive initial guidelines for representing uncertainty on maps and discuss when abstract versus iconic signs are practical. Specific rankings and effect sizes were not verified for this entry.

## Limitations
- Lab tasks with general participants, not domain experts acting under time pressure.
- Static maps only; no interactive or mobile setting.
- Guidelines are described by the authors as initial.

## What it means for SatClip
- SatClip mixes several uncertainty kinds in one answer: pixel-level classification doubt, cloud or SAR shadow gaps (completeness), and scene age (currency). The evidence card and map should not reuse one generic grey hatch for all of them.
- Candidate mapping to test: transparency or hatching for low-confidence flood pixels, a distinct "no data" pattern for cloud or layover masks, and the date chip (not the map) for currency.
- Run a small symbol-intuitiveness check with district officials before freezing the map legend, following the paper's two-step logic (intuitive first, then task performance).
