# SatClip state

This file is the shared memory between scheduled runs. Read it first, append a run log entry last.

## Totals

| Item | Value |
|---|---|
| Papers archived | 50 (IDs 001 to 050) |
| Next paper ID | 051 |
| Milestones done | M1 (M2 is next) |
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
