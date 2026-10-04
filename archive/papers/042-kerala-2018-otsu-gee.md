---
id: 042
title: "Flood inundation mapping- Kerala 2018; Harnessing the power of SAR, automatic threshold detection method and Google Earth Engine"
authors: "V. Tiwari, V. Kumar, M. A. Matin, A. Thapa, W. L. Ellenburg, N. Gupta, S. Thapa"
year: 2020
venue: "PLOS ONE, 15(8): e0237324, DOI 10.1371/journal.pone.0237324"
link: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0237324
code: none
category: indian-context
era: recent
tags: [sentinel-1, sar, flood-mapping, otsu, thresholding, kerala-2018, google-earth-engine, vv, india, validation-event]
verified: "2026-10-04 via https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0237324"
takeaway: "Otsu on Sentinel-1 VV (Lee 5x5) mapped the Kerala August 2018 flood at about 94.7% OA (kappa 0.87 to 0.88) against Sentinel-2; a ready Indian validation event and baseline for our SAR water instrument"
---

# Flood inundation mapping, Kerala 2018 (Otsu on Sentinel-1 in GEE)

## Problem
The August 2018 Kerala floods were among the worst in the state's recent history, and persistent monsoon cloud made optical mapping unreliable. Responders needed a fast, automatic way to map inundation without hand-tuned thresholds.

## Approach
Sentinel-1 GRD VV backscatter was processed in Google Earth Engine with a Lee speckle filter (5x5 window). Otsu's method picked a water / non-water threshold automatically from the histogram for each date. Flooded area in August 2018 was compared with a non-flood reference (January 2018) and with August of earlier years (2015 to 2017) to separate the event from normal monsoon water.

## Data and benchmarks
Sentinel-1 acquisitions on 9 and 21 August 2018 over Kerala. Validation used reference samples interpreted from Sentinel-2 imagery of 10 and 20 August 2018. The paper lists heavily affected places such as Chengannur, Kuttanad, Aluva, Chalakudy and N. Paravur.

## Key results
- Overall accuracy 94.73% (9 Aug) and 94.71% (21 Aug); kappa 0.87 and 0.88.
- Reported mean backscatter: water about -23.5 dB (std about 2.4), non-water about -8.8 dB (std about 1.5).
- The exact Otsu cut-off per date was not found in the text we read; do not quote one.

## Limitations
- Validation against Sentinel-2 photo-interpretation on cloud-gapped days, not independent field data, and samples may favour easy, clear areas.
- No explicit permanent-water mask, HAND/slope mask or urban flood handling was described in what we read.
- Global Otsu on a large area assumes a bimodal histogram; it can fail where water is a small fraction of the scene.
- The authors note heavy rain cells can add noise to C-band, and suggest L or X band or a two-dimensional Otsu as improvements.

## What it means for SatClip
- Adopt Kerala August 2018 (Sentinel-1 on 9 and 21 August, Sentinel-2 on 10 and 20 August) as a named regression test for the flood instrument; our receipt should reproduce roughly 95% OA on comparable samples or explain why not.
- Use the reported class means (water near -23 dB, land near -9 dB in VV) only as sanity bounds; compute the threshold per tile with Otsu on tiles that pass a bimodality check (in the style of Sen1Floods11 tiling), and abstain on tiles that fail it.
- Beat it by adding what it lacks: a dry-season permanent-water mask, a HAND or slope mask for hill terrain (Western Ghats), and a change-detection step against a same-season normal year, all stated on the card.
- Report the threshold value used on every card; this paper shows that leaving it out makes a result hard to re-check.
</content>
</invoke>
