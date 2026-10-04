# SatClip state

This file is the shared memory between scheduled runs. Read it first, append a run log entry last.

## Totals

| Item | Value |
|---|---|
| Papers archived | 25 (IDs 001 to 025) |
| Next paper ID | 026 |
| Milestones done | none (M1 is next) |
| Deck | not yet created (M7) |

## Conventions and decisions

- **Archive tooling.** Every paper file carries a `takeaway` field in its front matter. After adding papers, run `python tools/build_index.py`. It regenerates `archive/index.csv` and the catalog in `archive/README.md`, and fails on duplicate IDs or titles.
- **Citation keys.** In SOLUTION.md and NOVELTY.md, `[A###]` means an archive entry and `[E##]` means a numbered claim in `docs/reference/problem-evidence.md`.
- **Core design decision (run 1).** Instruments produce every number in an answer; the VLM only parses questions and explains results. The deck put the LoRA VLM at the centre. This was changed on evidence that VLMs localise and count poorly (A001, A012, A013, A014). The LoRA pipeline stays in M5 as the language layer.
- **Beachhead.** Monsoon flood and crop-condition questions at district level. Other uses come through the same machinery with different instruments.
- **No add_repo tool.** In run 1 no add_repo tool was exposed, but the repo was already cloned at `/home/claude/satclip` (origin `UnKnownnPasta/satclip`), so the run worked there.
- **Writing style.** No em dashes anywhere in the repo.

## Open questions and items to verify

- The deck reference "unified multimodal LLM for cross-sensor EO evaluated on SAR and BigEarthNet" is assumed to be EarthGPT (A002). This needs confirming with the team.
- Some entries carry numbers relayed through summarising fetches. Spot-check them before they go on slides:
  - A001 (GeoChat), A003 (EarthDial), A011 (RSVQA), A015 (FloodNet), A016 (RSICD), A022 (Sen1Floods11).
- Unresolved discrepancies flagged in the entries:
  - FloodNet image count (A015);
  - SkyScript pair count (A010);
  - RS-LLaVA base LLM (A025);
  - EarthGPT DOI (A002).
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
