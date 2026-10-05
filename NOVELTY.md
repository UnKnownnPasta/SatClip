# What is new in SatClip, and what would have to be true

This document is an honest comparison against the closest existing systems. It is checked against the archive as it grows: version 4 (run 4) covers 100 papers plus the competitor evidence in [docs/reference/problem-evidence.md](docs/reference/problem-evidence.md). A final pass against the whole archive is milestone M8.

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
| VHM [A078] | Yes | No | No | No | Boxes | No | **Partly: trained to refuse questions about absent objects (four question types); no threshold or score** | No | No (7B) | Open |
| EarthMind [A079], FUSAR-GPT [A082] | Yes | No | Reads SAR, no automatic choice; EarthMind's authors find the fused model nearly ignores SAR | No | Partial | No | No | No | No | Mostly open |
| Falcon [A080] | Task prompts | No | No | No | Masks | No | No | No | Plausible (0.7B) | Open |
| Change-Agent [A089] | Yes, change only | No | No | No | Change masks | No | No | No | No | Open code |
| Earth-Agent [A094] (ICLR 2026) | Yes | Via GEE products | No SAR | No | Via tools | No | No | No | No (cloud LLM) | Benchmark and code |
| Google Earth AI and Gemini geospatial reasoning [A095, E49] | Yes | Yes (Google data and models) | Not evaluated on SAR time series [A095] | No per-answer scene IDs found [A095] | Yes, on map | Confidence intervals on some model outputs, not on agent answers [A095] | No refusal behaviour described [A095] | No public evidence | No | US-gated paid tiers; not India |
| NASA and Microsoft Earth Copilot [E50] | Yes | NASA data | Unknown | Dataset-level | Unknown | Unknown | Unknown | Unknown | No | Researcher preview |
| Esri ArcGIS AI assistants [E51] | Yes, for ArcGIS tasks | Via ArcGIS | No | Via layers | Yes | No | No | Partial (ArcGIS history) | No | Paid licence |
| NRSC Bhuvan chatbot proposal [E29, E56] | Yes, multilingual | Proposed | Unknown | Unknown | Unknown | Unknown | Unknown | Unknown | Government infrastructure | Research proposal, not deployed |
| NRSC and NDEM flood maps [E3, E5, E6] | No (fixed products) | Yes, centrally | Yes (SAR preferred) | Yes | Yes | No (labelled "preliminary") | n/a | No | Government | Official agencies; not on demand |
| **SatClip (built, run 4)** | Yes, a fixed set of question types and 735 named districts | **Yes, live** (three public STAC catalogues, tested end to end) | **Yes** (monsoon rule, tested on live data) | **Yes** | **Yes** (per-tile PNG overlays clipped to the district) | **Model-based now** (propagated threshold error); fitting on labels is M5, and the card says so | **Yes, with a next step** | **Yes** | **Yes** (a whole district in about 30 s on CPU) | **Yes, open source, free data** |

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
3. **Abstention as a designed outcome, with a constructive next step.** "Insufficient evidence, next Sentinel-1 pass on date X" replaces a guess. Run 4 narrows this: VHM [A078] trains an RS VLM to refuse questions about objects that are not in the image, and GeoBenchX [A093] scores agents on refusing unsolvable tasks. Neither ties refusal to a confidence threshold over a measurement, reports coverage, or tells the user what would fix it. The claim is therefore "threshold-based abstention over a measured quantity, with a next step", not "the first RS system that refuses".
4. **Ease of deployment.** The whole truth layer runs on CPU on free data with no training, and can run fully offline. That makes it deployable on district or state infrastructure today. Fine-tuning improves only the language layer.

The claim is novelty of **combination and packaging for a specific user**, which is what the user asked for ("innovative in how it solves the problem"). It is not a new model architecture.

## 3. What would have to be true for the claim to hold

| # | Condition | How we check it | Status |
|---|---|---|---|
| 1 | No published RS assistant already returns per-answer scene provenance plus calibrated confidence plus abstention | Keep searching the archive, especially trust-calibration, eo-agents and upcoming work (runs 2 onward) | Holds for 100 papers, but narrower: instrument-grounded agents exist (Earth-Agent [A094], Change-Agent [A089], Google Earth AI [A095]) and learned refusal exists (VHM [A078]). None combines the four (instruments, per-answer scene provenance, confidence, threshold abstention), and none uses SAR for cloud |
| 2 | Instrument answers are accurate enough on Indian scenes to be useful at a reasonable coverage | M3 and M6: risk-coverage curves on a labelled Indian set | Not yet tested |
| 3 | Calibration fitted on public data transfers to India, or Indian labels can be gathered | M5 calibration fitting; report expected calibration error per zone | Not yet tested |
| 4 | Non-GIS users understand evidence cards and abstentions faster than maps or chat answers | M4 UX design; a small usability test with students or officers if possible | Not yet tested |
| 5 | Public STAC endpoints plus COG reads are fast enough for "minutes, not hours" on CPU | M2 and M6: measured latency per district-sized AOI | **First measurement holds:** Barpeta, 117 tiles, 2,335 sq km, 30.6 s from question to card on sandbox CPU (run 4). Repeat under load in M6 |
| 6 | Google Earth AI, Earth Copilot or the NRSC chatbot do not already ship this bundle in India | Re-check product pages each run | Holds as of 2026-10-04 [E49, E50, E56] |

### Run 2 evidence that strengthens or tests the claim

- **Calibration and abstention are mature in general ML but absent from RS assistants.** Temperature scaling [A026], selective classification with a guaranteed risk [A027], conformal sets [A028] and VQA abstention [A030] are well established. Conformal prediction has reached per-pixel RS classification [A032]. None of the archived RS assistants use any of them. SatClip's contribution is applying them per instrument and showing them to a non-expert, not inventing them.
- **The hallucination gap is now measured for RS VLMs.** RSHallu reports hallucination-free rates of roughly 36% to 69% for RS multimodal models [A033]. This strengthens the case for keeping generated text out of the number path.
- **Learned change models are no clear upgrade over a transparent instrument.** On Kuro Siwo, dedicated change-detection networks did not beat segmentation models given the full pre/post stack [A041], and learned optical change models swing widely across datasets [A038]. This supports transparent, calibrated instruments.
- **Official Indian practice already uses thresholding.** The NRSC flood atlas detects SAR water by variable thresholding [A046], and Indian case studies use Otsu on Sentinel-1 [A042]. SatClip's instruments are therefore familiar to official users; the new part is per-question, on-demand delivery with confidence and a receipt.
- **New risk to the claim:** strict risk targets can collapse coverage [A030]. The claim must be stated with its measured coverage, not just its risk.

### Run 3 evidence that strengthens or tests the claim

- **Human-factors research backs the evidence card over the chat answer.** Explanations raise acceptance of AI answers whether right or wrong [A067]; confidence display helps reliance match reliability but does not by itself raise accuracy [A070]; trust should be calibrated, not maximised [A065]; responders are limited by trust and workflow fit more than by algorithms [A069]. Fluent RS assistants optimise the very thing these studies warn about. The card-first design is a direct application, not a novelty of method.
- **The parser can be small.** Natural-language interfaces to data work by turning a question into an inspectable structured spec with ambiguity flags [A068]. SatClip's "I understood your question as" panel is the same pattern, which means a 256M to 2.2B open VLM [A063] with LoRA [A059, A060] is enough for the language layer.
- **EO foundation models are a threat and an ally.** Prithvi-EO-2.0, CROMA, SSL4EO-S12, DOFA and Clay [A052, A054 to A057] are open and Sentinel-native, but none ships a calibrated, abstaining, receipt-backed answer for a non-expert. They are best registered as instruments behind the same card. SkySense [A053] shows the accuracy ceiling of multi-modal fusion, but with non-commercial weights at billion-parameter scale.
- **Object counting stays out of scope.** Detection benchmarks are built on 0.3 m to 1 m imagery (DOTA, xView, DIOR [A071 to A073]); even there small objects are hard. Sentinel-1 ship detection (xView3-SAR [A075]) is the one object task native to our data and a candidate future instrument.
- **Data-layer ease is real but must be engineered.** Of three public catalogues, only some serve openly readable Sentinel-1 pixels (Earth Search S1 GRD is requester-pays; CDSE downloads need an account). SatClip's M2 data layer records which catalogue answered and why a scene was chosen, so this complexity never reaches the user.

### Run 4 evidence that strengthens or tests the claim

- **Instrument-grounded EO agents now exist, and they are the closest prior art.** Earth-Agent (ICLR 2026) [A094] calls 104 tools including NDVI and NDWI; Change-Agent [A089] uses a change model as its eyes and an LLM as its brain; Google Earth AI [A095] chains Google's imagery, population and flood models under a Gemini agent. SatClip's "instruments answer" is therefore not new as an idea. What stays new is what these agents lack: calibrated confidence on the answer, abstention below a threshold, scene IDs and dates on every answer, a re-runnable receipt, and SAR when clouds block optical.
- **Free-form tool agents get the parameters wrong.** Earth-Agent's GPT-5 matches expert tool parameters only about 26% of the time [A094]; on ThinkGeo, GPT-4o gets tool arguments right about a third of the time and the final answer right under 10% end to end [A092]; GeoGPT reports hallucinated tool and file arguments [A090]. A fixed router to versioned instruments with set parameters removes this whole failure class. This is the strongest published support so far for SatClip's ease claim.
- **VLMs still cannot be trusted to read SAR.** EarthMind's authors find the fused optical plus SAR model is nearly blind to the SAR input [A079]; FUSAR-GPT counts SAR targets correctly about 53% of the time [A082]; Geo-R1's SAR grounding is about 25% [A081]. Pixel-grounded RS VLMs reach about 52 mIoU on masks [A076]. SatClip's SAR answers stay instrument-only.
- **The SAR flood method SatClip uses is the operational one.** The DLR / Copernicus GFM chain is split-based tile selection plus a minimum-error threshold, with a fallback near -18 dB [A083 to A086]. SatClip implements the same family per tile, reports every threshold, and found on live Barpeta data that Otsu misplaces the threshold where Kittler-Illingworth does not.
- **The data supply keeps improving.** Sentinel-1C and 1D restore a two-satellite constellation with about 6-day revisit [A100]; NISAR adds free L-band and S-band SAR with provisional calibrated products since July 2026 [A098]. More passes mean fewer abstentions for lack of a recent scene.
- **A learned land-cover model was wrong, and the card abstained.** On live Sentinel-2 over Darbhanga (mostly cropland), RemoteCLIP [A008] labelled patches as grassland, forest and bare land with mean top probability 0.35, so the card abstained instead of publishing it. This is the design working, and a measured case for keeping learned models behind a confidence gate.

## 4. Closest threats to the claim (watch list)

- **Google Earth AI** [A095] is now the closest threat, not just a product page: same headline (plain-language land questions answered by chaining models), Google's data and distribution. Gaps today: no refusal behaviour described, no per-answer scene receipts, high-resolution RGB rather than SAR time series, small rubric-based evaluation, US-gated. If it adds abstention and provenance, SatClip's differentiation narrows to openness, offline deployment on Indian infrastructure, SAR-first monsoon handling and free data.
- **Earth-Agent** [A094] could add confidence and refusal with modest work. Watch for a follow-up.
- **VHM** [A078] shows honesty training for RS VLMs; a VHM-style model with calibrated scores would overlap with SatClip's abstention claim.

- **EarthDial** [A003] is the closest model: Sentinel-1 plus Sentinel-2 plus change, and open. If a follow-up adds confidence and abstention, our differentiation narrows to receipts, live data and ease of deployment.
- **NRSC's multilingual Bhuvan chatbot** [E29] targets the same users inside ISRO. If deployed, SatClip should position as its open, evidence-first engine rather than a rival.
- **Open EO foundation models with fine-tune recipes** [A052, A055, A057] could be wrapped by someone else into a non-expert assistant. Watch for a Prithvi or Clay based flood or crop chat tool with confidence output.
- **Google Earth AI** [E49] has the data and the distribution. Its India availability must be tracked.
