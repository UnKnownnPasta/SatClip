# What is new in SatClip, and what would have to be true

This document is an honest comparison against the closest existing systems. It is checked against the archive as it grows: version 2 (run 2) covers 50 papers plus the competitor evidence in [docs/reference/problem-evidence.md](docs/reference/problem-evidence.md). A final pass against the whole archive is milestone M8.

Citation keys: `[A001]` is an archive entry and `[E49]` is an evidence-brief claim.

## 1. Comparison

The dimensions are the ones that matter to a district official, extension officer or fact-checker without GIS skills.

| System | Plain-language questions | Fetches live Sentinel data for my area and dates | SAR used automatically under cloud | Scene ID and date on every answer | Region mask | Calibrated confidence | Abstains when unsure | Re-runnable receipt | Runs on CPU or offline | Free or open, usable in India |
|---|---|---|---|---|---|---|---|---|---|---|
| GeoChat [A001] | Yes | No (user supplies image) | No (RGB only) | No | Boxes as text, weak | No | No | No | No (7B) | Open weights |
| EarthGPT [A002] | Yes | No | Can read SAR, no automatic choice | No | No | No | No | No | No | Open data and code; weights not confirmed |
| EarthDial [A003] | Yes | No | Reads S1 VH, no automatic choice | No | Boxes | No | No | No | Possible but slow (4B) | Open weights |
| TEOChat [A007] | Yes, temporal | No | No | No | No | No | No | No | No | Open |
| LHRS-Bot [A005], RSGPT [A006], SkyEyeGPT [A004], RS-LLaVA [A025] | Yes | No | No | No | Partial (some grounding) | No | No | No | No | Mostly open |
| SARChat models [A021] | Yes, SAR only | No | SAR only | No | Partial | No | No | No | Small checkpoints exist | Open |
| Remote Sensing ChatGPT [A023] | Yes | No | No | No | Via tools | No | No | No | No (cloud LLM) | Code open; needs a paid LLM |
| GeoLLM-Engine agents [A024] | Yes | Environment only | No | No | Via tools | No | No | No | No | Research environment; no public code found |
| Google Earth AI and Gemini geospatial reasoning [E49] | Yes | Yes (Google data) | Unknown | Unknown | Yes, on map | Unknown | Unknown | No public evidence | No | US-gated paid tiers; not India |
| NASA and Microsoft Earth Copilot [E50] | Yes | NASA data | Unknown | Dataset-level | Unknown | Unknown | Unknown | Unknown | No | Researcher preview |
| Esri ArcGIS AI assistants [E51] | Yes, for ArcGIS tasks | Via ArcGIS | No | Via layers | Yes | No | No | Partial (ArcGIS history) | No | Paid licence |
| NRSC Bhuvan chatbot proposal [E29, E56] | Yes, multilingual | Proposed | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Government infrastructure | Research proposal, not deployed |
| NRSC and NDEM flood maps [E3, E5, E6] | No (fixed products) | Yes, centrally | Yes (SAR preferred) | Yes | Yes | No (labelled "preliminary") | n/a | No | Government | Official agencies; not on demand |
| **SatClip (target)** | Yes, a fixed set of question types | Yes, three public STAC catalogues | **Yes** | **Yes** | **Yes** | **Yes, fitted and reported** | **Yes, with a "next pass" hint** | **Yes** | **Yes** | **Yes, open source, free data** |

"Unknown" means we found no public evidence either way. These cells will be revisited as the archive grows.

## 2. What is new, stated honestly

**Not new on its own.** Each of these exists in prior work:

- natural-language interfaces to remote sensing [A001 to A007];
- multi-sensor understanding including SAR [A002, A003, A021];
- tool-calling EO agents [A023, A024];
- SAR flood mapping [A022];
- cloud masking and SAR fallback (NRSC already prefers SAR for floods [E32]).

**New, as far as the archive shows so far:**

1. **Instruments answer, the language model only routes and explains.** Every number in a SatClip answer comes from a named, versioned, transparent instrument run on an identified scene. Generative model weights never produce it. RS assistants in the archive generate answers directly [A001 to A007, A025]. Agents call tools but pass free text back through the LLM, with no confidence carried through [A023, A024].
2. **The evidence card as the unit of answer.** One answer carries:
   - what the system understood;
   - scene IDs and dates;
   - the sensor, with automatic optical-or-SAR choice;
   - the mask;
   - calibrated confidence;
   - an observed-versus-inferred flag;
   - a receipt that re-runs to the same output hash.

   None of the archived systems return this bundle. The receipt and observed-versus-inferred parts answer the provenance and audit-trail call in [E39].
3. **Abstention as a designed outcome, with a constructive next step.** "Insufficient evidence, next Sentinel-1 pass on date X" replaces a guess. No archived RS assistant abstains.
4. **Ease of deployment.** The whole truth layer runs on CPU on free data with no training, and can run fully offline. That makes it deployable on district or state infrastructure today. Fine-tuning improves only the language layer.

The claim is novelty of **combination and packaging for a specific user**, which is what the user asked for ("innovative in how it solves the problem"). It is not a new model architecture.

## 3. What would have to be true for the claim to hold

| # | Condition | How we check it | Status |
|---|---|---|---|
| 1 | No published RS assistant already returns per-answer scene provenance plus calibrated confidence plus abstention | Keep searching the archive, especially trust-calibration, eo-agents and upcoming work (runs 2 onward) | Holds for 50 papers. The newest RS hallucination benchmark (Feb 2026) still evaluates free-text VLM answers with no abstention or provenance [A033]; to re-check |
| 2 | Instrument answers are accurate enough on Indian scenes to be useful at a reasonable coverage | M3 and M6: risk-coverage curves on a labelled Indian set | Not yet tested |
| 3 | Calibration fitted on public data transfers to India, or Indian labels can be gathered | M5 calibration fitting; report expected calibration error per zone | Not yet tested |
| 4 | Non-GIS users understand evidence cards and abstentions faster than maps or chat answers | M4 UX design; a small usability test with students or officers if possible | Not yet tested |
| 5 | Public STAC endpoints plus COG reads are fast enough for "minutes, not hours" on CPU | M2 and M6: measured latency per district-sized AOI | Not yet tested |
| 6 | Google Earth AI, Earth Copilot or the NRSC chatbot do not already ship this bundle in India | Re-check product pages each run | Holds as of 2026-10-04 [E49, E50, E56] |

### Run 2 evidence that strengthens or tests the claim

- **Calibration and abstention are mature in general ML but absent from RS assistants.** Temperature scaling [A026], selective classification with a guaranteed risk [A027], conformal sets [A028] and VQA abstention [A030] are well established. Conformal prediction has reached per-pixel RS classification [A032]. None of the archived RS assistants use any of them. SatClip's contribution is applying them per instrument and showing them to a non-expert, not inventing them.
- **The hallucination gap is now measured for RS VLMs.** RSHallu reports hallucination-free rates of roughly 36% to 69% for RS multimodal models [A033]. This strengthens the case for keeping generated text out of the number path.
- **Learned change models are no clear upgrade over a transparent instrument.** On Kuro Siwo, dedicated change-detection networks did not beat segmentation models given the full pre/post stack [A041], and learned optical change models swing widely across datasets [A038]. This supports transparent, calibrated instruments.
- **Official Indian practice already uses thresholding.** The NRSC flood atlas detects SAR water by variable thresholding [A046], and Indian case studies use Otsu on Sentinel-1 [A042]. SatClip's instruments are therefore familiar to official users; the new part is per-question, on-demand delivery with confidence and a receipt.
- **New risk to the claim:** strict risk targets can collapse coverage [A030]. The claim must be stated with its measured coverage, not just its risk.

## 4. Closest threats to the claim (watch list)

- **EarthDial** [A003] is the closest model: Sentinel-1 plus Sentinel-2 plus change, and open. If a follow-up adds confidence and abstention, our differentiation narrows to receipts, live data and ease of deployment.
- **NRSC's multilingual Bhuvan chatbot** [E29] targets the same users inside ISRO. If deployed, SatClip should position as its open, evidence-first engine rather than a rival.
- **Google Earth AI** [E49] has the data and the distribution. Its India availability must be tracked.
