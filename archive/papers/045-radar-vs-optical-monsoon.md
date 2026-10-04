---
id: 045
title: "Radar versus optical: The impact of cloud cover when mapping seasonal surface water for health applications in monsoon-affected India"
authors: "Gowri Uday, B. V. Purse, D. I. Kelley, Abi Tamim Vanak, Abhishek Samrat, Anusha Chaudhary, Mujeeb Rahman, F. F. Gerard"
year: 2025
venue: "PLOS ONE, 20(1): e0314033, DOI 10.1371/journal.pone.0314033"
link: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0314033
code: "none (maps and reference data at NERC EIDC, https://doi.org/10.5285/3c23fea1-5b27-4b01-b9ef-fc13346cfedc)"
category: indian-context
era: recent
tags: [monsoon, cloud-cover, sentinel-1, landsat, jrc-global-surface-water, western-ghats, karnataka, kerala, maharashtra, surface-water, optical-limits]
verified: "2026-10-04 via https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0314033"
takeaway: "In Western Ghats districts, July to August cloud cover averaged about 90%, leaving roughly a quarter of surface water unmapped in the optical JRC product; Sentinel-1 VV recovered it, so monsoon questions must default to SAR"
---

# Radar versus optical under monsoon cloud (Western Ghats)

## Problem
Health researchers studying water-linked diseases rely on the JRC Global Surface Water product, the only global long-term monthly water dataset, which is derived from optical Landsat. In monsoon India that product may miss most water exactly when it matters. The paper quantifies how much is lost and whether Sentinel-1 fills the gap.

## Approach
Sentinel-1A VV backscatter at 10 m was thresholded to map surface water in three districts (Shivamogga in Karnataka, Sindhudurg in Maharashtra, Wayanad in Kerala) for 2017 and 2018. Thresholds were set manually, guided by Landsat land cover, and a Bayesian procedure was used to check threshold likelihood. Monthly SAR water was compared with the 30 m JRC product.

## Data and benchmarks
3,202 ground reference points from field surveys; monthly comparisons across two years and three districts.

## Key results
- July to August average cloud cover was about 92% (2017) and 90% (2018), leaving 25% and 23% of surface water area unmapped in the JRC product; in monsoon months JRC detected almost no water bodies while SAR showed the seasonal peak.
- June to August average monthly area difference between SAR and JRC: about 7,855 sq km (Shivamogga), 4,289 sq km (Sindhudurg) and 1,765 sq km (Wayanad), as reported.
- Under low cloud both approaches exceeded 98% overall accuracy, with SAR better on producer's and user's accuracy, especially for small features.
- SAR found tens of thousands of extra small water patches (for example about 34,894 more in Shivamogga), many being flooded paddy.

## Limitations
- Reference points were roadside-biased, not stratified random.
- The Bayesian threshold check was inconsistent between seasons without enough validation data.
- SAR misses water under forest canopy, vegetated wetlands and narrow tree-lined channels.
- Thresholds were manual, so transfer to other districts needs re-tuning.

## What it means for SatClip
- Adopt as the citation for the routing rule: for June to September queries in monsoon India, default to Sentinel-1 and treat optical as opportunistic; the planner should check scene cloud fraction first and fall back to SAR automatically.
- Avoid using JRC Global Surface Water as "ground truth" for monsoon months: use it only as a dry-season permanent-water mask, since in monsoon it under-maps water by design.
- Abstain or downgrade confidence for water questions under dense forest canopy (Western Ghats, Northeast), which SAR cannot see through at C-band; say so on the card.
- Report flooded paddy as a distinct likely confusion: SAR water in a paddy mask during transplanting may be cultivation, not disaster flooding, so the card should compare against the same month in a normal year.
</content>
</invoke>
