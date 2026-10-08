# SatClip state

This file is the shared memory between scheduled runs. Read it first, append a run log entry last.

## Totals

| Item | Value |
|---|---|
| Papers archived | 200 (IDs 001 to 200); 200-paper target reached in run 8 |
| Next paper ID | 201 |
| Milestones done | M1 to M6 (M6 in run 8) |
| Deck | not yet created (M7, next run) |

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

- **Training conventions (run 6).** `training/` holds `calibration/`, `lora/`, `eval/`, `colab/`. Generated data goes to `training/data/` and downloads to `training/.cache/` (both gitignored; rebuild with the builders, all seeded). Reports in `training/eval/reports/` and `training/calibration/reports/` are committed. Training extras: `pip install --break-system-packages torch torchvision --index-url https://download.pytorch.org/whl/cpu` then `transformers peft accelerate` (run 6 had transformers 5.19: `dtype` replaces `torch_dtype`, `warmup_ratio` is gone, Qwen2-VL needs `mm_token_type_ids`; the scripts handle all three). CPU smoke test: `python training/lora/train_lora.py --model hf-internal-testing/tiny-random-Qwen2VLForConditionalGeneration --data <small jsonl> --max-steps 4 --image-size 112 --out /tmp/x`.
- **Run 7 conventions.** (1) Water experiments use the local cache: `python training/calibration/cache_sen1floods11.py` (about 1 minute, about 90 MB in `training/.cache/sen1floods11/`), then `fit_water.py --from-cache` and `tune_water_vh.py`. VH bounds were chosen on train only; do not retune on test, Bolivia or Indian test chips. (2) `classify_sar_water(vv, valid, fit, vh)` and `classify_sar_change(a, b_vv, b_vh)` in `instruments/water.py` are the shared cores used by the instruments and the fitters; change them only together with a refit. (3) Calibration method `regimes` (calibration.py): `cal(raw, regime)`; `sar_logratio_change` passes "change" or "no_change" (new water at least 5% of measured area). (4) Kuro Siwo is read with `training/calibration/kurosiwo_stream.py` (HTTP range into the Hugging Face webdataset, no full download); its train and test shards share events, so evaluate grouped by event. (5) `training/eval/data/intents_handwritten.jsonl` is a test set written by hand in run 7: never tune the rule parser or prompts on it; add new hand-written questions in later runs instead. (6) OSM Overpass: overpass-api.de was unreachable from the sandbox, `maps.mail.ru/osm/tools/overpass` worked. ESA WorldCover COGs on `esa-worldcover.s3.eu-central-1.amazonaws.com` are readable directly.
- **Calibration conventions (run 6).** Instrument physics tests use the `identity_calibration` fixture (conftest) so they do not depend on fitted files; `test_calibration_files` checks the shipped maps. `"method": "inherit"` borrows another instrument's fitted map (used by `sar_logratio_change`). Refit water with `python training/calibration/fit_water.py` (streams about 1.4 GB from the public Sen1Floods11 bucket, about 5 minutes with 8 workers) or `--rows training/calibration/reports/sar_water_otsu_chips.csv` to refit without downloading.
- **Sen1Floods11 does include India (run 6).** A022 originally said India was absent; the bucket's split files show 68 Indian hand-labelled chips. A022 and SOLUTION risk 2 were corrected.

- **Run 8 conventions.** (1) COG reads (`data/cog.py`) always read whole native pixels and resize in numpy; do not reintroduce `out_shape` decimation in GDAL (non-deterministic under concurrent reads). Only `nearest` and `average` are supported. (2) Receipt tiles now include `reason`, so receipt IDs from before run 8 will not match re-runs. (3) After any change to instruments or the data layer, run `python ../tools/demo.py` then `python ../tools/reproduce.py` from `backend/` (each about 6 to 10 minutes live; run `reproduce.py` with `nohup ... &` because the Bash tool times out at 10 minutes). (4) `tools/loadtest.py` needs `redis-server` on PATH for the multi-process part (present in the sandbox) and `psutil`. (5) Sandbox installs needed this run: `pip install --break-system-packages fastapi pytest httpx fakeredis redis rasterio scipy uvicorn shapely pillow`. (6) Research agents: WebFetch permission prompts timed out again for all three agents; they used curl to export.arxiv.org, arxiv.org/html, api.crossref.org, api.openalex.org and raw GitHub READMEs, noted in each `verified` field. One agent (A197) also used api.datacite.org and source.coop; recheck that entry with WebFetch when it works.

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
- Deep Ensembles is archived as A129 and Twele et al. 2016 is archived as A083; the earlier "verified but not archived" note is out of date.
- Run 3 entries with flagged details: A052 (Prithvi-EO-2.0), A056 (DOFA) and A063 (SmolVLM) are arXiv-only; A057 (Clay) has no paper, performance claims unverified; A058 TPAMI acceptance from arXiv comment only; A062 MobileCLIP weights are under Apple research terms, check before any public deployment; A065, A066, A069 written from abstracts and metadata (publisher pages returned 403); A070 participant count for Experiment 2 looks small, recheck; A075 NeurIPS 2022 track unconfirmed; A072 is arXiv only.
- Venues confirmed only from READMEs:
  - GEOBench-VLM, ICCV 2025 (A014);
  - BigEarthNet-MM, GRSM 2021, not shown on any fetched page (A017).

- Run 4 entries with flagged details: A077, A079, A080 have no peer-reviewed venue; A081 author list differs between arXiv and the journal record; A079 training set size given as 20K and 30K in different places; A082 test-set size is the agent's estimate; A083, A085, A086 written from abstracts and GFM documentation (paywalled); A086 volume unknown and Ashman D numbers from ESA training slides; A087 volume unknown; A092 CVPR 2026 workshop venue only from its README; A095 v1 date and public access unconfirmed; A096 Earth Engine catalogue page not loaded; A098 public STAC for NISAR not confirmed; A099 no scores or dataset link; A100 commissioning date and revisit over India unconfirmed.
- Run 5 entries with flagged details: A101 has no peer-reviewed paper (usage figures self-reported by OGC); A103 manual hosted by APSAC, not pmfby.gov.in; A104 RMSE values not copied; A105 and A107 written from abstracts (MDPI and PDF not read); A108 to A113 summaries from standard knowledge (bibliographic data checked on Crossref); A114 pages not confirmed; A115 and A117 venue only from arXiv comments; A118 NeurIPS 2025 only from README; A119 track unconfirmed; A121 test cases not confirmed; A122 numeric thresholds not extracted; A123 and A124 years approximate.
- Run 8 entries with flagged details: A176 Hugging Face dataset link not fetched; A177 no code or data link found; A179 no peer-reviewed venue, test set on request; A180 relative gains as stated by the paper, per-model tables not checked; A181 no leaderboard numbers extracted; A182 no baselines, no venue; A183 flood image source not named, code not released; A186 F1 figures from the authors' EGU 2021 abstract, may differ from the journal paper; A187 MDPI full text not read (abstract only), GFM three-algorithm detail from general knowledge; A185 IoU values not quoted; A189 no Changen2 code found; A190 repository mentions paper corrections, not reviewed; A192 limitations are our reading; A194 and A193 no code; A195 code release not confirmed; A196 benchmark numbers not extracted, labels described as noisy by the authors; A197 verified partly via DataCite and source.coop; A198 ICML volume and pages not confirmed; A199 sampling figures not extracted; A200 repository URL from general knowledge.
- No verifiable Indian hand-labelled flood dataset beyond those already archived was found in run 8 (FLNet/BFCD-22 labels come from NDVI thresholds; a 2022 Assam change-detection paper is on Springer and was not readable).
- Planetary Computer `sentinel-1-rtc` metadata says an account is needed for tokens (A123), but anonymous SAS tokens worked in runs 4 and 5. Watch for failures (SOLUTION risk 13).
- Run 6 entries with flagged details: A126 cited by its Crossref chapter title and year 2000 (the 1999 tech-report form is the usual citation); A126 to A128 give no dataset or numeric results; A130 and A132 dataset names not confirmed; A131 and A132 code repositories not opened (GitHub blocked for agents); A134, A138, A139 written from abstracts; A140 and A141 abstracts only; A142 repo not checked; A146 to A148 venues from arXiv comments only; A149 and A150 have no peer-reviewed venue; A149 licence of the 2B weights not checked (must be before government deployment); bitsandbytes and Outlines repo links from general knowledge. All run 6 research agents fell back to curl (WebFetch permission prompts timed out), as noted in each `verified` field.
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

### Run 6, 2026-10-07

**Papers: 25 added (IDs 126 to 150)**
- trust-calibration (8): Platt scaling, Zadrozny and Elkan isotonic, Naeini ECE/BBQ, Deep Ensembles, Kendall and Gal uncertainties, Local Temperature Scaling, Ovadia uncertainty under shift, Conformal Risk Control.
- human-factors (6): MacEachren uncertainty semiotics, Kay quantile dotplots ("When (ish) is my bus?"), Bucinca cognitive forcing, Vasconcelos explanations and overreliance, Voigt satellite emergency mapping trends, Eviza.
- change-detection (6): Bruzzone and Prieto difference image, Gong SAR deep change, FC-Siamese, ChangeFormer, AnyChange, BFAST.
- efficient-inference (5): GPTQ, LLM.int8(), DoRA, Qwen2-VL, Outlines guided generation.
- Correction: A022 (Sen1Floods11) wrongly said India was absent; it has 68 Indian hand-labelled chips.

**Milestone M5: mostly built** (`training/`, ARCHITECTURE 6.9, `training/README.md`)
- Calibration: `training/calibration/fit_water.py` streams all 446 Sen1Floods11 hand-labelled chips, runs the production `classify_sar_water` (factored out of `sar_water_otsu` this run), labels a chip correct when its area is within 20% of the hand label, chooses Platt over isotonic on the valid split (ECE 0.107 vs 0.257), refits on train plus valid (312 chips) and writes `config/calibration/sar_water_otsu.json` (`fitted: true`, a = 2.44, b = -1.76) plus a report, plot and per-chip CSV. `fit_isotonic` rewritten (tiny blocks pooled, no duplicate points). `sar_logratio_change` borrows the water map (`inherit`).
- Language layer: `lora/schema.py` (five-key intent JSON, JSON schema for constrained decoding, resolver through the rule parser via the new `parse(req, intent=...)`), `build_intent_data.py` (12,000 / 1,500 / 1,500 pairs, English, Hinglish, Hindi, Indian date styles, typos, refusals, unseen-district test split), `build_rsvqa.py` (verified on the real RSVQA-LR files from Zenodo), `build_bigearthnet.py` (verified against the real v2 metadata.parquet; patch reading untested on real tars), `images.py` (S2 true colour, S1 VV/VH/ratio false colour), `train_lora.py` (LoRA, QLoRA, DoRA, vision tower frozen, reply-only loss; smoke-tested 4 steps on CPU with a tiny random Qwen2-VL on mixed text and image batches), `eval/eval_intents.py`, `eval/eval_vqa.py` (with yes/no confidence and risk-coverage; VRSBench converter untested), `colab/satclip_lora.ipynb`.
- Tests: 59 passing (5 new: schema, resolver, builder consistency, Sen1Floods11 regrid and metrics, calibration files).

**Measured**
- Water calibration (held-out test, 82 chips): ECE 0.296 to 0.088; at the 0.60 line, uncalibrated would publish 79% with 55% wrong, calibrated publishes 11% with 33% wrong. Bolivia: ECE 0.342 to 0.217, publishes none. India with a fit made without India: ECE 0.503 to 0.357, publishes 12% with 62.5% wrong; median IoU 0.03.
- Live: Barpeta flood extent 11 July 2024 now abstains at 0.46 (was published at 0.66); Barpeta flood change abstains; Darbhanga crop change unchanged (1,544 sq km, 0.89, placeholder calibration).
- Intent parsing, rule parser, 1,500 held-out questions: full match 0.163 (en 0.196, hinglish 0.153, hi 0.077), intent 0.569, district 0.925, dates 0.197, refusal precision 0.257 and recall 0.957.
- RSVQA-LR test (1,600 stratified), majority-per-type floor: 0.562 overall.

**Problems hit:** fresh container needed backend deps reinstalled; transformers 5.19 API changes (handled); research agents could not use WebFetch (timeouts) and used curl to arXiv, Crossref, OpenAlex and Semantic Scholar instead; GitHub pages blocked for agents, so several code links are unverified.

**Most important finding:** the first real calibration showed the water confidence was overconfident and, worse, that the VV-only water instrument misses most hand-labelled Indian flood water (flooded vegetation and rough water sit around -12 to -13 dB in VV but separate in VH). With the fitted map SatClip now abstains on most flood questions. That is the trust design working, but it makes the flagship use case unhelpful until the instrument improves.

**Exact next step (run 7)**
1. Archive papers 151 to 175: eo-foundation (about 8), object-detection (about 5), rs-vlm (about 5, newest 2026 models and any calibrated RS VLM), eo-agents (about 4), upcoming (about 3).
2. Water instrument v1.1 (highest priority, it decides whether the demo can publish anything): add VH to `classify_sar_water` (fit KI thresholds on VV and VH, water if either is below its threshold with the VH rule guarded against dry sand and shadow), tune only on Sen1Floods11 train, then refit calibration with `fit_water.py` and report test, Bolivia and India before and after. Keep v1.0 numbers in the report for comparison. Re-run livecheck on Barpeta.
3. Finish M5: `training/lora/build_india_qa.py` (OSM land-use shares over Sentinel-2 chips for sampled Indian districts via Overpass and the existing data layer), a multi-format date parser in `parser.py` (re-run `eval_intents.py --predictor rules`), and either fit `sar_logratio_change` on Kuro Siwo or record why not. Then tick M5 and start M6.

### Run 7, 2026-10-07

**Papers: 25 added (IDs 151 to 175)**
- eo-foundation (8): Presto, TESSERA, Galileo, AnySat, Copernicus-FM, SoftCon, SatlasPretrain, Scale-MAE.
- object-detection (5): Open Buildings continental detection, LS-SSDD-v1.0, SSDD official release, RTMDet, LSKNet.
- eo-agents (4): RSure-Agent (2026), DORA disaster-operations agent benchmark (2026), Earth-Agent-Pro (2026), GIS Copilot.
- rs-vlm (5): FUSAR-R1 (2026), GeoZero, More with Less (2026), ScaleEarth gated LoRA (2026), selective tool use for change VQA (2026).
- upcoming (3): GEOID-Flood benchmark (2026), GeoDisaster agent benchmark (2026, IIT Bombay), ISRO GSLV-F17/EOS-05 geosynchronous imaging satellite (launched September 2026 per ISRO pages; no data-access details found).
- All verified through the arXiv API, Crossref or official pages with curl (WebFetch permission prompts timed out for agents again); nine 2026 arXiv IDs were re-checked by the main run. Skipped as duplicates: DOFA, SpectralGPT, TerraMind, AlphaEarth, GeoRSCLIP, xView, Earth AI, GeoGround, EarthMind, Falcon, Geo-R1.

**Milestone M5: finished** (PLAN ticked)
- Water instrument v1.1 (`sar_water_otsu` 1.1, `sar_logratio_change` 1.1): VV or VH rule, joint-margin confidence, VH read optional with VV-only fallback; change uses VV or VH on both dates and a 3 dB drop in either polarisation.
- `cache_sen1floods11.py`, `tune_water_vh.py` (report `sar_water_vh_tuning.md`), `fit_water.py --from-cache --pols`, v1.0 reports kept as `sar_water_otsu_v1.0.*`, v1.0 vs v1.1 table in `sar_water_otsu.md`.
- `fit_change.py` + `kurosiwo_stream.py`: 848 Kuro Siwo samples from 22 events (train and test shards, 4 byte offsets each), grouped 5-fold CV, new `regimes` calibration method, `sar_logratio_change.json` now fitted (was borrowed).
- `build_india_qa.py`: Indian chips with WorldCover 2021 labels, S2 true colour and S1 false colour; smoke run 8 districts, 154 pairs. OSM rejected for land-use labels (rural Barpeta box: 85 features, 5 farmland); Bhuvan not used.
- Parser: `dates_in_text` (ISO, DD/MM/YYYY, DD-MM-YYYY, DD.MM.YYYY, "11th July, 2024", "July 11, 2024", Hindi month names, Devanagari digits), Hindi and Hinglish keywords, two dates make a water question a change question.
- Hand-written intent test set (44 questions, English, Hinglish, Hindi). VRSBench converter verified on the real 37,409-question file, with an answer-prior report.
- `ndvi_difference` calibration: not fitted, recorded why (no open Indian crop-decline labels).
- Tests: 66 passing (7 new in `tests/test_run7.py`; calibration-file test updated for the fitted change map).

**Measured**
- Water v1.0 -> v1.1, held-out test (82 chips): share correct 0.44 -> 0.55; ECE after 0.088 -> 0.074; coverage at 0.60 0.11 -> 0.43; error when published 0.33 -> 0.26; median IoU 0.15 -> 0.31. Bolivia: coverage 0 -> 0.43 with no errors. India, fit without India: coverage 0.12 -> 0.52, error when published 0.63 -> 0.55, median IoU 0.03 -> 0.09.
- Water change on Kuro Siwo (CV by event): raw AUROC 0.52; "no change" answers 68% right, "change" answers 27% right; 75% of flood chips undercounted by more than 20%; ECE 0.214 (borrowed) -> 0.041 (regime maps).
- Live: Barpeta flood extent 2024-07-11 published 905 sq km at 0.62 (39% of 2,335 sq km measured; was abstained at 0.46); Barpeta flood change 2024-06-05 to 2024-07-11 abstained at 0.23 (466 sq km); Darbhanga crop change unchanged (1,544 sq km, 0.89, placeholder calibration). 905 sq km includes the Brahmaputra channel and permanent wetlands (risk 12), not checked against an independent map.
- Intent parsing: generated test 0.163 -> 0.898 full match; hand-written test 0.682 (refusal precision 0.41).
- VRSBench: 83% of yes/no answers are "yes"; per-type answer prior 0.345.

**Problems hit:** Overpass main endpoint unreachable (used the mail.ru mirror); the first Kuro Siwo fit used the shard split, which shares events between train and test, and produced a flat map that abstained on everything (replaced by grouped CV and regime maps); `build_india_qa.py` is slow (about 25 s per district) because each chip does a STAC search and COG reads; research agents again could not use WebFetch.

**Most important finding:** adding VH made the water card useful again on the held-out data (it answers four times as often with fewer errors), but two hard limits surfaced: Indian flood water is still mostly missed with a fit that never saw India, and positive flood-change areas are usually undercounted, so the change card now abstains on almost every real flood spread question. The 2026 literature (RSure-Agent, selective tool use) reaches the same conclusion from the agent side: tools that run are still often wrong, and their reliability must be learned per tool.

**Exact next step (run 8)**
1. Archive papers 176 to 200 filling the remaining gaps (PLAN "Suggested next batches" row 8): rs-benchmark 7, sar-optical-fusion 5, rs-vlm 4, change-detection 2, historical 2, indian-context 2 (Indian labelled flood or crop sets usable for calibration), data-infrastructure 1, efficient-inference 1, upcoming 1. Read the "Not used, but real" leads in this log first: RS-Agent (2406.07089), CangLing-KnowFlow (2512.15231), REMSA (2511.17442), EO-Gym (2605.01250), TerraBench (2606.13148), Agentic AI for RS survey (2604.24919), lightweight VLM adaptation for MS and SAR (2609.02187).
2. Build M6 (Quality): (a) `tools/demo.py`, a scripted demo of six questions (flood extent published, flood change abstained with the before and after extents shown, crop change, ambiguous district, out of scope, Hindi question) writing `docs/demo/` cards and a short markdown transcript; (b) `docs/QUALITY.md` with sample queries and expected behaviour; (c) a load test (`tools/loadtest.py`) with the inline queue and with fakeredis plus 2 to 4 workers, measuring tiles per second, warm-cache latency and memory, and a note on horizontal scaling; (d) receipt reproducibility check (re-run 10 receipts, compare output hashes). Consider the SOLUTION risk 17 mitigation (show before and after extents for "did the flood spread") as part of M6 if small.


### Run 8, 2026-10-08

**Papers: 25 added (IDs 176 to 200). The 200-paper target is reached.**
- rs-benchmark (7): EO-Gym (2026), TerraBench (2026), CDVQA, QAG-360K/VisTA, SARLANG-1M (TGRS 2026), LRS-VQA, JL1-CC&QA (2026).
- upcoming (1): FloodReasonBench (2026).
- sar-optical-fusion (5): GLF-CR, WorldFloods, Konapala et al. S1/S2 diversity with DEM, Bayesian S1 datacube flood mapping (GFM), CNN versus DLR rule chain.
- change-detection (2): Changen2, UrbanSARFloods.
- historical (2): Rignot and van Zyl 1993 SAR ratio change, Gal and Ghahramani 2016 MC dropout.
- rs-vlm (4): lightweight VLM adaptation for MS and SAR (2026), Agentic AI for RS position paper (2026), CangLing-KnowFlow, RS-Agent.
- indian-context (2): SICKLE (Cauvery Delta paddy), AgriFieldNet (UP, Rajasthan, Odisha, Bihar).
- data-infrastructure (1): TorchGeo. efficient-inference (1): XGrammar.
- Verified with curl to arXiv, Crossref, OpenAlex and GitHub READMEs (WebFetch prompts timed out again); see "Run 8 entries with flagged details".

**Milestone M6: done** (PLAN ticked)
- `tools/demo.py`: six live questions on whole districts plus the offered follow-ups and a warm repeat; writes `docs/demo/TRANSCRIPT.md` and `cards.json`.
- `tools/reproduce.py`: cold re-run of every demo receipt; `docs/quality/reproducibility.json`.
- `tools/loadtest.py`: real water core on synthetic tiles, inline threads (1, 4, 8) and real redis-server with 1, 2, 4 worker processes, with 0 and 400 ms simulated reads; `docs/quality/loadtest.json`.
- `docs/QUALITY.md`: 12 sample questions with expected and measured behaviour, timings, reproducibility, scaling, defects, test inventory, known gaps. ARCHITECTURE 6.4 updated with measured capacity, new 6.10.
- SOLUTION risk 17 mitigation: `follow_ups` on abstained water-change cards (two extent requests, one per date window), rendered as buttons in the UI; `next_step` explains why.
- Fixes found by M6: deterministic COG reads (native read plus numpy `average`/`nearest` resize), read retries with a fresh cache key, one worker-level tile retry, `details.tiles_failed_to_read` on the card plus a warning chip, `reason` in receipt tiles.
- Tests: 73 passing (7 new in `tests/test_run8.py`).

**Measured**
- Live demo (2 vCPU sandbox, inline queue, 4 threads): Barpeta extent 2024-07-11 published 914 sq km at 0.62, 117 tiles, 77 s cold, 0.5 s warm. Barpeta change 5 June to 11 July abstained at 0.23; follow-ups published 413 sq km (0.73) and 914 sq km (0.62). Darbhanga crop change published 1,544 sq km at 0.89 (placeholder calibration), 128 tiles, 54 s. Ambiguous and out-of-scope: 0.01 s, no tiles. Hindi question with a Latin-script district: same card as the English one.
- Reproducibility: first run 7 of 8 (crop question 1,108 vs 1,544 sq km); after fixes 8 of 8 receipts (713 tiles) identical.
- Parallel read test: 64 concurrent reads of one Sentinel-2 window gave a different 3-column strip in up to 5 of 64 reads with GDAL decimation (VSI cache off; with default settings the defect changed 42 of 128 live crop tiles); identical bytes for every successful read after the fix. 1 to 6 of 64 reads fail transiently through the sandbox proxy.
- Load: compute about 0.1 s per tile; Redis workers 11.8, 21.5, 20.1 tiles/s (1, 2, 4 workers, no I/O, 2 cores); with 400 ms reads 2.0, 4.0, 7.8 tiles/s; inline threads do not scale compute (9.9 at 1 thread, 5.5 at 8). Warm 144-tile job 0.01 s inline, 0.1 to 0.2 s Redis. About 86 MB per worker, 13 MB Redis. Parse-only API 84 req/s, p50 14 ms, p95 26 ms.

**Problems hit:** the determinism fix roughly doubles cold read time (Barpeta 42 s to 77 s); the Bash tool's 10-minute limit killed one combined demo plus reproduce run (use nohup); Devanagari district names are not in the gazetteer (asks for the area instead); no new verifiable Indian hand-labelled flood set found.

**Most important finding:** M6's reproducibility check caught SatClip giving two different answers to the same question on the same scenes (GDAL decimation under concurrency plus silent tile drop-outs). Both are fixed and every receipt now re-runs identically. On the research side, VisTA [A179] already answers change questions with masks and EO-Gym [A176] already switches to SAR with a small tuned model, so SatClip's novelty must rest on the combination of calibrated confidence, abstention, scene receipts and Indian non-expert delivery (NOVELTY run 8).

**Exact next step (run 9)**
1. Archive papers 201 to 225: newly published 2026 work first, then challengers to NOVELTY.md (calibrated or abstaining RS VLMs and agents; VisTA, EO-Gym and RSure-Agent follow-ups; Google Earth AI updates), terrain and per-pixel SAR posterior methods, urban flood coherence, Indian flood labels.
2. Build M7 (deck): read the pptx skill first. Retake screenshots with the API running (`tools/screenshots.py`), adding one of the Barpeta flood-change card with its two follow-up buttons and one of a published follow-up. Build `deck/satclip.pptx` in claymorphism style with the story in the task brief, using numbers from `docs/QUALITY.md`, `docs/demo/TRANSCRIPT.md` and NOVELTY run 8; send it to the user.
3. Small items if time allows: Devanagari aliases for district names (QUALITY question 7); a slope or HAND mask in `sar_water_otsu` (A083, A186).
