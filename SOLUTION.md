# SatClip: the solution thesis

Version 1.6 (run 7, 2026-10-07): water instrument v1.1 with VH, the change instrument's own calibration, and a harder test of the question parser (sections 4, 6 and 9). Version 1.5 (run 6) added the first fitted calibration.

> **In one line:** SatClip answers plain-language "what happened here, and when" questions about Indian land with an **evidence card**: a measurement taken from the actual Sentinel scene by a transparent instrument, a map of where it applies, the scene IDs and dates used, a calibrated confidence, and a receipt that lets anyone re-run it. When the evidence is not good enough, it says so and tells you what would fix it.

Citation keys:

- `[A003]` is archive entry 003 in [archive/papers](archive/papers/).
- `[E12]` is claim 12 in the [problem evidence brief](docs/reference/problem-evidence.md), where each claim links to its source.

This document refines the submitted idea deck (summarised in [docs/reference/deck-notes.md](docs/reference/deck-notes.md)). Where the evidence pushed us to change the deck's design, we say so explicitly (section 8).

---

## 1. Whose problem

### Primary users: people who decide at district level and must answer "where and how bad" questions quickly

| User | The question they actually have | What they do today |
|---|---|---|
| District disaster officials (DDMA, District Magistrate's office, state relief commissioner staff) | "Which villages in my district are under water since Tuesday, and is it spreading?" | Wait for centrally produced NRSC maps through NDEM or Bhuvan [E3, E7]. In 2024 there were about 300 flood products for the whole country [E2], and turnaround varied from the same day to two days [E5, E6]. Otherwise they rely on field reports. |
| Agriculture and crop-insurance officers (PMFBY, YES-TECH) | "Did the crop in these blocks actually suffer between sowing and harvest?" | Crop cutting experiments, which a parliamentary committee called slow and labour-intensive [E11]. Satellite yield models whose outputs farmers dispute without an independent check [E16]. Claims have stayed pending partly because data arrived late [E13]. |

Run 5 adds the official channels these users already work in. NRSC flood maps reach district managers through NDEM [A102] and Bhuvan [A101]; NRSC's Assam flood hazard atlas classifies every 50 m pixel by how often it flooded in 26 years [A106]. For agriculture, YES-TECH makes satellite-derived yields count for 30% of PMFBY loss assessment and lists Sentinel-1 and EOS-04 among its inputs [A103], and FASAL already judges satellite crop estimates against government statistics by district-level deviation [A104]. SatClip therefore complements these channels: it answers the question asked today, in their vocabulary, with a receipt, and exports layers they can overlay.

### Secondary users: people who must verify a claim about a place and date

| User | The question they actually have | What they do today |
|---|---|---|
| Journalists and fact-checkers | "Was this area really flooded, burned or cleared on the date this viral post claims?" | Free tools such as EO Browser, which assume the user knows which sensor and band to use. Earth Engine needs code [E18]. Synthetic imagery now makes up a real share of their fact-checks [E19]. |
| Urban and town planners, researchers without GIS training | "How much has built-up area grown around this town since 2020?" | Hire or borrow GIS help. 65% of urban settlements have no master plan, and planner posts are badly understaffed [E17]. |

### Beachhead

We start with **monsoon flood and crop-condition questions at district level**. Three reasons:

1. Here the cost of a slow or wrong answer is highest.
2. Here optical imagery fails most often [E30, E31].
3. Here the method is most mature, through SAR water detection [A022] and spectral indices.

Every other use is the same machinery pointed at a different instrument.

---

## 2. Why the problem is real and lasting

The problem is structural, not a temporary gap waiting for a better model.

1. **Questions are local and constant; answers are produced centrally.** India has over 700 districts, and every flood season brings thousands of local questions. The central system produces a few hundred map products a year [E2], with no published delivery time [gap noted in the evidence brief]. Even excellent central mapping cannot answer each official's own polygon and dates on demand.
2. **The skills gap is large and slow to close.** India's own task force counted roughly 25,000 to 50,000 trained geospatial users against a need of about 500,000 more [E21, E22]. It also said decision-makers in particular need basic orientation [E23]. Training programmes are large but cannot turn every officer into an analyst [E27]. NRSC researchers themselves have proposed a chatbot for non-GIS users of Bhuvan [E29], which confirms the need from inside ISRO.
3. **The monsoon returns every year, and so do the clouds.**
   - Cloud cover is above 60% over most of India from June to September [E30].
   - In the Western Ghats it reaches about 90% in July and August, and optical water maps miss about a quarter of surface water there [E31, A045].
   - NRSC itself prefers radar for floods [E32].

   Any optical-only tool fails exactly when it is needed most.
4. **Fluent AI makes the trust problem worse, not better.**
   - General multimodal models caption imagery well but localise and count badly. GPT-4V scored about 0.16 mIoU on localisation [A013]. The best open VLM scores around 42% on a geospatial multiple-choice benchmark [A014].
   - Remote sensing VLMs that emit boxes in text get low grounding accuracy [A001, A012].
   - The UN space office now calls for provenance, metadata and audit trails on AI-derived EO products [E39].

   As answers become easier to generate, the scarce thing becomes answers that can be checked.
5. **The data supply is free, open and secured for years.**
   - Copernicus data are free and open [E41].
   - Sentinel-1C and 1D restored a 6-day radar revisit [E42, E43].
   - Three public STAC catalogues index the archive [E45 to E47].

   The bottleneck is not data, it is the last step from data to a trusted answer.

---

## 3. How SatClip solves it

### The core idea: instruments answer, the language model only asks and explains

The deck put a fine-tuned vision-language model at the centre, generating the answers. The evidence says that is backwards for the users we serve [A001, A012, A013, A014]. SatClip inverts it.

```
"Was Barpeta flooded after 2 July compared to mid June?"
        |
  (1) Understand  ->  {place: Barpeta district, dates: [2026-06-10..20], [2026-07-02..06],
                       question: water_extent_change}
                       shown back to the user: "I understood: water extent change in Barpeta, ..."
        |
  (2) Find evidence -> STAC search (CDSE / Earth Search / Planetary Computer)
                       optical if cloud-free over the AOI, else Sentinel-1 SAR (automatic)
        |
  (3) Measure      ->  a named, transparent instrument per question type
                       (SAR water threshold + log-ratio change; NDWI / NDVI deltas;
                        RemoteCLIP zero-shot land cover; built-up index ...)
        |
  (4) Check        ->  calibrated confidence per tile; abstain if below threshold,
                       if cloud and no SAR, or if the question is out of scope
        |
  (5) Answer       ->  EVIDENCE CARD:
                       "About 312 sq km newly under water (confidence 0.86)"
                       + map mask + scene IDs + acquisition dates + sensor
                       + what was observed vs inferred + receipt (JSON to re-run)
```

### The five deck tasks, each mapped to an instrument

| Deck task | What SatClip does | Instrument (prototype, CPU) |
|---|---|---|
| Change detection (headline) | Measures what changed, where, between two dates, with an area figure and mask | Sentinel-1 log-ratio with an automatic two-class threshold whose fitted posterior gives the confidence [A036, A140], calibrated on Kuro Siwo [A041] and Sen1Floods11 [A022]; crop change compared with the change expected for the season, since normal phenology looks like loss [A145]; learned detectors (FC-Siam, ChangeFormer, AnyChange) only as proposals or cross-checks, because their 10 m Sentinel accuracy is far below their high-resolution benchmark scores [A142, A143, A144]; optical change vector analysis or index differencing calibrated on OSCD [A034, A035]; cloud mask decides the sensor [A019] |
| Scene classification | Labels land cover for the area, with calibrated probabilities | Built in run 4 as an **experimental** instrument: RemoteCLIP zero-shot [A008] over sub-patches. On live Darbhanga data it mislabelled cropland and the card abstained (confidence 0.35). Next candidates: a BigEarthNet-trained S1/S2 classifier [A017], TerraMind [A097] or AlphaEarth embeddings [A096] with a small labelled head |
| VQA | Answers only questions that break down into measurable instruments (presence, extent, area, change, trend). Anything else is declined. | Router plus instruments; never free-form generation of numbers |
| Captioning | A short description, clearly labelled as a description, not a measurement | Built in run 4 as `index_caption`: shares of water, dense and sparse vegetation and other surfaces from NDWI and NDVI, written from a template, so it cannot hallucinate. A VLM caption later [A004, A025, A080], checked against these shares |
| Object detection | Limited to what 10 m data supports (large water bodies, ships in SAR, large structures). Very high resolution counting is out of scope. | Deferred to M3 evaluation; flagged honestly |

### Where the fine-tuned VLM fits

The LoRA-tuned open VLM from the deck stays in the plan (M5) and does three jobs:

- better question understanding, including Indian place names and mixed-language queries;
- richer captions;
- explanations of the evidence card.

It is evaluated against the instruments and is never the source of a number. EarthDial was the first base candidate [A003], because it already handles Sentinel-1 and Sentinel-2. **As built (run 6, M5):** the pipeline defaults to Qwen2-VL-2B-Instruct [A149] with LoRA or QLoRA on the language side only, because it is small enough for a free T4 and a state CPU server, handles any image size natively, and the job is language, not pixels; DoRA is a switch [A148], and the merged model can be quantised with GPTQ or AWQ [A146, A061] after checking that 8-bit stays lossless [A147]. The model's whole output is a five-key JSON that the deterministic gazetteer and date code resolve, so a parsing mistake can only cost an "I understood" correction. Radar reaches the model as a fixed-stretch VV, VH, VV-minus-VH false colour, so the same backscatter always looks the same.

Run 3 adds a second, CPU-first track. Fully open small VLMs in the 256M to 2.2B range (SmolVLM [A063]) are the realistic base for the parser and explainer on a laptop or a state server. LoRA keeps base weights frozen and versioned, and merged adapters add no inference latency [A059]; QLoRA lets the fine-tune fit on one free-tier GPU [A060]; 4-bit weight quantization shrinks the merged model further [A061]. Because the VLM only parses and explains, a small model is enough: it never has to see the whole scene or produce a measurement.

Open EO foundation models (Prithvi-EO-2.0 [A052], CROMA [A055], SSL4EO-S12 [A054], DOFA [A056], Clay [A057]) are the right tool for a *learned second opinion* next to an instrument, for example a CROMA-based SAR water head checked against the Otsu mask. They are not the default path, because they still need labelled fine-tuning per task and most are GPU-sized. Where the second opinion disagrees with the instrument, the card lowers its confidence or abstains.

---

## 4. Why it is easier (the innovation)

The innovation is **ease**. SatClip does not have a better model. It has a shorter, more checkable path from a question to an answer someone can act on.

1. **Easier for the user.**
   - **No GIS knowledge needed.** No sensor choice, band math, downloads or projections.
   - **One question, one card.** The card shows what it understood, so misreadings are caught in one glance.
   - **Clouds handled automatically.** The user never has to know that radar exists [E32].
2. **Easier to trust.**
   - The answer comes with its own evidence: scene IDs, dates, mask and confidence.
   - It comes with its own receipt, so a supervisor, auditor or journalist can re-run it and get the same number.
   - That is far simpler than deciding whether to believe a fluent paragraph [E39].
3. **Easier to build and run.**
   - Day-one value needs **no training at all**. The instruments are physics-based or pretrained, everything runs on CPU, and the data is free [E41, E45 to E47].
   - The expensive part, fine-tuning, improves the language layer, not the truth layer. The system is useful even if fine-tuning never happens.
4. **Easier to extend.**
   - A new question type is a new instrument plus a calibration set, not a new model.
   - Tool-using EO agents lose reliability as tool chains get longer [A024]. SatClip keeps plans short and fixed: one question type, one instrument recipe.
   - Run 4 measured how large that loss is. Free-form agents pick the right tool parameters only about 26% (Earth-Agent with GPT-5 [A094]) to 35% (ThinkGeo with GPT-4o [A092]) of the time, and ThinkGeo's end-to-end answers are right under 10% of the time. A fixed router to versioned instruments with set parameters cannot make that error.
   - Run 7 adds 2026 evidence that the field is converging on this design. In an emergency-operations benchmark, 13 frontier LLMs often chose the wrong sensor, and handing them the correct tool order helped by only 1 to 4 points [A165]; SatClip picks optical or SAR in code. Earth-Agent-Pro now restricts planning to expert-written skills, still reaching only about 66% with GPT-5 [A166]. A 2026 change-VQA agent that calls fixed rule-based tools answers proportion questions almost perfectly on ground-truth maps but only 63% to 66% on model-made maps [A172]: answer quality is capped by the instrument, which is why SatClip calibrates and abstains per instrument rather than trusting the chain.

Compared with existing approaches:

- **RS VLMs** (GeoChat, EarthGPT, EarthDial, TEOChat [A001, A002, A003, A007]) answer from model weights. Their answers carry no scene ID, date, calibrated confidence or abstention.
- **Agent frameworks** [A023, A024, A089, A094] chain tools, including real spectral instruments, but neither carry confidence through nor abstain, and none uses SAR when clouds block optical.
- **Commercial assistants** (Google Earth AI [A095], Earth Copilot, ArcGIS assistants) are gated by region, licence or invitation [E49 to E51]. Google's published Earth AI system describes no refusal behaviour and attaches no scene IDs to agent answers [A095].

SatClip's contribution is the combination, packaged for a non-expert: an evidence card with abstention, built on free data and running on CPU or offline. See [NOVELTY.md](NOVELTY.md) for the honest comparison.

---

## 5. How it scales

| Dimension | Design choice |
|---|---|
| Data | No bulk download. STAC search plus Cloud-Optimised GeoTIFF windowed reads fetch only the pixels inside the AOI. Three interchangeable public catalogues, with failover between them. |
| Compute | Each AOI is split into fixed tiles. Each tile-date-instrument job is independent and runs on a CPU worker. Results stream back tile by tile. Workers scale horizontally behind a queue. |
| Caching | Results are keyed by (tile, scene ID, instrument version). Two officials asking about the same district on the same day cost one computation. Popular districts in flood season are naturally hot in the cache. |
| Users | A stateless API: any replica can serve any request. User state lives only in the query and its receipt. |
| Regions | The instruments are mostly physics-based (backscatter, spectral indices), so they transfer across regions better than learned models. Thresholds and calibration are fitted per agro-climatic zone as labelled data accumulates. |
| Languages | The question is parsed into a small structured query, so supporting a new language means supporting parsing plus templated answer rendering. It does not need a new model that generates answers. The numbers never pass through translation. |
| Deployment | The same containers run on a laptop, a state data centre or ISRO infrastructure. A local STAC mirror plus local models allow fully offline operation (the deck's sovereignty goal). |

---

## 6. Why it can be trusted

1. **Grounding.** Every answer names its scene IDs, acquisition dates, sensor and AOI mask. Nothing is said about a place without an observed scene behind it.
2. **Observed versus inferred.** Pixels filled in by cloud-removal models are never presented as observed [A019, A020]. The card marks them, or the system switches to SAR.
3. **Calibration.**
   - Each instrument's raw score is mapped to a probability using a held-out labelled set, starting from public data such as Sen1Floods11 [A022] and SEN12MS-CR [A019], and moving to Indian labelled events as they are collected.
   - The mapping is temperature or Platt scaling, checked with expected calibration error and reliability diagrams [A026]; zero-shot CLIP scores need it too [A031]. Category answers and per-pixel masks can use conformal sets, abstaining when a set contains contradictory labels [A028, A032].
   - Calibration error is reported, not assumed.
   - **As built (run 4):** before any labelled fit, each area instrument computes a model-based confidence: the probability that its area is within plus or minus 20% if its threshold is off by a stated error (1 dB for SAR, 0.05 for NDVI), from the share of pixels near the threshold. Tile errors are summed for the district total, assuming full correlation (the conservative case). The calibration files are identity maps marked "not yet fitted", and every card prints that status. M5 replaces them with isotonic fits on labelled data.
   - **Fitted (run 6, M5).** The water instrument is now calibrated on the 446 hand-labelled Sen1Floods11 chips [A022], using the production code itself, with the event the card claims ("area within 20% of the reference map") as the label. Platt scaling [A126] beat isotonic regression [A127] on the valid split and was kept; ECE and MCE [A128] are reported on a held-out split, an unseen country (Bolivia) and a leave-India-out fit, as dataset-shift work says a single in-distribution number is not enough [A132]. Result: the uncalibrated score was badly overconfident (it would have published 79% of held-out chips with 55% wrong); after the fit, ECE fell from 0.30 to 0.09 and the card publishes 11% of chips with 33% wrong, abstaining on the rest. The flood-change instrument borrows the water map until it has its own labels, and its card says "borrowed". Next steps from the archive: ensembles of instrument variants (threshold, polarisation, filter) to widen ranges [A129], naming the type of uncertainty in the abstention message (sensor noise versus untested region) [A130], spatially varying calibration that never edits the mask [A131], and conformal risk control to bound the share of truly flooded area missed [A133].
   - **Run 7: VH, a refit, and a calibration per answer regime.** Water v1.1 adds a VH rule (water if VV or VH is below its own fitted threshold, bounds chosen on the Sen1Floods11 train split only). On the untouched test split the share of chips within 20% rose from 0.44 to 0.55, ECE after fitting from 0.088 to 0.074, and the card now answers 43% of chips (was 11%) with 26% wrong (was 33%); Bolivia went from answering none to answering 43% with none wrong. India stays weak: with a fit that never saw India, 55% of published Indian chip answers are wrong. The change instrument now has its own calibration from Kuro Siwo [A041] (848 samples, 22 events, cross-validated by event). Its raw score barely ranks right from wrong (AUROC 0.52) because "no meaningful new water" answers (68% right) and "X sq km of new water" answers (27% right, mostly undercounts) are mixed, so it ships one map per answer regime (ECE 0.041 against 0.214 for the borrowed map). This is the same lesson RSure-Agent reports for EO agents: tools that run without error are still wrong often enough to matter (at least 22.7% of tool-dependent tasks), so each tool's reliability has to be learned, not assumed [A164].
4. **Abstention.** This is the classic reject option: Chow showed in 1970 that refusing to decide on low-confidence cases trades a small loss of coverage for a large drop in error [A112]. Below a threshold, or with cloud and no SAR, or for an out-of-scope question, the answer is "insufficient evidence". It also names the next useful pass, for example "next Sentinel-1 pass over this AOI: 9 July". The threshold is chosen on a risk-coverage curve for a target error rate [A027] and published together with the resulting coverage, because strict risk targets can leave very few questions answered [A030].
5. **Explanations never add persuasion.** In human-AI studies, explanations made people accept AI answers more often whether the answer was right or wrong [A067], and showing a confidence score improved how well people's reliance matched the AI's reliability without, by itself, raising joint accuracy [A070]. Trust should match capability, not be maximised [A065]. So the card leads with the map, the scenes and a plain confidence band; generated prose is short, optional and checked against the card (risk 9).
6. **Auditability.** Each answer has a receipt: query, parsed intent, scene IDs, instrument name and version, parameters, and the output hash. Re-running the receipt reproduces the answer. Run 5 adds a check against the CEOS-ARD Normalised Radar Backscatter checklist [A122]: the receipt should state which ARD layers the radar source supplied (Planetary Computer RTC ships only VV and VH, with no layover, shadow or incidence-angle layers [A123]).
7. **Honest evaluation.**
   - We run blind (image-free) baselines to expose language bias [A011].
   - We compare against NRSC products for past Indian floods where they exist.
   - We report error rates per region and per sensor.
8. **The interface shows trust, not just numbers (M4, run 5; run 6 research).** Run 6 adds three design rules from the archive: show the area range as a few countable outcomes (a quantile dotplot or "4 in 5") rather than a density, which people read more accurately on phones [A135]; make the evidence cheap to check, because explanations only cut overreliance when checking costs less than trusting [A137], so the before and after thumbnails are one tap away; and show the defaults SatClip picked (district, window, threshold) as editable chips, the way Eviza handles ambiguity [A139]. An optional "guess first" mode for high-stakes cards is a candidate, since cognitive forcing reduces overreliance but users dislike it [A136].
   The original run 5 design: The web card leads with the number and a confidence meter that draws the publication threshold as a marker, so a 0.66 answer visibly sits just above the line and a 0.56 answer visibly sits below it. Two kinds of "no" look different: "Needs one detail" (blue, the question lacks a place or date, or the district name is ambiguous, with one-tap choices) and "Not enough evidence" (amber, the satellite measurement was too weak). Uncalibrated confidence is flagged on every card until M5.

---

## 7. What SatClip deliberately does not do

- It does not do open-ended chat about imagery. Questions outside the supported types are declined, with an example of what can be asked.
- It does not count or detect small objects. At 10 m, cars, houses and people are out of scope, and SatClip says so.
- It does not forecast. It reports what satellites observed, not what will happen.
- It does not replace official NRSC or NDEM products or field verification. It answers the local follow-up questions those products cannot, and it links to them where they exist.
- It does not present reconstructed or model-generated imagery as observed.
- It does not track individuals. The AOI is a place, and Sentinel resolution cannot identify people.

---

## 8. Where this refines the deck

| Deck | SatClip now | Why |
|---|---|---|
| A LoRA VLM at the centre generates answers for five tasks | Instruments produce the answers; the VLM parses questions and explains results | VLMs localise and count poorly [A001, A012, A013, A014]; users need checkable numbers [E39] |
| Five tasks presented equally | Change and condition questions lead (floods, crops); detection is narrowed to what 10 m supports | Highest user value, most mature methods [A022]; resolution limits |
| "Mask, scene ID, date, confidence" | The same, plus a re-runnable receipt and an observed-versus-inferred flag | Audit trail and provenance [E39]; cloud-filling risks [A019, A020] |
| EarthDial-class BigEarthNet accuracy as a target | Kept as a secondary target for the classifier; the primary metric is answer error at a fixed coverage, plus time-to-answer | The user cares about trustworthy answers per question, not leaderboard accuracy |

---

## 9. Top risks

| # | Risk | Mitigation |
|---|---|---|
| 1 | **Indian conditions break the instruments.** Flooded paddy looks like flood water [A043, A044]; permanent water and seasonal wetlands confuse change maps [A015, A022]. | Use a pre-event baseline and a permanent-water reference layer (removed first, as the NRSC flood atlas does [A046]); compute the Otsu threshold per tile and abstain on tiles with no clear water/land split [A042]; use Kerala 2018 [A042] and Bihar 2020 [A043] as named regression events; calibrate per zone. |
| 2 | **Not enough labelled Indian data for calibration.** Sen1Floods11 has only 68 hand-labelled Indian chips [A022] (an earlier version of this document wrongly said none), and runs 6 and 7 show they are the hardest: a fit made without them is still off on them (ECE 0.36 for v1.0, 0.23 for v1.1). GEOID-Flood (2026) adds 219 Copernicus EMS events with separate permanent-water labels, but 140 are in Europe [A173]. | Build a small hand-labelled Indian test set early. Use public NRSC map sheets as weak labels where licensing allows. Publish calibration error openly. |
| 3 | **The question parser misreads intent or place.** | Show "I understood your question as..." on every card. Use a fixed, small intent set. Resolve place names against gazetteers. |
| 4 | **Public endpoint limits or outages** (CDSE authentication, rate limits). | Use three catalogues with failover, aggressive caching and a local mirror option. |
| 5 | **Users over-trust a confidence number or a fluent explanation.** Explanations raise acceptance of wrong answers too [A067]; confidence display calibrates reliance but does not by itself raise accuracy [A070]; field experience says trust and workflow fit, not algorithms, limit EO uptake by responders [A069]. | Use plain-language confidence bands. Make abstention visible and normal. Show the map, not just the number. Keep explanations short and secondary. Use the human-AI guidelines [A066] as a UI checklist, and run UX testing with real officers. |
| 6 | **A large platform ships a similar assistant in India.** Google Earth AI is US-gated today [E49] and, as published, chains models under a Gemini agent without refusal or per-answer scene receipts [A095]. | Openness, offline deployment, SAR-first monsoon handling and receipts are hard for a closed service to match on government infrastructure. |
| 7 | **Scope creep back to a chatbot.** | Every new capability must arrive as an instrument plus a calibration set plus a test. |
| 8 | **Coverage collapses at a strict risk target.** In VQA, abstention at 1% risk left under 8% of questions answered [A030]. If SatClip abstains on most real questions, users stop asking. | Publish coverage at 1%, 5% and 10% risk per instrument; pick the operating point with users; prefer instruments with a physical signal (SAR water) where coverage stays high. |
| 9 | **The explanation layer hallucinates around correct numbers.** RS VLMs give hallucination-free answers only about 36% to 69% of the time, including wrong sensor and resolution claims [A033]; LVLMs over-claim co-occurring objects [A029]. | A deterministic check that every number, date, sensor and resolution in any generated sentence matches the evidence card; templated text when the check fails. |
| 10 | **Foundation models overtake instruments.** Open EO foundation models with flood and crop fine-tunes exist [A052, A055]. If they become clearly more accurate on Indian events, a threshold instrument looks dated. | Keep the instrument interface model-agnostic: a fine-tuned foundation model can register as an instrument, as long as it is calibrated, versioned and carries a receipt. The evidence card, not the algorithm, is the product. |
| 11 | **The confidence model was overconfident (confirmed run 6; run 7: water extent refitted for v1.1, water change fitted on Kuro Siwo, crop change still a placeholder because no open labelled crop-decline set exists for India).** The run 4 error model gave 0.6 to 0.7 on a bimodal flood scene; on held-out Sen1Floods11 chips, answers that cleared the 0.60 line with that score were wrong 55% of the time. | Fitted Platt map shipped (trust item 3); live Barpeta 11 July 2024 now abstains at 0.46 instead of publishing at 0.66. Refit per region and season as Indian labels arrive [A132]; fit the change instrument on Kuro Siwo [A041]. |
| 12 | **Permanent water and flooded paddy inflate "under water" numbers.** Barpeta on 11 July 2024 measured 681 sq km of water (29%), which includes the Brahmaputra channel, wetlands (beels) and flooded paddy. | Subtract a permanent-water reference (for example JRC Global Surface Water) and show "new since baseline" by default for flood questions; the change instrument already reports water before and after. |

| 13 | **The best free radar source changes its access terms.** Planetary Computer's `sentinel-1-rtc` metadata says an account is required for tokens [A123], even though anonymous SAS tokens worked in runs 4 and 5; CDSE needs S3 credentials and serves SAFE archives [A124]. | Treat token failure as a normal failover case; support CDSE with user-supplied credentials; keep an on-prem RTC path (GRD plus open terrain correction) for government deployment. |
| 14 | **No terrain or shadow mask on the radar input.** Without layover and shadow layers [A122, A123], hill shadow in the north of flood districts can read as water. | Derive a shadow mask from an open DEM (Copernicus GLO-30) and slope before thresholding; already listed as a caveat on every SAR card. |
| 15 | **The VV-only water instrument misses Indian flood water (run 6; partly fixed run 7).** Run 7 status: v1.1 with VH raises Indian median IoU from 0.03 to 0.09 and coverage from 12% to 52%, but 55% of published Indian answers are still wrong with a fit that never saw India; Indian labelled water has a median VV near -11 dB, so thresholds alone will not close the gap. Next: a learned second opinion (SoftCon or Galileo heads [A156, A153]) registered as a calibrated instrument, and per-region calibration. Original entry: On the Indian Sen1Floods11 chips inspected, labelled water had a median VV backscatter of about -12 to -13 dB (flooded vegetation, wind-roughened water), above any VV water threshold; across the 64 usable Indian chips median IoU is 0.03 and most flood questions now abstain. Abstaining is honest, but an assistant that always says "not enough evidence" is not useful (see risk 8). | Instrument v1.1: add VH (on the same chips, labelled water about -20 to -22 dB in VH versus land about -16 dB), choose thresholds on the train split only, refit the calibration and report the test, Bolivia and India numbers side by side; consider the Bruzzone and Prieto EM posterior as the per-pixel confidence [A140]. |
| 16 | **The question parser fails on Indian phrasing (measured run 6; run 7 status below).** Run 7: Indian date formats and common Hindi and Hinglish words lift the rule parser to 0.90 full match on the generated test set, but only 0.68 on 44 hand-written questions (refusal precision 0.41), because the generated set shares templates with training. The adapter must be judged on hand-written questions. Original entry: The rule parser fully understands only 16% of held-out questions (8% in Hindi), mainly because it reads only ISO dates and English keywords. | A deterministic multi-format date parser first, then the LoRA parser (M5 pipeline) only if it beats the rule baseline on unseen districts; constrained JSON decoding so it can only emit allowed values [A150]. |

---

## 10. How we will know it works (targets for M6 and M8)

| Metric | Target |
|---|---|
| Time from question to first tile result | Under 2 minutes for a district-sized AOI on CPU (to be measured) |
| Flood extent agreement with a reference map on historical Indian events | Report IoU and its uncertainty; no target until we have the reference set |
| Selective risk at a published coverage | Wrong answers among non-abstained answers, reported per sensor and per instrument |
| Receipt reproducibility | 100% of sampled receipts re-run to the same output hash |

## Run 7 additions to the risk table

| # | Risk | Mitigation |
|---|---|---|
| 17 | **Positive flood-change answers are usually wrong (measured run 7).** On Kuro Siwo, "X sq km of new water" answers are within 20% only 27% of the time, and 75% of chips with labelled flood are undercounted by more than 20%. With its regime map, the change card now abstains on almost every positive change answer, including live Barpeta June to July 2024 (0.23). | Show "water before" and "water after" extents (each from the better-calibrated extent instrument) as the default answer to "did the flood spread", with the change map as a secondary view; investigate the undercount (likely flooded vegetation and the 3 dB drop rule) before claiming change areas. |
| 18 | **Self-generated test sets flatter the system.** Template-generated intent questions gave 0.90 full match to a keyword parser; hand-written ones gave 0.68. The same trap applies to auto-generated image Q&A (`build_india_qa.py`). | Keep small hand-written test sets that are never used for tuning, collect real questions from users, and report both numbers side by side. |

