# SatClip handoff (local continuation)

Written 2026-10-10 at the end of the scheduled-run series (9 runs, 2026-10-04 to 2026-10-09). From here on, work continues locally. This file holds everything a fresh person or a fresh Claude session needs. Read it top to bottom once, then use STATE.md and PLAN.md as the live logs.

Style rule for everything in this repo: English, and no em dashes anywhere (docs, slides, code comments).

---

## 1. Who and what

- **Owner:** Sai Bhuwan S (GitHub `UnKnownnPasta`), CSE student at RVITM, Team Stardust.
- **Team:** Sai Bhuwan S, Yashita Mandavilli, Raj Venkat, Nikhil S Rao, Shashwat Mittal, Sasanuru Anirudh.
- **Event:** Smart India Hackathon 2026, problem statement **SIH26167** "SatQueryAI: An Interactive Vision-Language Assistant for Multimodal Remote Sensing Image Analysis through Text Queries" (Theme: Space Technology, Software).
- **Repo:** https://github.com/UnKnownnPasta/satclip (default branch `main`). Last scheduled commit: `aed85ae` (run 9). This handoff is the commit after it.

### The original idea deck (what the team submitted)

- One interface for five geospatial AI tasks on satellite imagery driven by plain text: scene classification, captioning, VQA, object detection, change detection.
- Sentinel-1 SAR plus Sentinel-2 optical (plus Landsat) fusion, aiming at EarthDial-class accuracy on BigEarthNet.
- Two-date change intelligence.
- Flow: AOI or image plus dates, STAC ingestion, NLP pre-processing, scene retrieval, vision encoder plus projector plus task router into a LoRA-tuned open VLM for optical and SAR, grounding with scene metadata, every answer with mask, scene ID, date and calibrated confidence, abstain ("insufficient evidence") below threshold.
- Feasibility: LoRA on an open model; Indian Q&A auto-generated from BigEarthNet labels plus Bhuvan and OSM; SAR fallback for monsoon cloud; tile-wise inference with a job queue; out-of-scope queries refused.
- Claimed benefits: speed, cost (free data, open weights), trust, sovereignty (offline on government infrastructure).
- Full summary: `docs/reference/deck-notes.md`.

### The four user goals (the brief the scheduled runs followed)

1. A research archive of about 200 real, verified papers, one entry each saying what it is and what it means for SatClip. **Done: 225.**
2. A solution that is innovative in ease of solving a lasting problem, answering: whose problem, why real and lasting, how, why easier, how it scales, why trustworthy, verified against the archive. **Done as SOLUTION.md v1.8 and NOVELTY.md v9; final verification pass (M8) open.**
3. A working prototype (CPU only, open pretrained models, live Sentinel data from public STAC) plus ready-to-run LoRA training code and a Colab notebook. **Done (M1 to M6).**
4. A .pptx deck in claymorphism style (soft extruded surfaces, rounded shapes, paired inner and outer shadows, pastel but accessible palette), UX focused, in both app and deck. **Done (M7), refresh after M8.**

---

## 2. The thesis in one screen

**One line:** SatClip answers plain-language "what happened here, and when" questions about Indian land with an **evidence card**: a measurement from the actual Sentinel scene by a transparent instrument, a map of where it applies, scene IDs and dates, a calibrated confidence, and a receipt that re-runs to the same output hash. When evidence is weak it abstains and says what would fix it.

- **Users:** district disaster officials (DDMA, DM office), agriculture and crop-insurance officers (PMFBY, YES-TECH); secondary: journalists and fact-checkers, planners and researchers without GIS skills.
- **Beachhead:** monsoon flood and crop-condition questions at district level.
- **Key design change from the deck (run 1, on evidence):** instruments produce every number; the VLM only parses the question and explains. Reason: benchmarks show RS VLMs localise, count and handle SAR poorly (A001, A012, A013, A014, A033, DisasterM3, PANGAEA). The LoRA VLM stays as the language layer (parser and explainer), never the source of a number.
- **Innovation = ease:** no GIS skills, one question one card, clouds handled automatically (SAR first in monsoon), answers carry their own evidence and receipt, day-one value needs no training, runs on CPU and offline, new question type = new instrument plus calibration set.
- **Novelty is a combination claim (NOVELTY run 9):** every single ingredient exists somewhere in 2026 work (masks with answers: VisTA A179, TerraScope A201; SAR switching: EO-Gym A176; live retrieval: UnivEARTH A204; deterministic replay: OpenEarthAgent A205; flood-map rejection: SHRUG-FM A202). No archived system combines more than two of: calibrated per-answer confidence, threshold abstention with a next step, measured-reproducible Sentinel scene receipts, SAR-first monsoon handling, CPU or offline deployment, plain-language delivery for Indian districts.
- **Closest threats (watch list):** SHRUG-FM, UnivEARTH-style agents with abstention, TerraScope or OpenEarthAgent adding confidence, VisTA with confidence, EO-Gym with calibration, RSure-Agent, GeoDisaster (IIT Bombay), Google Earth AI (biggest), Earth-Agent, VHM, EarthDial follow-ups, NRSC Bhuvan chatbot.

Citation keys: `[A###]` = `archive/papers/###-*.md`; `[E##]` = claim in `docs/reference/problem-evidence.md`.

---

## 3. Status

| Milestone | Status | Where |
|---|---|---|
| M1 Architecture | done (run 2) | `docs/ARCHITECTURE.md`, `docker-compose.yml`, `config/satclip.yaml` |
| M2 Data layer | done (run 3, rebuilt run 4) | `backend/satclip/data/` |
| M3 AI engine | done (run 4) | `backend/satclip/instruments/`, `calibration.py`, `gazetteer.py`, `aggregate.py` |
| M4 Frontend | done (run 5) | `frontend/` (plain HTML/CSS/JS, vendored Leaflet) |
| M5 Training code | done (runs 6 to 7) | `training/` (+ `training/README.md`) |
| M6 Quality | done (run 8) | `tools/demo.py`, `tools/reproduce.py`, `tools/loadtest.py`, `docs/QUALITY.md`, `docs/demo/` |
| M7 Deck | done (run 9) | `deck/satclip.pptx` (14 slides), `deck/build_deck.js`, `deck/README.md` |
| **M8 Innovation verification** | **open** | NOVELTY.md final pass + `docs/VERIFICATION.md` (to write) |
| Archive | 225 papers, IDs 001 to 225, next ID **226** | `archive/papers/`, `archive/index.csv`, `archive/README.md` |
| Tests | 73 passing | `backend/tests/` |

Category counts (target / current): rs-vlm 25/28, rs-benchmark 20/22, eo-foundation 18/18, change-detection 16/18, sar-optical-fusion 15/17, object-detection 10/10, trust-calibration 16/21, eo-agents 12/15, data-infrastructure 10/12, efficient-inference 12/12, indian-context 14/16, human-factors 12/14, historical 10/10, upcoming 10/12.

---

## 4. Key measured numbers (use these on slides; sources in brackets)

- **Live demo (run 8 and 9, 2 vCPU, inline queue):** Barpeta (Assam) flood extent 2024-07-11 published **914 sq km at 0.62** (117 tiles, 77 s cold, 0.5 s warm). Barpeta flood change 5 June to 11 July 2024 **abstained at 0.23**; its follow-ups published 413 sq km (0.73) before and 914 sq km (0.62) after. Darbhanga crop change 2024-03-01 to 2024-04-25 published 1,544 sq km decline at 0.89 (**placeholder calibration**, rabi harvest explains much of it). Ambiguous district and out-of-scope answer in 0.01 s. (`docs/demo/TRANSCRIPT.md`)
- **Caveat:** the 914 sq km includes the Brahmaputra channel, permanent wetlands and paddy. Not checked against an NRSC or ASDMA map. Do not call it "flood extent" on a slide without that caveat.
- **Water calibration (Sen1Floods11, held-out 82 chips), v1.0 to v1.1 (VH added):** share correct 0.44 to 0.55; ECE after calibration 0.088 to 0.074; coverage at the 0.60 line 0.11 to 0.43; error when published 0.33 to 0.26; median IoU 0.15 to 0.31. India with a fit that never saw India: coverage 0.12 to 0.52, error when published 0.63 to 0.55, median IoU 0.03 to 0.09. (`training/calibration/reports/`)
- **Water change (Kuro Siwo, 848 samples, 22 events, CV by event):** raw AUROC 0.52; "change" answers right 27%; ECE 0.214 to 0.041 with regime maps. Flood-change cards therefore abstain on almost every real spread question, which is why follow-ups exist.
- **Reproducibility:** 8 of 8 demo receipts (713 tiles) re-run to identical output hashes from cold, after fixing GDAL decimation non-determinism and silent tile drop-outs. (`docs/quality/reproducibility.json`)
- **Load:** about 0.1 s compute per tile; Redis workers 11.8 / 21.5 / 20.1 tiles/s (1/2/4 workers, 2 cores, no I/O); with 400 ms simulated reads 2.0 / 4.0 / 7.8 tiles/s; about 86 MB per worker; parse-only API 84 req/s, p50 14 ms, p95 26 ms. (`docs/quality/loadtest.json`)
- **Intent parsing:** rule parser 0.898 full match on generated test, **0.682 on 44 hand-written questions** (refusal precision 0.41). The hand-written set is test only, never tune on it.
- **RSVQA-LR majority floor:** 0.562. **VRSBench:** 83% of yes/no answers are "yes"; answer prior 0.345.

---

## 5. Run it locally

Requirements: Python 3.10+, Node (only for the deck), optional Redis and Docker.

```bash
git clone https://github.com/UnKnownnPasta/satclip && cd satclip
python -m venv .venv && source .venv/bin/activate

cd backend
pip install -e ".[dev,geo,redis]"            # fastapi, rasterio, redis, pytest, fakeredis ...
python -m pytest -q                          # expect 73 passed (offline, uses fixtures)
uvicorn satclip.api.main:app --reload --port 8000   # UI at http://localhost:8000

# live checks against real catalogues (internet needed)
python -m satclip.data.smoke
python -m satclip.livecheck "How much of Barpeta was under water on 2024-07-11?"

# full stack
cd .. && docker compose up --build           # UI :8080, API :8000
docker compose up --scale worker=8
```

Optional land-cover instrument: `pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu && pip install -e ".[ml]"`. Without it, land-cover questions abstain.

Quality tools (run from `backend/`, each 6 to 10 min live): `python ../tools/demo.py`, then `python ../tools/reproduce.py`. Load test: `python ../tools/loadtest.py` (needs `redis-server` on PATH and `psutil`). Screenshots: API running, then `python tools/screenshots.py` and `python tools/ui_keyboard_check.py` (Playwright + Chromium).

Training: see `training/README.md`. Extras: CPU torch, `transformers peft accelerate`. Colab notebook: `training/colab/satclip_lora.ipynb` (default base Qwen2-VL-2B-Instruct, LoRA/QLoRA/DoRA, language side only). CPU smoke test:
`python training/lora/train_lora.py --model hf-internal-testing/tiny-random-Qwen2VLForConditionalGeneration --data <small jsonl> --max-steps 4 --image-size 112 --out /tmp/x`

Deck rebuild: see `deck/README.md` (needs pptxgenjs, react, react-dom, react-icons, sharp; API running for screenshots). The archive chart reads `archive/index.csv` at build time, so rebuild after adding papers.

---

## 6. Repo map

```
README.md             pitch + links
HANDOFF.md            this file
STATE.md              run log, conventions, open questions (long, authoritative history)
PLAN.md               milestone checklist + research coverage table
SOLUTION.md           thesis v1.8 (sections 1-10 + run additions, risks 1-23)
NOVELTY.md            comparison table, honest novelty, conditions, watch list (v9)
archive/              papers/NNN-slug.md, index.csv, README.md (catalog)
backend/satclip/      api/main.py, parser.py, tiling.py, jobqueue.py, worker.py, aggregate.py,
                      receipt.py, calibration.py, gazetteer.py, data/ (stac, scene, select, cog,
                      provider, smoke), instruments/ (water, vegetation, landcover, common),
                      resources/districts.json (735 districts)
backend/tests/        73 tests, fixtures/stac recorded responses
config/               satclip.yaml (all settings, env override SATCLIP_<SECTION>__<KEY>),
                      calibration/<instrument>.json
frontend/             claymorphism UI, vendored Leaflet (no CDN, a test enforces it)
training/             calibration/, lora/, eval/, colab/; reports committed, data and cache ignored
tools/                build_index.py, build_gazetteer.py, demo.py, reproduce.py, loadtest.py,
                      screenshots.py, ui_keyboard_check.py
docs/                 ARCHITECTURE.md, QUALITY.md, demo/, quality/, reference/, screenshots/, share/
deck/                 satclip.pptx, build_deck.js, capture_assets.py, assets/
```

---

## 7. Conventions and gotchas (condensed from STATE.md; read STATE.md for detail)

**Archive**
- One file per paper `archive/papers/NNN-short-slug.md`. Front matter: id, title, authors, year, venue, link, code, category, era (historical <2020, recent 2020-2026, upcoming/preprint), tags, `takeaway`, `verified` (how it was checked). Sections: Problem, Approach, Data and benchmarks, Key results, Limitations, What it means for SatClip.
- After adding papers run `python tools/build_index.py` (regenerates `index.csv` and the catalog; fails on duplicate IDs or titles).
- Every paper must be real and verified against its source page. Never invent numbers; flag what could not be confirmed. Own words, no quotes over 15 words, no PDFs committed.
- Category keys: rs-vlm, rs-benchmark, eo-foundation, change-detection, sar-optical-fusion, object-detection, trust-calibration, eo-agents, data-infrastructure, efficient-inference, indian-context, human-factors, historical, upcoming.

**Backend**
- Instruments register with `@register(name, version)`; intent to instrument mapping in `config/satclip.yaml` under `intents`; unknown names fall back to `not_implemented` (abstains honestly). `synthetic` instrument is test-only.
- Instruments get pixels only through `DataProvider` with canonical band names (`green, red, nir, swir16, scl, vv, vh`). Tests inject a fake provider via `satclip.data.provider.set_provider`.
- Shared cores `classify_sar_water` and `classify_sar_change` in `instruments/water.py` are used by both instruments and fitters: change them only together with a refit.
- COG reads always read native pixels and resize in numpy (`average` or `nearest`). Never reintroduce GDAL `out_shape` decimation (non-deterministic under concurrency).
- After any change to instruments or the data layer: re-run `tools/demo.py` and `tools/reproduce.py`.
- Queue: inline threads (dev) or Redis lists `satclip:tiles` / `satclip:processing` (prod). No Celery or RQ, by choice.
- Abstention threshold `trust.abstain_below: 0.6`; bands high >= 0.85, moderate >= 0.70.
- `.gitignore` once had a bare `data/` rule that silently dropped `backend/satclip/data/`; it is now `/data/`. After commits, check `git status --ignored` for ignored source files.

**Data access**
- Sentinel-1 pixels come only from Planetary Computer `sentinel-1-rtc` (gamma0, anonymous SAS signing; SAR thresholds from sigma0 papers are shifted +1 dB). Earth Search S1 is requester-pays and CDSE needs a login, so both are search-only (`readable: false`).
- Sentinel-2: Earth Search (do not re-apply the -0.1 offset when `earthsearch:boa_offset_applied: true`) or Planetary Computer (needs the offset for baseline 04.00+).
- Searches cached per 1 degree cell. Monsoon months 6 to 9: SAR first for water questions.
- geoBoundaries files are Git LFS; fetch via media.githubusercontent.com. OSM Overpass main endpoint was unreachable from the cloud sandbox; mail.ru mirror worked (locally the main one probably works).
- PC metadata says an account may be needed for SAS tokens (risk 13); watch for failures.

**Training and eval**
- Water: `cache_sen1floods11.py` (about 90 MB) then `fit_water.py --from-cache` and `tune_water_vh.py`. VH bounds chosen on train only; never retune on test, Bolivia or Indian chips.
- Kuro Siwo via `kurosiwo_stream.py` (HTTP range into HF webdataset); evaluate grouped by event (shards share events).
- `ndvi_difference` calibration is deliberately a placeholder (no open Indian crop-decline labels). Candidate labels found later: SICKLE (A196, Cauvery delta paddy), AgriFieldNet (A197); check before fitting.
- transformers 5.x: `dtype` not `torch_dtype`, no `warmup_ratio`, Qwen2-VL needs `mm_token_type_ids` (scripts handle these).

**Deck**
- `deck/build_deck.js` post-processes slide XML because pptxgenjs closes inner shadows with `</a:outerShdw>`. Validate after each rebuild.

**Sandbox-only problems you will probably not hit locally:** egress proxy blocks, WebFetch timeouts (agents used curl to arXiv, Crossref, OpenAlex, Semantic Scholar), Bash 10-minute limit (use nohup for long runs), `pkill -f "uvicorn satclip"` killing the tool shell.

---

## 8. Open questions and items to verify

- Confirm with the team that the deck's "unified multimodal LLM for cross-sensor EO on SAR and BigEarthNet" is EarthGPT (A002).
- Spot-check numbers before they go on slides: A001 GeoChat, A003 EarthDial, A011 RSVQA, A015 FloodNet, A016 RSICD, A022 Sen1Floods11, A033 RSHallu per-model rates.
- Unresolved: FloodNet image count (A015), SkyScript pair count (A010), RS-LLaVA base LLM (A025), EarthGPT DOI (A002).
- Many entries have flagged details (venue from arXiv comment only, abstract-only, code link not opened). The full list per run is in STATE.md "Open questions". Re-verify A197 with a normal browser.
- Licences to check before any government deployment: MobileCLIP weights (A062, Apple research terms), Qwen2-VL-2B weights (A149), Bhuvan data terms (not used so far).
- Barpeta water figure vs NRSC or ASDMA reports for early July 2024 (not yet compared).
- NOVELTY condition 4 (non-GIS users understand cards faster than maps or chat) is **untested**. A small usability test with students or officers would be the strongest missing evidence.

---

## 9. What to do next (in order)

1. **M8, innovation verification (the only open milestone).**
   - Final NOVELTY.md pass over all 225+ papers: one table with columns claim, closest prior art (archive IDs), what differs, evidence in the prototype. Keep the combination framing (section 2 above).
   - Write `docs/VERIFICATION.md`: for each claim, the command to run and the measured output (demo transcript, calibration reports, reproducibility JSON, load test, keyboard check, abstention screenshots).
   - Tick M8 in PLAN.md, update README project map.
2. **Refresh the deck** if M8 changes claim wording (innovation slide and trust slide), then rebuild and validate.
3. **Water instrument v1.2** (biggest usefulness gain, SOLUTION run 9 additions): HAND >= 10 m marked "not assessable" (MERIT Hydro, A210), per-district permanent-water and radar-insensitive exclusion map from the S1 archive (A211), per-pixel P(water) from fitted distributions with refusal when not bimodal (A212, A217), agreement score like GFM (A213); show "new water outside river and wetlands"; state unassessed built-up area on flood cards. Refit calibration and re-run demo and reproduce afterwards.
4. **Research, papers 226 onward** (PLAN row 10): agent systems named by the A209 survey (TerraAgent, GeoMMAgent, MAP-Agent, VRA, RemoteAgent, VagueEO) checked for confidence or abstention; Chow et al. 2016 HAND threshold study; new 2026 calibrated or abstaining RS models; Indian flood labels; conformal methods for area estimates. Leads already seen but not archived are in the STATE.md run logs.
5. **Small items:** Devanagari aliases for district names (QUALITY question 7); conformal range on area answers written into the receipt (A218, A219); PROV-style receipt and per-instrument model card (A222, A223); a usability test (NOVELTY condition 4).

When working with Claude Code locally, a good opening prompt is:
> Read HANDOFF.md, then STATE.md and PLAN.md. Continue with section 9 step 1 (M8). Follow the conventions in HANDOFF section 7. No em dashes. Append a dated entry to STATE.md when done.

---

## 10. The scheduled task

The cloud scheduled task that produced runs 1 to 9 can now be cancelled. Each run reads only the repo, so if it is left on it will keep committing to `main` (next it would do run 10: M8 plus papers 226 to 250), which could conflict with local work. Pause or delete it from the scheduled tasks list in the Claude app before pushing local changes.
