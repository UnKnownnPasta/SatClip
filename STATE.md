# SatClip state

This file is the shared memory between scheduled runs. Read it first, append a run log entry last.

## Totals

| Item | Value |
|---|---|
| Papers archived | 75 (IDs 001 to 075) |
| Next paper ID | 076 |
| Milestones done | M1, M2 (M3 is next) |
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
