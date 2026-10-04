# SatClip: the solution thesis

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
| Change detection (headline) | Measures what changed, where, between two dates, with an area figure and mask | Sentinel-1 log-ratio with an automatic two-class threshold whose fitted posterior gives the confidence [A036], calibrated on Kuro Siwo [A041] and Sen1Floods11 [A022]; optical change vector analysis or index differencing calibrated on OSCD [A034, A035]; cloud mask decides the sensor [A019] |
| Scene classification | Labels land cover for the area, with calibrated probabilities | RemoteCLIP or GeoRSCLIP zero-shot [A008, A009], plus a BigEarthNet-trained S1/S2 classifier [A017] |
| VQA | Answers only questions that break down into measurable instruments (presence, extent, area, change, trend). Anything else is declined. | Router plus instruments; never free-form generation of numbers |
| Captioning | A short description, clearly labelled as a description, not a measurement | Retrieval-based or small captioner; a VLM later [A004, A025] |
| Object detection | Limited to what 10 m data supports (large water bodies, ships in SAR, large structures). Very high resolution counting is out of scope. | Deferred to M3 evaluation; flagged honestly |

### Where the fine-tuned VLM fits

The LoRA-tuned open VLM from the deck stays in the plan (M5) and does three jobs:

- better question understanding, including Indian place names and mixed-language queries;
- richer captions;
- explanations of the evidence card.

It is evaluated against the instruments and is never the source of a number. EarthDial is the leading base candidate [A003]. It was chosen because it already handles Sentinel-1 and Sentinel-2.

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

Compared with existing approaches:

- **RS VLMs** (GeoChat, EarthGPT, EarthDial, TEOChat [A001, A002, A003, A007]) answer from model weights. Their answers carry no scene ID, date, calibrated confidence or abstention.
- **Agent frameworks** [A023, A024] chain tools but neither carry confidence through nor abstain.
- **Commercial assistants** (Google Earth AI, Earth Copilot, ArcGIS assistants) are gated by region, licence or invitation [E49 to E51].

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
4. **Abstention.** Below a threshold, or with cloud and no SAR, or for an out-of-scope question, the answer is "insufficient evidence". It also names the next useful pass, for example "next Sentinel-1 pass over this AOI: 9 July". The threshold is chosen on a risk-coverage curve for a target error rate [A027] and published together with the resulting coverage, because strict risk targets can leave very few questions answered [A030].
5. **Explanations never add persuasion.** In human-AI studies, explanations made people accept AI answers more often whether the answer was right or wrong [A067], and showing a confidence score improved how well people's reliance matched the AI's reliability without, by itself, raising joint accuracy [A070]. Trust should match capability, not be maximised [A065]. So the card leads with the map, the scenes and a plain confidence band; generated prose is short, optional and checked against the card (risk 9).
6. **Auditability.** Each answer has a receipt: query, parsed intent, scene IDs, instrument name and version, parameters, and the output hash. Re-running the receipt reproduces the answer.
7. **Honest evaluation.**
   - We run blind (image-free) baselines to expose language bias [A011].
   - We compare against NRSC products for past Indian floods where they exist.
   - We report error rates per region and per sensor.

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
| 2 | **Not enough labelled Indian data for calibration.** Sen1Floods11 has no Indian event [A022]. | Build a small hand-labelled Indian test set early. Use public NRSC map sheets as weak labels where licensing allows. Publish calibration error openly. |
| 3 | **The question parser misreads intent or place.** | Show "I understood your question as..." on every card. Use a fixed, small intent set. Resolve place names against gazetteers. |
| 4 | **Public endpoint limits or outages** (CDSE authentication, rate limits). | Use three catalogues with failover, aggressive caching and a local mirror option. |
| 5 | **Users over-trust a confidence number or a fluent explanation.** Explanations raise acceptance of wrong answers too [A067]; confidence display calibrates reliance but does not by itself raise accuracy [A070]; field experience says trust and workflow fit, not algorithms, limit EO uptake by responders [A069]. | Use plain-language confidence bands. Make abstention visible and normal. Show the map, not just the number. Keep explanations short and secondary. Use the human-AI guidelines [A066] as a UI checklist, and run UX testing with real officers. |
| 6 | **A large platform ships a similar assistant in India.** Google Earth AI is US-gated today [E49]. | Openness, offline deployment, SAR-first monsoon handling and receipts are hard for a closed service to match on government infrastructure. |
| 7 | **Scope creep back to a chatbot.** | Every new capability must arrive as an instrument plus a calibration set plus a test. |
| 8 | **Coverage collapses at a strict risk target.** In VQA, abstention at 1% risk left under 8% of questions answered [A030]. If SatClip abstains on most real questions, users stop asking. | Publish coverage at 1%, 5% and 10% risk per instrument; pick the operating point with users; prefer instruments with a physical signal (SAR water) where coverage stays high. |
| 9 | **The explanation layer hallucinates around correct numbers.** RS VLMs give hallucination-free answers only about 36% to 69% of the time, including wrong sensor and resolution claims [A033]; LVLMs over-claim co-occurring objects [A029]. | A deterministic check that every number, date, sensor and resolution in any generated sentence matches the evidence card; templated text when the check fails. |
| 10 | **Foundation models overtake instruments.** Open EO foundation models with flood and crop fine-tunes exist [A052, A055]. If they become clearly more accurate on Indian events, a threshold instrument looks dated. | Keep the instrument interface model-agnostic: a fine-tuned foundation model can register as an instrument, as long as it is calibrated, versioned and carries a receipt. The evidence card, not the algorithm, is the product. |

---

## 10. How we will know it works (targets for M6 and M8)

| Metric | Target |
|---|---|
| Time from question to first tile result | Under 2 minutes for a district-sized AOI on CPU (to be measured) |
| Flood extent agreement with a reference map on historical Indian events | Report IoU and its uncertainty; no target until we have the reference set |
| Selective risk at a published coverage | Wrong answers among non-abstained answers, reported per sensor and per instrument |
| Receipt reproducibility | 100% of sampled receipts re-run to the same output hash |
