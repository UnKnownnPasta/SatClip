# What is new in SatClip, and what would have to be true

This document is an honest comparison against the closest existing systems. It is checked against the archive as it grows: version 9 (run 9) covers 225 papers plus the competitor evidence in [docs/reference/problem-evidence.md](docs/reference/problem-evidence.md). A final pass against the whole archive is milestone M8.

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
| RSure-Agent [A164] (2026 preprint) | Agent tasks | No | No | No | Via tools | **Per-tool reliability learned from past tasks, used inside the agent; not shown to users** | **Internal: rejects or asks for more evidence before using a tool output** | No | No (LLM agent) | Preprint |
| Selective tool use for change VQA [A172] (2026 preprint) | Yes, change questions | No | No | No | Via fixed change tools | No | No | No | Small (4B LoRA) | Preprint |
| ScaleEarth [A171] (2026 preprint) | Yes | No | No | No | No | Uncertainty on its resolution guess only | Falls back to a default resolution, never abstains on the answer | No | No | Preprint |
| GeoDisaster agents [A174] (2026 benchmark, IIT Bombay) | Yes, disaster questions incl. Sentinel-1 floods | Workflows over prepared data | Yes, in a SAR flood subset | Not per answer | Via workflows | No (authors list uncertainty as future work) | No | Runnable workflows | No | Benchmark |
| Earth-Agent-Pro [A166] (2026 preprint) | Yes | Via tools | Partial | No | Via tools | No | No | Evidence log for self-repair only | No | Preprint |
| QAG-360K / VisTA [A179] (2024 preprint) | Yes, change questions | No (bitemporal optical pairs supplied) | No | No | **Yes: a change mask with every answer, empty when nothing changed** | No | No | No | No | Test set on request |
| EO-Gym agent [A176] (2026 preprint) | Yes | Yes, inside its environment (fetches older scenes, switches optical to SAR) | **Yes, learned** | No | Via tools | No | No | No | Small (4B LoRA) | Preprint |
| TerraScope [A201] (CVPR 2026) | Yes | No | Reads optical or SAR, no automatic choice | No | **Yes, pixel masks behind area answers** | No | No | No | No (GPU) | Open per paper |
| SHRUG-FM [A202] (CVPR EarthVision 2026) | No (segmentation model) | No | No (Sentinel-2 optical) | No | Flood masks | **Reliability scores, stated as not calibrated** | **Rejects unreliable flood maps; no next step** | No | Not stated | Research code |
| UnivEARTH agents [A204] (ACL 2026 Findings) | Yes | **Yes, via Earth Engine code the agent writes** | Not automatic | No | Via code | No | No | No | No (cloud LLM) | Needs Earth Engine |
| OpenEarthAgent [A205] (ECCV 2026) | Yes | No | No | No | Via tools | No | No | **Deterministic replay of tool traces** | No | Open |
| **SatClip (built, run 9)** | Yes, a fixed set of question types and 735 named districts; Indian date formats and common Hindi and Hinglish words | **Yes, live** (three public STAC catalogues, tested end to end) | **Yes** (monsoon rule, tested on live data; water uses VV and VH since run 7) | **Yes** | **Yes** (per-tile PNG overlays clipped to the district) | **Fitted for water extent (Sen1Floods11) and water change (Kuro Siwo, one map per answer regime); crop change still a labelled placeholder** | **Yes, with a next step** | **Yes** | **Yes** (a whole district in about 40 to 60 s on CPU) | **Yes, open source, free data** |

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
| 1 | No published RS assistant already returns per-answer scene provenance plus calibrated confidence plus abstention | Keep searching the archive, especially trust-calibration, eo-agents and upcoming work (runs 2 onward) | **Holds for 175 papers (run 7).** The nearest 2026 work learns tool reliability inside an agent without showing it to users (RSure-Agent [A164]), abstains only on an internal resolution guess (ScaleEarth [A171]), or names uncertainty as future work (GeoDisaster [A174]). Earlier note, still narrower than run 1: instrument-grounded agents exist (Earth-Agent [A094], Change-Agent [A089], Google Earth AI [A095]) and learned refusal exists (VHM [A078]). None combines the four (instruments, per-answer scene provenance, confidence, threshold abstention), and none uses SAR for cloud |
| 2 | Instrument answers are accurate enough on Indian scenes to be useful at a reasonable coverage | M3 and M6: risk-coverage curves on a labelled Indian set | **Improved but not met (run 7).** Water v1.1 (VV or VH) publishes 43% of held-out chips with 26% wrong and 52% of Indian chips (fit without India) with 55% wrong; flood-change answers with real new water are right only 27% of the time on Kuro Siwo and now abstain. Run 6 status: **Fails for water today.** On 64 Indian Sen1Floods11 chips the VV-only water instrument has median IoU 0.03, and after calibration it publishes 12% of them with 62% wrong. The trust machinery works (it abstains), but usefulness needs instrument v1.1 with VH. Crop change not yet tested on labels |
| 3 | Calibration fitted on public data transfers to India, or Indian labels can be gathered | M5 calibration fitting; report expected calibration error per zone | **Partly (runs 6 and 7).** Run 7: India with a fit made without India, ECE 0.30 to 0.23 (v1.1); Kuro Siwo change maps cross-validated by event, ECE 0.041 with regime maps. Run 6: Fit on 312 chips worldwide: held-out ECE 0.30 to 0.09; unseen Bolivia 0.34 to 0.22; India with a fit made without India 0.50 to 0.36. Calibration transfers to unseen chips of known events but degrades on new regions, as dataset-shift work predicts [A132], so per-region refits are needed |
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

### Run 5 evidence that strengthens or tests the claim

- **Benchmarks keep confirming the core design choice.** On DisasterM3, general and RS VLMs are near chance at counting damaged buildings and get worse when the post-disaster image is SAR [A118]. On XLRS-Bench, the best MLLMs average about 40% on four-option questions over huge scenes and almost never draw a correct box [A117]. EarthVQA finds counting and comprehensive analysis far weaker than yes/no judging even with masks as input [A115]. Measuring with instruments and letting language only phrase the result remains the safer design.
- **Foundation models do not beat simple supervised baselines on flood water.** On PANGAEA's Sen1Floods11 task a plain UNet outperforms every geospatial foundation model, and RemoteCLIP reaches about 55 water IoU [A120]; GEO-Bench also found RS pre-training often fails to beat ImageNet weights [A119]. This supports keeping SAR thresholding as the water instrument and keeping RemoteCLIP experimental (risk 10 in SOLUTION.md is not yet materialising).
- **The data-layer ease is not unique and should not be claimed as such.** openEO (now an OGC Community Standard) [A121] and odc-stac [A125] already turn STAC searches into district-clipped cubes. SatClip's novelty is above that layer: the question-to-card contract, calibrated abstention and receipts for a non-expert. We should reuse these tools where they fit and record an openEO-style process graph in the receipt.
- **The method lineage is decades old, which is a strength.** Minimum-error thresholding [A109], Otsu [A108], NDWI [A110], NDVI [A111], Lee speckle filtering [A113], change vectors [A114] and the reject option [A112] are well understood and explainable to an auditor. The new part is packaging them behind a plain question with a calibrated, abstaining, receipt-backed answer.
- **Official Indian products still publish headline numbers without uncertainty.** A peer-reviewed Assam 2022 Sentinel-1 study reports a flooded area of about 33,900 sq km with no stated uncertainty [A105]; the NRSC atlases are multi-year syntheses, not answers to today's question [A046, A106]. This gap is exactly what the evidence card fills.
- **Live check, run 5.** The web UI ran end to end on live data: Barpeta flood extent (published, 0.66, just above the 0.60 line), Barpeta flood change June to July 2024 (abstained at 0.56, shown with its map), Darbhanga crop change March to April 2024 (published, 0.89, with the caveat that harvest also lowers greenness), and an ambiguous "Aurangabad" (two one-tap choices, nothing measured). A live search on 6 October 2026 also returned Sentinel-1D scenes over Barpeta, so the restored constellation [A100] is already in the catalogue.

### Run 6 evidence that strengthens or tests the claim

- **Calibration is what makes the abstention claim real, and it changed the product.** Fitting the water confidence on Sen1Floods11 hand labels showed that the uncalibrated score would have published most answers with a majority of them wrong; after fitting, the live Barpeta flood card abstains (0.46) instead of publishing (0.66). None of the RS assistants or agents in the archive reports a reliability diagram or a risk-coverage curve for its answers [A001 to A007, A094, A095]. Fitting on the production code with a published report and a per-region ledger is part of the claim now, following classic calibration practice [A126, A127, A128] and shift testing [A132].
- **The cost: today SatClip is honest but rarely useful for Indian floods.** The novelty claim is about a trustworthy answer at a useful coverage; the run 6 numbers meet the first half and miss the second (SOLUTION risk 15). This is the most important open problem in the project.
- **Learned change detectors do not threaten the instrument choice at 10 m.** The best FC-Siam F1 on Sentinel-2 OSCD is about 58 [A142]; ChangeFormer's 90 F1 is on very high resolution LEVIR-CD [A143]; zero-shot AnyChange has 4% to 31% pixel precision [A144]. Classical difference-image thresholding with an EM posterior [A140] stays the better fit for an auditable, calibrated card.
- **Human factors work supports the card design and adds two concrete rules.** Explanations reduce overreliance only when they make checking cheaper [A137]; countable uncertainty displays beat densities on phones [A135]. Satellite emergency mapping today is delivered as expert map products [A138], which confirms the gap between existing services and a non-expert asking a question.
- **The language layer is measurable and the baseline is weak.** The rule parser's full-match rate is 0.16 on held-out districts (0.08 in Hindi). A small LoRA model constrained to a five-key JSON [A149, A150] is a plausible fix, but the claim does not depend on it: the parser only affects the "I understood" step, which the user can correct.

### Run 7 evidence that strengthens or tests the claim

- **The 2026 frontier is moving toward SatClip's architecture, not past it.** Models that route to fixed tools (More with Less [A170], selective tool use [A172], GeoDisaster [A174], Earth-Agent-Pro [A166]) are now common. That validates "the model routes, the instrument measures" and means the claim cannot rest on tool use. What still separates SatClip is what the user receives: per-answer scene IDs and dates, a calibrated probability, threshold abstention with a next step, and a receipt.
- **The closest new work is about reliability inside the agent.** RSure-Agent [A164] shows tool outputs are wrong in at least 22.7% of tool-dependent tasks even when the tool runs, and learns per-tool reliability to accept, ask or reject. It does not show a calibrated probability per answer to the user, and it reports no scene receipts. SatClip's Kuro Siwo result is the same lesson measured on a physical instrument, and it is why reliability is learned per instrument and per answer regime.
- **Answer quality is capped by the instrument [A172], which is also SatClip's main weakness today.** Water v1.1 answers about four times as many held-out chips at the 0.60 line as v1.0, with fewer wrong, but Indian chips stay hard, and positive change answers mostly abstain. The novelty claim is unaffected (the card behaves as designed); the usefulness claim (condition 2) is still the open problem.
- **Foundation models now target the beachhead tasks directly.** Galileo [A153], AnySat [A154] and Copernicus-FM [A155] cover flood and crop tasks with SAR and optical inputs; TESSERA ships open yearly embeddings [A152]; SoftCon gives small SAR encoders [A156]. None has a question interface, receipts, calibration or abstention, so they fit as calibrated second-opinion instruments behind the card, not as competitors to it.
- **Benchmarks keep exposing priors.** VRSBench answers are 83% "yes" among yes/no questions (measured in run 7), and the 2026 agent benchmarks [A166, A174] grade answers with an LLM judge, which adds its own error. SatClip reports its numbers against non-learned baselines and hand-written test sets for the same reason.
- **New data for honest evaluation.** GEOID-Flood [A173] separates permanent water from flood water across 219 events, with a held-out set from after January 2026; it is the next external test for the water instruments, although mostly European.

### Run 8 evidence that strengthens or tests the claim

- **Grounded change answers are no longer new on their own.** QAG-360K and its VisTA model [A179] already answer plain-language change questions with a pixel mask, and expect an empty mask when nothing changed. CDVQA [A178] shows learned models answer change-ratio questions badly (about 39% right), which supports computing ratios from masks. SatClip's claim must therefore rest on the combination: calibrated per-answer confidence, threshold abstention with a next step, Sentinel-1/2 scene IDs and dates, a re-runnable receipt, SAR-first monsoon handling, and delivery to non-experts for Indian districts. No archived system has more than two of these.
- **Small tuned models that choose tools and switch to SAR now exist.** EO-Gym [A176] trains a 4B LoRA model to fetch older scenes and move from optical to SAR, beating a frontier model; RS-Agent [A195] and CangLing-KnowFlow [A194] show that classifying the task first and following expert workflow templates gives over 95% planning accuracy. This validates SatClip's closed set of question types and code-chosen sensors, and removes "automatic SAR fallback" as a distinguishing claim by itself. None of them reports calibrated confidence or abstains.
- **Numbers are where agents fail.** TerraBench [A177] finds the best agent gets only 22.9% of numeric answers within tolerance, and wrong argument values are the top failure; JL1-CC&QA [A182] finds judges reject invented exact percentages. Both support SatClip's rule that numbers come only from instruments and that parsed arguments are checked in code.
- **The field's own agenda matches SatClip's design.** A 2026 position paper on agentic remote sensing [A193] asks for projection, time window, provenance and an uncertainty measure to be carried through every step, using flood area as its example, but offers no system, calibration method or abstention rule. SatClip is a working instance of that agenda.
- **SAR VLMs still misread radar [A180, A192].** Even after heavy tuning, general VLMs need large SAR corpora, and a lightweight S1/S2 adaptation reaches only 0.77 F1 on per-patch flood calls with no area or confidence [A192]. This supports keeping the VLM away from backscatter.
- **Better physics exists for the weak instrument.** The Copernicus GFM Bayesian datacube method [A187] gives a per-pixel posterior water probability against each pixel's own seasonal history, plus a no-sensitivity mask, and a DEM input lifts flood F1 [A186]. Both are the concrete next steps for SOLUTION risk 15; neither is a question-answering system.
- **Reproducibility is now demonstrated, not only designed.** M6 re-ran every demo receipt from a cold start and found two defects (non-deterministic decimated reads and silent tile drop-outs) before fixing them (docs/QUALITY.md). The receipt claim is the only one in the comparison table that no other system even attempts, so its being measured matters.

### Run 9 evidence that strengthens or tests the claim

- **Abstention for flood maps now has published prior art.** SHRUG-FM [A202] (CVPR EarthVision 2026) flags unreliable foundation-model flood predictions (Sentinel-2, optical) using input out-of-distribution scores and prediction uncertainty, and rejects them. Its scores are explicitly not calibrated, it answers no questions and gives no next step. SatClip's abstention claim is therefore narrowed again: "abstention over a calibrated measurement of a user's question, with a next step and a receipt", not "the first EO system that rejects outputs".
- **Live retrieval by an LLM agent is not new on its own.** UnivEARTH [A204] (ACL 2026 Findings) has agents write Google Earth Engine code that fetches real imagery; the best agent reaches about 40% zero-shot and 64.5% with self-debugging, with no abstention or calibration. This supports SatClip's fixed instrument recipes and removes "fetches live data" as a standalone differentiator.
- **Deterministic re-runs of tool traces exist.** OpenEarthAgent [A205] (ECCV 2026) replays tool traces and computes NDVI, NBR and NDBI change. It overlaps SatClip's receipt and index-change ideas, but carries no confidence, no abstention, no scene search and no SAR. The receipt claim becomes "a receipt tied to Sentinel scene IDs whose re-run is measured to reproduce the same output hash", which M6 demonstrated.
- **Pixel-grounded area answers exist.** TerraScope [A201] (CVPR 2026) answers area and change questions backed by masks from optical or SAR. It needs a GPU and has no calibration, provenance or abstention. Masks on their own are not a SatClip novelty.
- **Faithful, step-grounded reasoning exists.** RSThinker [A206] (ICLR 2026) ties each reasoning step to an image box. SatClip should not claim auditable reasoning in general, only auditable measurement.
- **The research agenda names SatClip's features but does not build them.** ANASSA [A207] lists provenance, uncertainty and an "insufficient evidence" outcome as requirements without an implementation; the 2026 reasoning survey [A209] finds no RS reasoning system that evaluates calibration or abstention and no validated operational deployment. Being a working, measured system is part of the claim.
- **VLM self-reported confidence cannot replace instrument calibration.** A 2026 study [A224] finds VLM verbal confidence barely changes when the evidence changes. RSHBench [A203] measures 47% to 61% hallucination in RS VLM answers. Both support keeping the confidence meter tied to fitted instrument calibration, never to the language model.
- **Stronger trust tools are available to adopt.** Risk-controlling prediction sets [A218], conformal segmentation [A219] and conformal risk control over tool chains [A225] give finite-sample guarantees that SatClip's Platt maps do not. They are an upgrade path, not a threat: none is packaged with Sentinel provenance for non-experts.

## 4. Closest threats to the claim (watch list)

- **SHRUG-FM [A202] plus a question interface.** It already rejects unreliable flood maps; calibrated scores and a plain-language front end would make it a direct competitor for flood extent.
- **UnivEARTH-style agents [A204] with abstention.** Live retrieval through Earth Engine plus a refusal rule would overlap; watch for follow-ups.
- **TerraScope [A201] or OpenEarthAgent [A205] adding confidence.** Either has most of the plumbing.

- **VisTA / QAG-360K [A179] with confidence.** It already returns a change mask with each answer; adding a calibrated score, abstention and Sentinel provenance would make it a direct competitor for change questions.
- **EO-Gym [A176] with calibrated answers.** It already does the sensor switching and scene fetching; a reliability head would overlap strongly.

- **A calibrated RS VLM.** Conformal risk control [A133] and local temperature scaling [A131] are general tools; an RS VLM that ships with them and per-answer scene provenance would overlap strongly with SatClip. None found as of run 7; ScaleEarth [A171] is the first 2026 RS model seen to abstain on calibrated uncertainty, but only for its own resolution estimate.
- **RSure-Agent [A164] with a user-facing confidence.** If its learned per-tool reliability were turned into a per-answer probability with scene provenance, it would overlap with SatClip's trust claim. Watch for a follow-up or code release.
- **GeoDisaster [A174] adding uncertainty-aware answers**, which its authors list as future work; it already has a Sentinel-1 flood subset and Indian authors.
- **openEO and odc-stac based assistants** [A121, A125]: anyone could put a chat front end on these. Watch for one that adds confidence and abstention.

- **Google Earth AI** [A095] is now the closest threat, not just a product page: same headline (plain-language land questions answered by chaining models), Google's data and distribution. Gaps today: no refusal behaviour described, no per-answer scene receipts, high-resolution RGB rather than SAR time series, small rubric-based evaluation, US-gated. If it adds abstention and provenance, SatClip's differentiation narrows to openness, offline deployment on Indian infrastructure, SAR-first monsoon handling and free data.
- **Earth-Agent** [A094] could add confidence and refusal with modest work. Watch for a follow-up.
- **VHM** [A078] shows honesty training for RS VLMs; a VHM-style model with calibrated scores would overlap with SatClip's abstention claim.

- **EarthDial** [A003] is the closest model: Sentinel-1 plus Sentinel-2 plus change, and open. If a follow-up adds confidence and abstention, our differentiation narrows to receipts, live data and ease of deployment.
- **NRSC's multilingual Bhuvan chatbot** [E29] targets the same users inside ISRO. If deployed, SatClip should position as its open, evidence-first engine rather than a rival.
- **Open EO foundation models with fine-tune recipes** [A052, A055, A057] could be wrapped by someone else into a non-expert assistant. Watch for a Prithvi or Clay based flood or crop chat tool with confidence output.
- **Google Earth AI** [E49] has the data and the distribution. Its India availability must be tracked.

## Run 9 summary of the claim

After 225 papers, every single ingredient of SatClip exists somewhere: masks with answers [A179, A201], SAR switching [A176], live retrieval [A204], deterministic replays [A205], flood-map rejection [A202]. No archived system combines more than two of: calibrated per-answer confidence, threshold abstention with a next step, Sentinel scene receipts that are measured to reproduce, SAR-first monsoon handling, CPU or offline deployment, and plain-language delivery for Indian districts. The claim stands as a combination claim, and as the only one shown working end to end on live data with measured calibration.
