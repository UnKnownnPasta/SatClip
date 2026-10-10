# SatClip verification (M8)

This document shows, claim by claim, how the prototype demonstrates what [NOVELTY.md](../NOVELTY.md) section 5 claims. Every check has a command and a measured output. Checks marked **re-run 2026-10-10** were executed again for M8 in a 2 vCPU cloud sandbox with no GPU, against the live public catalogues. Checks marked **run 8** come from `docs/QUALITY.md` and were not repeated.

Claim keys (N1 to N8) and ingredient keys (C1 to C6) are defined in NOVELTY.md sections 5.2 and 5.4.

| Section | Claim | Check | When |
|---|---|---|---|
| 1 | All | Test suite | re-run 2026-10-10 |
| 2 | N2, N6 | Evidence card contents on a live question | run 8 card, re-derived 2026-10-10 |
| 3 | N3 (C1) | Calibration reports and exact refit | re-run 2026-10-10 |
| 4 | N4 (C2) | Abstention, follow-ups, refusal and ambiguity | re-run 2026-10-10 |
| 5 | N5 (C3) | Cold re-run of every demo receipt, two days later | re-run 2026-10-10 |
| 6 | N7 (C5) | Latency and scaling on CPU | run 8 |
| 7 | N8 (C6) | Parser on hand-written Indian questions; keyboard walkthrough | re-run 2026-10-10 |
| 8 | N1 | Archive-wide novelty scan | 2026-10-10 |
| 9 | | What is not verified | |

---

## 1. Test suite

```bash
cd backend && pip install -e ".[dev,geo,redis]" && python -m pytest -q
```

Result (2026-10-10): **73 passed** in 13.9 s. The suite runs offline on recorded STAC fixtures and synthetic rasters, and covers the parser, tiling, both queue backends, the data layer, every instrument, calibration files, the aggregator's abstention rule, receipts and the UI contract (including "no CDN scripts").

## 2. Every number comes from a named instrument, with its scenes (N2, N6)

Question: *"How much of Barpeta was under water on 2024-07-11?"* Card from `docs/demo/cards.json` (fields abridged):

| Field | Value |
|---|---|
| `answer_text` | About 914 sq km of Barpeta, Assam under water, 39% of the 2,335 sq km measured (low confidence, 0.62). |
| `understood_as` | water extent in Barpeta, Assam, 2024-07-05..2024-07-17 |
| `instrument`, `method` | `sar_water_otsu`; Sentinel-1 VV or VH backscatter below split-based thresholds |
| `scenes` | `S1A_IW_GRDH_1SDV_20240711T115715_20240711T115740_054713_06A943_rtc`, 2024-07-11, S1, planetary-computer |
| `selection_notes` | monsoon month, so radar is used first because it sees through cloud (N6) |
| `confidence`, `calibration` | 0.622, `fitted` |
| `observed_vs_inferred` | observed |
| `tiles_answered` | 117 of 117, each with a PNG mask and bounds |
| `receipt_id` | `5d27fcc87150f848` |
| `caveats` | radar misses water under dense vegetation; no terrain mask yet |

The language side never produces `value`. The parser's whole output is the five-key intent JSON (`training/lora/schema.py`), which deterministic gazetteer and date code resolve into `understood_as`. Run it: `cd backend && python -m satclip.livecheck "How much of Barpeta was under water on 2024-07-11?"` (about 80 s cold).

## 3. Calibrated confidence (N3, C1)

Reports: `training/calibration/reports/sar_water_otsu.md` (Sen1Floods11, 408 chips) and `sar_logratio_change.md` (Kuro Siwo, 848 samples, 22 events, cross-validated by event).

| Instrument | Evaluation | ECE before to after | Coverage / error at the 0.60 line |
|---|---|---|---|
| Water extent v1.1 | Held-out test, 82 chips | 0.139 to 0.074 | 0.43 / 0.257 |
| Water extent v1.1 | Bolivia, never seen | 0.402 to 0.323 | 0.43 / 0.0 |
| Water extent v1.1 | India, fit without India | 0.295 to 0.227 | 0.52 / 0.545 |
| Water change | Kuro Siwo, grouped CV | 0.214 to 0.041 (regime maps) | most positive-change answers abstain |
| Crop change | none | not fitted | card shows "Confidence not yet calibrated" |

**Re-run 2026-10-10.** Both fits were repeated from the committed per-sample rows without downloading:

```bash
python training/calibration/fit_water.py --rows training/calibration/reports/sar_water_otsu_chips.csv --no-write
python training/calibration/fit_change.py --rows training/calibration/reports/sar_logratio_change_samples.csv --no-write
```

The regenerated reports and fit JSON differed from the committed ones **only in the generation date**: every coefficient, ECE, coverage and IoU figure matched. The shipped maps in `config/calibration/` are therefore reproducible from committed data.

## 4. Abstention with a next step (N4, C2)

**Live change card (run 8 card, receipt re-run 2026-10-10).** *"Did the flood spread in Barpeta between 2024-06-05 and 2024-07-11?"* abstained at 0.23 (below 0.60), with `follow_ups` for "water before" and "water after". Both follow-ups published: 413 sq km at 0.73 and 914 sq km at 0.62. Screenshots: `docs/screenshots/08-flood-change-abstain.png`, `09-flood-change-followup.png`.

**Refusal and ambiguity (re-run 2026-10-10 against the running API, raw output in [verification/api_checks.json](verification/api_checks.json)):**

| Question | Outcome | Time | Next step shown |
|---|---|---|---|
| How many cars are parked in Barpeta on 2024-07-11? | `out_of_scope` | 0.03 s | a supported example question |
| How much of Aurangabad was under water on 2024-07-11? | `ambiguous_area` | 0.01 s | names Aurangabad, Bihar and Aurangabad, Maharashtra |
| Who will win the next election in Assam? | `out_of_scope` | 0.03 s | a supported example question |

No tiles are read and no scene is searched for these, so a refusal costs nothing.

## 5. Receipts reproduce, across days (N5, C3)

```bash
cd backend && python ../tools/reproduce.py --out ../docs/quality/reproducibility_m8.json
```

**Re-run 2026-10-10:** all 8 receipts written by the run 8 demo on 2026-10-08 were re-run cold in a fresh container, two days and one container later. Result: **8 of 8 output hashes and 8 of 8 receipts identical** (same scenes, values and confidence; 713 tiles in total; the Barpeta extent took 88.9 s cold). Raw output: [quality/reproducibility_m8.json](quality/reproducibility_m8.json). Run 8's original check is in `quality/reproducibility.json`.

This also re-validates the live data path end to end on 2026-10-10: three public catalogues reachable, Planetary Computer anonymous SAS signing still working (SOLUTION risk 13), Sentinel-2 COGs readable.

## 6. Ease and scale on CPU (N7, C5) (run 8, not re-run)

From `docs/QUALITY.md` sections 3 and 6 and `quality/loadtest.json`:

- Whole district, cold, 2 vCPU: 54 to 98 s (117 to 128 tiles); repeat question 0.5 s from the tile cache.
- Compute about 0.1 s per tile; with 400 ms simulated reads, Redis workers give 2.0, 4.0 and 7.8 tiles/s for 1, 2 and 4 processes (linear in workers).
- About 86 MB per worker; parse-only API 84 requests/s, p50 14 ms.
- No GPU, no hosted LLM, no training needed for any of the above. Re-run: `python ../tools/loadtest.py` (needs `redis-server` and `psutil`).

## 7. Non-expert Indian users (N8, C6)

**Parser, hand-written test set (re-run 2026-10-10):**
`python training/eval/eval_intents.py --data training/eval/data/intents_handwritten.jsonl`

| Slice | n | Full match | District | Dates |
|---|---|---|---|---|
| all | 44 | 0.682 | 1.000 | 0.864 |
| English | 24 | 0.750 | 1.000 | 0.875 |
| Hinglish | 12 | 0.583 | 1.000 | 0.833 |
| Hindi | 8 | 0.625 | 1.000 | 0.875 |

Refusal precision 0.41, recall 0.90. Identical to the run 7 figure. Report: [verification/intents_m8_check.md](verification/intents_m8_check.md). A wrong parse is visible in "I understood" and is one tap to correct, so it cannot silently change a number.

**Keyboard-only walkthrough (re-run 2026-10-10):** `python tools/ui_keyboard_check.py` with the API running drove the question box, district combobox, date picker and card by keyboard only and ended on the "Insufficient evidence" card for the Barpeta change question: **walkthrough OK**. Colour contrast was measured at 4.5:1 or better for all pairs in run 5 (ARCHITECTURE 6.8).

## 8. Archive-wide novelty scan (N1)

```bash
python tools/novelty_scan.py
```

225 entries scanned, 81 shortlisted, each shortlisted system judged by hand (NOVELTY.md 5.3). Output: [verification/archive_scan.csv](verification/archive_scan.csv). No archived system has more than two of the six ingredients in full; SatClip has six, with crop-change confidence labelled as a placeholder.

## 9. What is not verified

- **Usefulness to real officers** (NOVELTY condition 4): no user study yet.
- **Flood accuracy on Indian events against an official map**: the Barpeta figure has not been compared with NRSC or ASDMA maps and includes permanent water.
- **Crop-change calibration**: no open Indian crop-decline labels; the card says so.
- **The LoRA parser**: training code is smoke-tested on CPU with a tiny model only; no trained adapter has been evaluated, so the rule parser numbers above are the shipped baseline.
- **Docker deployment** was not run in the sandbox; the Redis multi-process path was tested with a local `redis-server`.
- **Product availability** (Google Earth AI in India, a Bhuvan chatbot) was checked with a short web search only.
