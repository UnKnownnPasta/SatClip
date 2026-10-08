# SatClip quality report (M6)

Run 8, 2026-10-08. Everything here was measured in this run in the cloud sandbox (2 vCPU Intel Xeon 2.1 GHz, no GPU) against the live public catalogues, unless a line says otherwise. Raw outputs are committed next to this file.

| What | Where | How to re-run (from `backend/`) |
|---|---|---|
| Unit and integration tests | `backend/tests/` | `python -m pytest -q` |
| Scripted demo, six questions | `docs/demo/TRANSCRIPT.md`, `docs/demo/cards.json` | `python ../tools/demo.py` (full districts) or `--quick` (small boxes) |
| Receipt reproducibility | `docs/quality/reproducibility.json` | `python ../tools/reproduce.py` |
| Load and scaling test | `docs/quality/loadtest.json` | `python ../tools/loadtest.py` |
| Live smoke test of the catalogues | console | `python -m satclip.data.smoke` |
| Keyboard walkthrough and screenshots | `docs/screenshots/` | `python ../tools/ui_keyboard_check.py`, `python ../tools/screenshots.py` |

## 1. Summary

- **Tests:** 73 pass (66 before this run, 7 new in `tests/test_run8.py`).
- **Demo:** all six kinds of answer behave as designed on whole districts, live. A published flood extent, a change question that abstains and then offers the two extents (both published), a published crop change, an ambiguous district, an out-of-scope refusal and a Hindi question.
- **Reproducibility:** 8 of 8 demo receipts re-ran from a cold start to the identical receipt (same scenes, values and confidence), after two defects found by this check were fixed (section 4).
- **Scaling:** with read latency in the loop, throughput grows in proportion to worker processes (2.0, 4.0 and 7.8 tiles per second for 1, 2 and 4 Redis workers). Repeat questions are served from the tile cache in about half a second for a whole district.
- **Two defects found and fixed by M6:** non-deterministic COG decimation under concurrent reads, and transient read failures silently dropping tiles (section 5).

## 2. Sample questions and expected behaviour

These are the acceptance cases. The first six are the scripted demo (`tools/demo.py`); the rest are covered by unit tests or the hand-written intent test set (`training/eval/data/intents_handwritten.jsonl`).

| # | Question | Expected behaviour | Run 8 result |
|---|---|---|---|
| 1 | How much of Barpeta was under water on 2024-07-11? | Sentinel-1 radar (monsoon month), whole district clipped to its outline, a number with scene ID, date, map overlay and fitted confidence; published only at 0.60 or above | Published: about 914 sq km, 39% of 2,335 sq km measured, confidence 0.62 (low band), 1 scene, 117 of 117 tiles |
| 2 | Did the flood spread in Barpeta between 2024-06-05 and 2024-07-11? | Change card. Change areas are the least reliable number (SOLUTION risk 17), so below threshold it abstains and offers "water before" and "water after" as one-tap follow-ups | Abstained at 0.23. Follow-ups: 413 sq km on 5 June (0.73, published) and 914 sq km on 11 July (0.62, published, served from cache) |
| 3 | Did the crop decline in Darbhanga between 2024-03-01 and 2024-04-25? | Sentinel-2 NDVI difference on pixels clear on both dates; "Confidence not yet calibrated" chip, because no Indian crop-decline labels exist (M5 decision) | Published: about 1,544 sq km, 63% of 2,463 sq km measured, 0.89 (placeholder calibration, flagged) |
| 4 | How much of Aurangabad was under water on 2024-08-10? | Two districts share the name: ask which one, measure nothing | "Needs one detail", two one-tap choices (Bihar, Maharashtra), 0 tiles |
| 5 | Count the boats in Ernakulam | Outside the supported question types: refuse and suggest a supported one | Refused (`out_of_scope`), 0 tiles |
| 6 | Barpeta में 11 जुलाई 2024 को कितना इलाका पानी में डूबा था? | Hindi wording and Hindi month name parsed; same card as question 1 | Same answer as question 1 (cache hit, 0.5 s) |
| 7 | बारपेटा में 11 जुलाई 2024 को कितना पानी था? (district in Devanagari) | Known gap: the gazetteer has only Latin-script names, so SatClip asks for the area instead of guessing | `missing_area` (asks for the place); fix planned: Devanagari aliases in the gazetteer |
| 8 | How much was under water? | No area and no date: ask for the missing details, measure nothing | `missing_area`, then `missing_dates` |
| 9 | Did the crop decline in Darbhanga? | A change question needs two dates | `need_two_dates` |
| 10 | Describe the land in Ernakulam on 2024-02-15 | Index-based description with shares; labelled as indicative | Covered by `test_instruments.py` and run 5 screenshots |
| 11 | A drawn box larger than 400 tiles | Refuse before any work starts, ask for a smaller area | HTTP 413 with a plain message (`test_core.py`) |
| 12 | A tile whose reads fail even after retries | The tile is reported as an error, confidence is lowered, and the card shows "N map tiles could not be read" | `details.tiles_failed_to_read` and a warning chip (new in run 8) |

## 3. Scripted demo timings (live, whole districts)

| Question | Tiles | Cold time | Warm time |
|---|---|---|---|
| Barpeta flood extent | 117 | 77 s | 0.5 s |
| Barpeta flood change | 117 | 98 s | not measured |
| Barpeta extent on 5 June (follow-up) | 117 | 54 s | not measured |
| Darbhanga crop change | 128 | 54 s | not measured |
| Ambiguous district, out of scope | 0 | 0.01 s | 0.01 s |

Cold times use the inline queue with 4 threads in one process, so they are the single-laptop numbers. Before the determinism fix (section 5) the same Barpeta question took 42 s: reading at native resolution and resizing in numpy roughly doubles the bytes read for Sentinel-2 and Sentinel-1 at 20 m. We chose identical answers over speed; the cost is recovered by more workers (section 6) and by the cache.

## 4. Receipt reproducibility

Each receipt holds the parsed question, every tile's scenes, values, confidences, parameters and error reasons, and a SHA-256 hash of the output. `tools/reproduce.py` re-asks every demo question from a fresh process with an empty cache and compares hashes.

**Result (final run, 2026-10-08): 8 of 8 receipts reproduced exactly**, covering 6 measured questions (117 to 128 tiles each, 713 tiles in total) and 2 clarification cards. Every tile's scenes, values, confidences and parameters matched, and so did the published answer.

| Check | Receipts | Same output hash | Same receipt ID |
|---|---|---|---|
| First run (before the fixes in section 5) | 8 | 7 | 7 (Darbhanga crop: 1,108 vs 1,544 sq km) |
| Final run (after the fixes) | 8 | 8 | 8 |

The target in SOLUTION.md section 10 was 10 sampled receipts; the demo produces 8, so 8 were checked. Reproduction holds while the catalogues serve the same scenes; a reprocessed scene gets a new ID and the mismatch report names the tile and field that moved.

## 5. Defects found by M6 and how they were fixed

1. **Non-deterministic reads (fixed).** The first reproducibility run gave the same Darbhanga crop question two different answers (1,108 and 1,544 sq km) on the same two scenes. Two causes:
   - Letting GDAL decimate a 10 m band to 20 m inside the read is not deterministic under concurrent reads. In a test with 64 parallel reads of one window (GDAL's cache off), up to 5 reads returned a different 3-pixel-wide column strip with no error raised; with the default settings the same defect changed values in 42 of 128 tiles of the live crop question. `data/cog.py` now snaps the window to whole native pixels, reads at native resolution and resizes in numpy ("average" for reflectance and backscatter, "nearest" for the scene classification band). After the change, every successful parallel read returned identical bytes.
   - Transient HTTP failures (through this sandbox's proxy, about 1 to 6 reads in 64 under load) made some tiles fail, so they silently dropped out of the total. Reads now retry up to 4 times with a fresh cache key (GDAL remembers a failed byte range), a failed tile is retried once more by the worker after 3 s, and any tile that still fails is listed on the card (`tiles_failed_to_read`, shown as a warning chip) and in the receipt with its reason.
2. **"Did the flood spread" was almost always abstained (mitigated).** Run 7 found change areas undercount badly, so the change card abstains on nearly every real flood. The card now offers the two extents as one-tap follow-ups (`follow_ups` on the card, buttons in the UI). Live, both Barpeta extents publish (413 and 914 sq km), so the official still gets a usable answer: water more than doubled between the two passes. Caveat: both extents include permanent water such as the Brahmaputra channel (risk 12), so the difference is an upper bound on flood spread only if permanent water did not change.

## 6. Load and scaling

`tools/loadtest.py` runs the real VV+VH water core (`classify_sar_water`) on a synthetic 280 x 280 pixel tile per job tile (0.05 degrees at 20 m), so the numbers measure SatClip's own compute and queue overhead without network noise. A sleep per tile stands in for COG reads. Jobs have 144 tiles (about the size of Barpeta). Redis runs as a real `redis-server` with separate worker processes, as in docker-compose.

| Scenario | Read latency per tile | 1 | 2 | 4 | 8 |
|---|---|---|---|---|---|
| Inline threads (one process), tiles per second | 0 ms | 9.9 | | 5.3 | 5.5 |
| Inline threads, tiles per second | 400 ms | 2.0 | | 5.0 | 5.6 |
| Redis worker processes, tiles per second | 0 ms | 11.8 | 21.5 | 20.1 | |
| Redis worker processes, tiles per second | 400 ms | 2.0 | 4.0 | 7.8 | |

Other measurements:

- **Warm cache:** a repeated 144-tile job finishes in 0.01 s inline and 0.1 to 0.2 s through Redis (every tile a cache hit). Live, a repeated district question returns in 0.5 s, most of it the API's half-second polling interval.
- **Memory:** about 86 MB per worker process, 13 MB for Redis with these jobs, 78 to 124 MB for the single-process API with the inline queue.
- **API path without measurement** (parsing, refusals, clarifications): 84 requests per second from one client, median 14 ms, 95th percentile 26 ms.
- **CPU cost per tile:** about 85 to 100 ms for the water core on one core.

What this means:

- **Threads do not scale compute.** Inline threads lose to a single thread on pure compute (GIL and numpy contention on 2 vCPUs). They are fine for a laptop because live tiles are dominated by read latency, but production should run worker processes.
- **Processes scale until the cores run out.** Two Redis workers doubled compute throughput on 2 vCPUs, and four gave no more. With read latency in the loop, four workers gave 3.9 times one worker, because workers mostly wait on I/O.
- **A rough capacity model.** Live cold reads took about 0.66 s per tile of wall time with 4 threads in run 8. A 117-tile district therefore needs about 77 s on one laptop. With 16 worker processes on 4 to 8 cores it should take 10 to 20 s (extrapolated, not measured here). A state-wide flood (Assam has 35 districts, roughly 3,000 to 4,000 tiles) would take a few minutes on such a pool, with every later question about the same passes served from cache.
- **The limit is then the catalogues.** Before that size, measure the request rate that Planetary Computer and Earth Search tolerate. For an on-premises deployment, mirror the scenes for the event area into local object storage first (ARCHITECTURE 7).

## 7. Test inventory

| File | Tests | Covers |
|---|---|---|
| `test_core.py` | parser, tiling, queue, aggregation, receipts, API | Core flow and abstention rules |
| `test_data.py` | STAC search with recorded fixtures, scene selection, COG reads | Data layer (M2) |
| `test_instruments.py` | water, change, NDVI, landcover on synthetic rasters | AI engine physics (M3) |
| `test_redis_queue.py` | Redis queue with fakeredis | Exactly-once finalisation |
| `test_ui.py` | static UI rules (no CDN scripts, ARIA, config) | M4 |
| `test_training.py` | intent schema, builders, calibration methods | M5 |
| `test_run7.py` | date parser, Hindi keywords, VH water, regime calibration | Run 7 changes |
| `test_run8.py` | follow-up extents, receipt determinism, numpy resize, read path, demo coverage | Run 8 changes |

## 8. Known gaps

- District names in Devanagari or other Indian scripts are not recognised (question 7).
- `ndvi_difference` confidence is a placeholder; the card says so.
- The live water figures include permanent water and have not been compared with an independent flood map for the same dates (STATE.md open item).
- No measured multi-host numbers; the capacity model above is an extrapolation from 2 vCPUs.
