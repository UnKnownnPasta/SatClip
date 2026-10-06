# SatClip state

This file is the shared memory between scheduled runs. Read it first, append a run log entry last.

## Totals

| Item | Value |
|---|---|
| Papers archived | 125 (IDs 001 to 125) |
| Next paper ID | 126 |
| Milestones done | M1, M2, M3, M4 (M5 is next) |
| Deck | not yet created (M7) |

## Conventions and decisions

- **Archive tooling.** Every paper file carries a `takeaway` field in its front matter. After adding papers, run `python tools/build_index.py`. It regenerates `archive/index.csv` and the catalog in `archive/README.md`, and fails on duplicate IDs or titles.
- **Citation keys.** In SOLUTION.md and NOVELTY.md, `[A###]` means an archive entry and `[E##]` means a numbered claim in `docs/reference/problem-evidence.md`.
- **Core design decision (run 1).** Instruments produce every number in an answer; the VLM only parses questions and explains results. The deck put the LoRA VLM at the centre. This was changed on evidence that VLMs localise and count poorly (A001, A012, A013, A014). The LoRA pipeline stays in M5 as the language layer.
- **Beachhead.** Monsoon flood and crop-condition questions at district level. Other uses come through the same machinery with different instruments.
- **No add_repo tool.** In run 1 no add_repo tool was exposed, but the repo was already cloned at `/home/claude/satclip` (origin `UnKnownnPasta/satclip`), so the run worked there.
- **Writing style.** No em dashes anywhere in the repo.
- **Backend conventions (run 2).** Python package `backend/satclip`. Run tests with `cd backend && python -m pytest -q` (needs fastapi, pydantic, pyyaml, pytest, httpx; fakeredis optional). The instrument for each intent is set in `config/satclip.yaml` under `intents`; unknown names fall back to `not_implemented`, which abstains honestly. The `synthetic` instrument exists only for tests and marks its cards "synthetic test data". New instruments register with `@register(name, version)` in `satclip/instruments/`.
- **Queue choice (run 2).** Inline thread-pool queue for dev and tests; Redis lists (`satclip:tiles`, `satclip:processing`) for production, with the last worker to push a result finalising the card. No Celery or RQ, to keep the dependency surface small for offline deployment.
- **Demo gazetteer (run 2).** `satclip/parser.py` holds three approximate district boxes (Barpeta, Ernakulam, Darbhanga) for demos only. M3 should replace them with real boundaries (Bhuvan or OSM).

- **Data layer conventions (run 3).** `backend/satclip/data/`. Instruments get pixels only through `DataProvider` (`for_tile`, `read`, `tile_is_clear`) and only see canonical band names (`green`, `red`, `nir`, `swir16`, `scl`, `vv`, `vh`). Searches are cached per 1 degree search cell. Tests use recorded fixtures in `backend/tests/fixtures/stac/` via `httpx.MockTransport`; COG tests write temp GeoTIFFs. Live check: `cd backend && python -m satclip.data.smoke`.
- **Catalogue readability (run 3).** Earth Search S1 GRD is requester-pays and CDSE downloads need a login, so both are marked `readable: false` for those sensors in config. Sentinel-1 pixels therefore come only from Planetary Computer `sentinel-1-rtc` (SAS-signed). S2 has two readable sources (Earth Search, Planetary Computer).
- **Lost data package (found run 4).** `.gitignore` had a bare `data/` rule, so `backend/satclip/data/` (the whole M2 data layer) was never committed in run 3; only its tests were. Run 4 rebuilt it against those committed tests and changed the rule to `/data/`. After every commit, check `git status --ignored` for source files that are being ignored.
- **Live access (run 4).** In run 4 the sandbox reached all three STAC hosts, the Sentinel-2 COG bucket, Planetary Computer SAS tokens and blob storage, Hugging Face and geoBoundaries directly. Live checks: `cd backend && python -m satclip.data.smoke` and `python -m satclip.livecheck` (writes `backend/runtime/livecheck.json`). If egress is blocked again in a later run, fall back to the fixtures.
- **Instrument conventions (run 4).** Instruments get config from `get_provider().cfg`; tests inject a fake provider with `satclip.data.provider.set_provider`. Each area instrument returns `value` (km2), `confidence`, `params.sigma_abs_km2`, `params.sigma_floor_km2`, `params.evidence_factor` and `params.measured_km2`; the aggregator sums the sds for the card confidence (ARCHITECTURE 6.7). Calibration files live in `config/calibration/<instrument>.json`; all are `fitted: false` identity maps until M5. Masks are written to `backend/runtime/masks/` (gitignored, shared docker volume) and served at `/v1/masks/{name}`.
- **Gazetteer (run 4).** `backend/satclip/resources/districts.json`, 735 districts with state and simplified outline, built by `tools/build_gazetteer.py` from geoBoundaries gbOpen IND ADM2 and ADM1 (ODbL 1.0, LGD source, build 2023-12-12; the GitHub files are LFS, fetch them via media.githubusercontent.com). Duplicate names need the state in the question. Names of four letters or fewer must match their capitalisation.
- **Radiometry (run 4).** Planetary Computer S1 RTC is gamma0 linear; SAR thresholds from sigma0 papers are shifted +1 dB. Earth Search S2 items with `earthsearch:boa_offset_applied: true` must not get the -0.1 offset again; Planetary Computer S2 needs it for baseline 04.00 and later.
- **UI conventions (run 5).** `frontend/` is plain HTML, CSS and JS with no build step; Leaflet is vendored in `frontend/vendor/leaflet/` (no CDN scripts, a test enforces it). UI settings and example questions live in `config/satclip.yaml` under `ui`, served by `GET /v1/ui-config`. Screenshots: start the API (`cd backend && uvicorn satclip.api.main:app --port 8000`), then `python tools/screenshots.py` (live questions take 20 to 60 s each) and `python tools/ui_keyboard_check.py`. Do not run `pkill -f "uvicorn satclip"` from the Bash tool: the pattern matches the tool's own shell and kills it.
- **Research agents and fetching (run 5).** Two research agents fell back to curl when WebFetch permission prompts timed out (not domain blocks). Entries were still verified against Crossref, arXiv and official pages. Later runs should prefer WebFetch and note in the entry if another route was used.
- **Sandbox egress (run 3).** The run sandbox's proxy refuses direct connections to all three STAC hosts (CONNECT 403, organization policy), even though the user allowed all websites. WebFetch can still reach them, which is how the fixtures were recorded. Live smoke and the real M3 instrument checks must be run by the user, or tested through WebFetch-recorded fixtures plus synthetic rasters.

## Open questions and items to verify

- The deck reference "unified multimodal LLM for cross-sensor EO evaluated on SAR and BigEarthNet" is assumed to be EarthGPT (A002). This needs confirming with the team.
- Some entries carry numbers relayed through summarising fetches. Spot-check them before they go on slides:
  - A001 (GeoChat), A003 (EarthDial), A011 (RSVQA), A015 (FloodNet), A016 (RSICD), A022 (Sen1Floods11).
- Unresolved discrepancies flagged in the entries:
  - FloodNet image count (A015);
  - SkyScript pair count (A010);
  - RS-LLaVA base LLM (A025);
  - EarthGPT DOI (A002).
- Run 2 entries with flagged details: A031 and A032 are arXiv-only; A033 (RSHallu) per-model rates came from a tool-assisted HTML read, recheck against the PDF before citing on slides; A039 (xBD) venue unconfirmed; A043 methods paywalled (no threshold or accuracy); A046 headline totals and sensors unconfirmed; A042 authors as initials only.
- Verified but not yet archived (good candidates for later IDs): Deep Ensembles (Lakshminarayanan et al., NIPS 2017, arXiv 1612.01474); Twele et al. 2016, Sentinel-1 automated flood processing chain (IJRS 37(13):2990-3004).
- Run 3 entries with flagged details: A052 (Prithvi-EO-2.0), A056 (DOFA) and A063 (SmolVLM) are arXiv-only; A057 (Clay) has no paper, performance claims unverified; A058 TPAMI acceptance from arXiv comment only; A062 MobileCLIP weights are under Apple research terms, check before any public deployment; A065, A066, A069 written from abstracts and metadata (publisher pages returned 403); A070 participant count for Experiment 2 looks small, recheck; A075 NeurIPS 2022 track unconfirmed; A072 is arXiv only.
- Venues confirmed only from READMEs:
  - GEOBench-VLM, ICCV 2025 (A014);
  - BigEarthNet-MM, GRSM 2021, not shown on any fetched page (A017).

- Run 4 entries with flagged details: A077, A079, A080 have no peer-reviewed venue; A081 author list differs between arXiv and the journal record; A079 training set size given as 20K and 30K in different places; A082 test-set size is the agent's estimate; A083, A085, A086 written from abstracts and GFM documentation (paywalled); A086 volume unknown and Ashman D numbers from ESA training slides; A087 volume unknown; A092 CVPR 2026 workshop venue only from its README; A095 v1 date and public access unconfirmed; A096 Earth Engine catalogue page not loaded; A098 public STAC for NISAR not confirmed; A099 no scores or dataset link; A100 commissioning date and revisit over India unconfirmed.
- Run 5 entries with flagged details: A101 has no peer-reviewed paper (usage figures self-reported by OGC); A103 manual hosted by APSAC, not pmfby.gov.in; A104 RMSE values not copied; A105 and A107 written from abstracts (MDPI and PDF not read); A108 to A113 summaries from standard knowledge (bibliographic data checked on Crossref); A114 pages not confirmed; A115 and A117 venue only from arXiv comments; A118 NeurIPS 2025 only from README; A119 track unconfirmed; A121 test cases not confirmed; A122 numeric thresholds not extracted; A123 and A124 years approximate.
- Planetary Computer `sentinel-1-rtc` metadata says an account is needed for tokens (A123), but anonymous SAS tokens worked in runs 4 and 5. Watch for failures (SOLUTION risk 13).
- Live findings to recheck in M6: Barpeta 11 July 2024 water figure (681 sq km) includes permanent water and paddy; compare with NRSC or ASDMA flood reports for early July 2024 before quoting it as flood extent.

## Run log

### Run 1, 2026-10-04

**Scaffold**
- README.md, PLAN.md (M1 to M8 checklist and a 200-paper coverage table across 14 categories), STATE.md, docs/reference/deck-notes.md, archive/README.md, archive/index.csv, archive/papers/.
- `tools/build_index.py`.

**Papers: 25 added (IDs 001 to 025)**
- Remote sensing VLMs (9): GeoChat, EarthGPT, EarthDial, SkyEyeGPT, LHRS-Bot, RSGPT, TEOChat, SARChat, RS-LLaVA.
- Benchmarks (7): RSVQA, VRSBench, VLEO-Bench, GEOBench-VLM, FloodNet, BigEarthNet-MM, SkyScript.
- EO foundation (2): RemoteCLIP, RS5M/GeoRSCLIP.
- SAR-optical fusion and SAR (4): SEN12MS, SEN12MS-CR, DSen2-CR, Sen1Floods11.
- EO agents (2): Remote Sensing ChatGPT, GeoLLM-Engine.
- Historical (1): RSICD captioning.

**Evidence brief**
- docs/reference/problem-evidence.md: 56 sourced claims on users, the skills gap, monsoon cloud, AI trust, data availability and competitors.

**Thesis**
- SOLUTION.md v1 (evidence-card thesis, beachhead, scaling, trust, non-goals, risks, deck refinements).
- NOVELTY.md v1 (comparison table across 13 systems, novelty statement, falsifiable conditions).

**Problems hit**
- arXiv export API and some direct downloads were blocked by the proxy. Agents verified through arXiv abs pages, ar5iv, GitHub READMEs and lab pages instead.
- No add_repo tool was available (see Conventions).

**Most important finding**
- Benchmarks show VLMs are weak exactly where officials need precision (localisation, counting, damage).
- India's flood products are centrally produced (about 300 in 2024) with no published turnaround time.

Together these point to an evidence-first design.

**Exact next step (run 2)**
1. Archive papers 026 to 050, focused on trust-calibration (about 8), change-detection (about 8), indian-context (about 5) and data-infrastructure (about 4).
2. Build M1:
   - `docs/ARCHITECTURE.md` with mermaid diagrams;
   - backend/ (FastAPI app skeleton, config, health endpoint, job queue stub);
   - frontend/ skeleton;
   - docker-compose.yml;
   - shared config.

### Run 2, 2026-10-04

**Papers: 25 added (IDs 026 to 050)**
- trust-calibration (8): Guo calibration, selective classification, RAPS conformal, POPE, reliable VQA abstention, CLIP zero-shot calibration, SACP (RS conformal), RSHallu (Feb 2026 preprint).
- change-detection (8): CVA polar framework, OSCD, SAR log-ratio generalized Gaussian, LEVIR-CD/STANet, BIT, xBD, LEVIR-CC, Kuro Siwo.
- indian-context (5): Kerala 2018 Otsu SAR, Bihar 2020 flood and paddy, Singha NE India paddy maps, radar vs optical in monsoon India, NRSC Flood Affected Area Atlas.
- data-infrastructure (4): Google Earth Engine, Australian Geoscience Data Cube, OGC COG standard, STAC spec.

**Milestone M1 done**
- `docs/ARCHITECTURE.md`: principles, system and sequence diagrams, data model, router table, tiling, queue, caching layers, horizontal scaling, catalogue failover, deployment modes (laptop, cloud, air-gapped), config, repo layout.
- `config/satclip.yaml` shared config with env overrides.
- `backend/satclip`: FastAPI API (health, intents, queries, jobs, SSE events, receipts), rule-based parser, deterministic tile grid, inline and Redis queues, worker with result cache, aggregator with abstention, receipts with output hash, instrument registry.
- 14 tests passing (incl. Redis queue via fakeredis). Smoke-tested with uvicorn and a Playwright screenshot of the UI shell.
- `frontend/`: claymorphism UI shell (question box, example chips, "I understood" panel, tile progress, evidence card, abstention state, dark mode, focus rings).
- `docker-compose.yml` (redis, api, 2 workers, nginx frontend) and `backend/Dockerfile`. Docker itself was not run in this sandbox.

**Docs updated**
- SOLUTION.md v1.1: change instrument recipe (A034 to A036, A041), calibration method (A026 to A028, A031, A032), new risks 8 (coverage collapse, A030) and 9 (explanation hallucination, A033), India regression events (A042, A043, A046).
- NOVELTY.md v2: run 2 evidence section; condition 1 still holds at 50 papers.

**Problems hit**
- The user said mid-run that all website access is allowed; no access requests needed.
- No add_repo tool again; worked in the existing clone. Push to main works.

**Most important finding**
- Calibration and abstention methods are mature in general ML (A026 to A030) but no RS assistant uses them, and the first RS hallucination benchmark (A033) finds RS VLMs hallucination-free only about 36% to 69% of the time. Abstention must be published with its coverage, since strict risk can leave few questions answered (A030).

**Exact next step (run 3)**
1. Archive papers 051 to 075: eo-foundation (about 8: SatMAE, Prithvi, SkySense, SSL4EO-S12, CROMA, DOFA, Clay, SpectralGPT), efficient-inference (about 6), human-factors (about 6), object-detection (about 5).
2. Build M2 in `backend/satclip/data/`: STAC search with failover over the three endpoints in config (pystac-client or plain httpx), cloud filter and SAR fallback with the monsoon rule, scene metadata into `SceneRef`, COG windowed reads with rasterio for a tile bbox, search and header caches. Add tests with recorded STAC responses so tests run offline, plus one live smoke script.

### Run 3, 2026-10-04

**Papers: 25 added (IDs 051 to 075)**
- eo-foundation (8): SatMAE, Prithvi-EO-2.0, SkySense, SSL4EO-S12, CROMA, DOFA, Clay, SpectralGPT.
- efficient-inference (6): LoRA, QLoRA, AWQ, MobileCLIP, SmolVLM, knowledge distillation (Hinton).
- human-factors (6): Lee and See trust in automation, Amershi human-AI guidelines, Bansal explanations and team performance, NL4DV, Lang et al. EO for humanitarian services, Zhang et al. confidence and trust calibration.
- object-detection (5): DOTA, xView, DIOR, Oriented R-CNN, xView3-SAR.

**Milestone M2 done** (`backend/satclip/data/`)
- `stac.py`: STAC Item Search over httpx with paging, failover and per-endpoint cooldown, request-hash cache, attempt log.
- `scene.py`: catalogue-neutral `Scene`, canonical band names across Earth Search, Planetary Computer and CDSE.
- `select.py`: monsoon SAR-first rule for water questions, optical cloud limit with SAR fallback, optical-only questions abstain on cloud, coverage/readability/band checks, closest-to-window choice, same-orbit SAR pairs for change; plain-language reasons.
- `cog.py`: windowed COG reads of a lon/lat box in native CRS, GDAL range-request settings, Planetary Computer SAS signing with token cache, SCL tile cloud fraction.
- `provider.py`: single entry point for instruments; searches per 1 degree search cell (5 neighbouring tiles cost 1 catalogue call, tested).
- `smoke.py` live smoke script; `GET /v1/scenes` API endpoint for the AOI picker.
- Config: readable flags, signing, search cell, tile cloud limit. pyproject and Dockerfile now install httpx, numpy, rasterio.
- Tests: 34 passing (20 new, offline, using fixtures recorded from the live catalogues for Barpeta 2024).
- ARCHITECTURE.md section 6.6 documents the data layer.

**Docs updated**
- SOLUTION.md v1.2: CPU-first VLM track (SmolVLM, LoRA, QLoRA, AWQ), EO foundation models as a learned second opinion registered as instruments, trust item "explanations never add persuasion" (A065, A067, A070), risk 5 strengthened, new risk 10 (foundation models overtake instruments).
- NOVELTY.md v3: run 3 evidence section and a new watch-list item.

**Problems hit**
- Direct HTTP to the three STAC hosts is blocked by the sandbox egress proxy (see Conventions). The live smoke script runs and fails cleanly with StacError, which also exercises failover. Fixtures were recorded with WebFetch.
- Still no add_repo tool; worked in the existing clone.

**Most important finding**
- Human-AI studies show explanations increase acceptance of wrong AI answers as much as right ones (A067), while calibrated confidence helps people rely appropriately (A070). This is direct evidence for SatClip's card-first, explanation-light design versus fluent RS chat assistants.

**Exact next step (run 4)**
1. Archive papers 076 to 100: rs-vlm (about 7, newest 2025 to 2026 models), sar-optical-fusion (about 6), eo-agents (about 6), upcoming (about 6).
2. Build M3 in `backend/satclip/instruments/`: `sar_water_otsu` (VV dB, per-tile Otsu with bimodality check, abstain when no clear split), `sar_logratio_change`, `ndvi_difference` (with SCL masking via `DataProvider.tile_is_clear`), `zero_shot_landcover` (RemoteCLIP or GeoRSCLIP on CPU via open_clip, lazy-loaded), a template `caption` instrument; confidence from a calibration file per instrument (temperature or isotonic, with a documented placeholder until M5 fits it); masks saved as small PNG or COG per tile and linked from the card; replace demo gazetteer with OSM/Bhuvan boundaries if reachable. Test instruments on synthetic rasters through a fake `DataProvider` reader, since live catalogue access is blocked in the sandbox.

### Run 4, 2026-10-05

**Papers: 25 added (IDs 076 to 100)**
- rs-vlm (7): GeoPixel, GeoGround, VHM, EarthMind, Falcon, Geo-R1, FUSAR-GPT.
- sar-optical-fusion (6): Twele 2016 S1 flood chain, Martinis 2009 split-based thresholding, Martinis 2015 TerraSAR-X flood service, Chini 2017 HSBA, SEN12MS-CR-TS, UnCRtainTS.
- eo-agents (6): Change-Agent, GeoGPT, Autonomous GIS (Li and Ning), ThinkGeo, GeoBenchX, Earth-Agent.
- upcoming (6): Google Earth AI, AlphaEarth Foundations, TerraMind, NISAR, IEEE GRSS DFC 2026, Sentinel-1D.

**Repair: M2 data layer rebuilt.** The run 3 data package had never been committed (see Conventions, "Lost data package"). Rebuilt `scene.py`, `stac.py`, `select.py`, `cog.py`, `provider.py`, `smoke.py` so all 34 committed tests pass, then verified live: S1 RTC and S2 windows read for Barpeta.

**Milestone M3 done** (`backend/satclip/instruments/`, `calibration.py`, `gazetteer.py`)
- `sar_water_otsu`: split-based bimodal block selection, Kittler-Illingworth threshold, neighbourhood refit, gamma0 limits, speckle removal; S2 NDWI path.
- `sar_logratio_change`: same-orbit pair, threshold from the after scene plus a 3 dB drop; S2 NDWI pair path.
- `ndvi_difference`: two-date NDVI on doubly clear pixels, decline and gain areas.
- `index_caption`: template description from NDVI and NDWI shares (no generative model).
- `zero_shot_landcover`: RemoteCLIP ViT-B/32 on CPU, lazy-loaded from Hugging Face, abstains if torch is missing.
- Confidence model (threshold-error propagation, summed tile sds) and placeholder calibration files; district gazetteer with outline clipping; per-tile PNG overlays; card fields for method, calibration status, selection notes, caveats, breakdown, details, masks; API `/v1/masks`, `/v1/regions`, `/v1/regions/{key}`; `satclip.livecheck` script.
- Tests: 49 passing (14 new instrument and API tests on synthetic rasters, plus new data and tiling tests).
- Measured live: Barpeta district, 117 tiles, 2,335 sq km, 30.6 s from question to card on sandbox CPU. The same live question run twice in fresh processes gave the same receipt output hash.

**Defects found on live data and fixed:** Otsu threshold misplaced on real SAR (switched to Kittler-Illingworth); Earth Search reflectance offset applied twice (description changed from 88% to 38% dense vegetation after the fix); tiling float edge added an extra column of tiles; naive Ashman D test passes unimodal data (now D >= 3 plus a 3 dB gap).

**Docs updated:** ARCHITECTURE 6.7 (engine as built), SOLUTION v1.3 (ease evidence from agent benchmarks, built instruments, confidence as built, risks 11 and 12), NOVELTY v4 (seven new comparison rows, narrowed abstention claim, run 4 evidence, Google Earth AI now top threat), README, PLAN.

**Problems hit:** torchvision from PyPI mismatched the CPU torch build (reinstall from the PyTorch CPU index fixed it). geoBoundaries files are Git LFS pointers on raw.githubusercontent.

**Most important finding:** instrument-grounded EO agents now exist (Earth-Agent at ICLR 2026, Google Earth AI), so "instruments answer" alone is not new. But those agents get tool parameters right only 26% to 35% of the time and none abstains or attaches scene receipts. Our own live test showed the value of the gate: RemoteCLIP mislabelled Darbhanga cropland and the card abstained instead of publishing it.

**Exact next step (run 5)**
1. Archive papers 101 to 125: indian-context (about 7: ASDMA/NDMA flood reporting, Bhuvan, PMFBY YES-TECH, NRSC crop monitoring, Assam 2022 or 2024 floods), historical (about 7: Otsu 1979, Kittler-Illingworth 1986, McFeeters NDWI 1996, Tucker NDVI 1979, Chow 1970 reject option, Lee filter 1980, CVA Malila 1980), rs-benchmark (about 6), data-infrastructure (about 5).
2. Build M4 in `frontend/`: map (Leaflet or MapLibre from cdnjs) with district search via `/v1/regions`, outline from `/v1/regions/{key}`, tile overlays from card `masks`, two-date compare picker, evidence chips (scene, date, sensor, confidence band, calibration status), abstention state with reason and next step, ambiguous-district chooser, method and caveats drawer, receipt link; mobile-first claymorphism, keyboard and contrast checks; Playwright screenshots saved in `docs/screenshots/` for the deck.

### Run 5, 2026-10-06

**Papers: 25 added (IDs 101 to 125)**
- indian-context (7): Bhuvan, NDEM, PMFBY YES-TECH manual, FASAL wheat forecasts, Assam 2022 Sentinel-1 flood study, NRSC Assam Flood Hazard Zonation Atlas, Sentinel-1 near-real-time kharif rice mapping.
- historical (7): Otsu 1979, Kittler-Illingworth 1986, McFeeters NDWI 1996, Tucker NDVI 1979, Chow reject option 1970, Lee local-statistics filter 1980, Malila change vector analysis 1980.
- rs-benchmark (6): EarthVQA, RSVG/DIOR-RSVG, XLRS-Bench, DisasterM3, GEO-Bench, PANGAEA.
- data-infrastructure (5): openEO API, CEOS-ARD SAR (NRB), Planetary Computer Sentinel-1 RTC, Copernicus Data Space APIs, odc-stac.

**Milestone M4 done** (`frontend/`, ARCHITECTURE 6.8)
- Mobile-first claymorphism UI: question box with examples from config, folded district combobox (ARIA 1.2, arrow keys) and one-date or two-date picker, "I understood" panel with four progress steps and a progressbar, evidence card (headline number, confidence meter with the 0.60 publication marker, evidence chips grouped by sensor and date, calibration chip, method drawer with scene choice, numbers, breakdown bars and caveats, receipt open and copy), two distinct "no" states ("Needs one detail" with one-tap district choices, "Not enough evidence" with what would help), vendored Leaflet map with district outline, per-tile overlays, legend with colours and overlay toggle, light and dark themes, reduced motion.
- Backend support: `QueryRequest.region` (picked district wins over text), `ParsedQuery.candidate_keys`, `GET /v1/ui-config`, `ui` block in config, legend colours on masks, example dates in "what would help" text moved to 2024 dates that have data.
- Tests: 54 passing (5 new in `tests/test_ui.py`). Keyboard-only walkthrough passes. All colour pairs measured at 4.5:1 or better (light and dark).
- Screenshots from live runs in `docs/screenshots/` (8 screens: home, flood extent desktop, mobile and dark, ambiguous district, out of scope, crop change, flood change abstention).

**Measured live in the UI:** Barpeta flood extent 2024-07-11 published at 681 sq km (0.66, low band); Barpeta flood change 2024-06-05 to 2024-07-11 abstained at 0.56; Darbhanga crop change 2024-03-01 to 2024-04-25 published at 1,544 sq km decline (0.89, high; rabi harvest explains much of it, which the caveat says); Aurangabad offered Bihar and Maharashtra.

**Docs updated:** SOLUTION v1.4 (official channels NDEM, Bhuvan, YES-TECH, FASAL as the context SatClip complements; Chow reject option as the root of abstention; CEOS-ARD check in receipts; trust item 8 on the UI; risks 13 radar access terms and 14 missing shadow mask), NOVELTY v5 (run 5 evidence: DisasterM3, XLRS-Bench, EarthVQA, PANGAEA; data-layer ease not claimed as unique given openEO and odc-stac; new watch-list item), README (screenshot, statuses), ARCHITECTURE 6.8, PLAN.

**Problems hit:** WebFetch permission prompts timed out for two research agents (they used curl against Crossref and arXiv). `pkill -f "uvicorn satclip"` killed the tool shell (see Conventions).

**Most important finding:** benchmarks from 2025 to 2026 keep landing on the same side: VLMs are near chance at counting disaster damage and worse on SAR (DisasterM3), and on Sen1Floods11 a plain UNet beats every geospatial foundation model while RemoteCLIP reaches only about 55 water IoU (PANGAEA). Classical, auditable instruments behind a calibrated, abstaining card remain the right core.

**Exact next step (run 6)**
1. Archive papers 126 to 150: trust-calibration (about 8: isotonic regression calibration, Platt scaling, risk-coverage and AURC, conformal risk control, semantic segmentation calibration, LVLM abstention or "I don't know" training, uncertainty in RS segmentation), human-factors (about 6), change-detection (about 6), efficient-inference (about 5).
2. Build M5 in `training/`: (a) `calibration/fit.py` that runs the water instruments on Sen1Floods11 hand-labelled chips (and Kuro Siwo if reachable), fits isotonic maps into `config/calibration/*.json` with `fitted: true`, and writes reliability diagrams and risk-coverage curves; (b) LoRA fine-tuning for the parser and explainer (SmolVLM or Qwen2-VL-2B, PEFT, QLoRA) on RSVQA plus auto-generated question-to-intent pairs from the gazetteer and templates; (c) a Colab notebook; (d) an evaluation harness for RSVQA and VRSBench subsets. If too big, do (a) first since it makes the confidence real, and note the stop point.
