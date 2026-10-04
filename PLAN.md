# SatClip plan

## Build milestones

- [x] **M1. Architecture.** (run 2)
  - `docs/ARCHITECTURE.md` with mermaid diagrams and the scalability design: stateless API, task queue with tile-wise workers, STAC search plus COG windowed reads, caching, horizontal scaling, offline or on-prem deployment.
  - Repo scaffold: Python FastAPI backend, frontend, shared config, docker-compose.
- [ ] **M2. Data layer.**
  - STAC search over Copernicus Data Space, Element84 Earth Search and Microsoft Planetary Computer for Sentinel-1/2 by AOI and dates.
  - Cloud filtering with SAR fallback, scene metadata, tiling.
- [ ] **M3. AI engine.**
  - Task router for the supported query types.
  - CPU-friendly open models and instruments: RemoteCLIP or similar for zero-shot classification and retrieval, a small captioner, spectral index and SAR log-ratio change detection.
  - Every answer grounded to scene ID, date and region mask, with a calibrated confidence and abstention below threshold.
  - Evidence card and receipt as defined in SOLUTION.md.
- [ ] **M4. Frontend.**
  - Claymorphism UI, mobile-first.
  - Plain-language query box, AOI picking and two-date compare.
  - Evidence chips (scene, date, confidence) and a map overlay; clear abstention states.
  - Accessible contrast and keyboard support.
- [ ] **M5. Training code.**
  - LoRA fine-tuning pipeline for an open VLM on optical and SAR data (BigEarthNet, RSVQA, auto-generated Indian Q&A from Bhuvan and OSM layers).
  - A Colab notebook.
  - An evaluation harness against RSVQA and VRSBench.
  - Calibration fitting.
- [ ] **M6. Quality.**
  - Tests, sample queries and a scripted demo.
  - Load and scalability notes with measured numbers where possible.
- [ ] **M7. Deck.**
  - SatClip pitch and demo deck as .pptx, claymorphism style, UX-focused, with real prototype screenshots, saved in `deck/`.
  - Refreshed in later runs when the project changes.
- [ ] **M8. Innovation verification.**
  - Final NOVELTY.md pass against the whole archive, with each claim tied to evidence.
  - `docs/VERIFICATION.md` showing how the prototype demonstrates each claim.

## Research coverage (target about 200 papers)

Each run adds 25 papers, choosing the categories with the largest remaining gap. Counts are updated every run.

| Category key | Scope | Target | Current |
|---|---|---|---|
| rs-vlm | RS vision-language models and assistants | 25 | 9 |
| rs-benchmark | RS VQA, captioning, grounding datasets and benchmarks | 20 | 7 |
| eo-foundation | Scene classification and EO foundation models (SatMAE, Prithvi, SkySense, SSL4EO, CLIP-style) | 18 | 2 |
| change-detection | Optical and SAR change detection | 16 | 8 |
| sar-optical-fusion | SAR-optical fusion, SAR analytics, cloud removal | 15 | 4 |
| object-detection | Object detection in RS | 10 | 0 |
| trust-calibration | Hallucination, calibration, uncertainty, selective prediction and abstention | 16 | 8 |
| eo-agents | Retrieval-augmented and tool-using agents for EO | 12 | 2 |
| data-infrastructure | STAC, COG, Copernicus, tiling, job queues | 10 | 4 |
| efficient-inference | LoRA, quantization, edge and offline inference | 12 | 0 |
| indian-context | ISRO, Bhuvan, monsoon, disaster management, agriculture | 14 | 5 |
| human-factors | UX of GIS, conversational analytics, decision support | 12 | 0 |
| historical | Foundations before 2020 | 10 | 1 |
| upcoming | 2026 preprints, challenges, announced datasets | 10 | 0 |
| **Total** | | **200** | **50** |

### Suggested next batches

| Run | Categories to cover |
|---|---|
| 2 | trust-calibration (about 8: conformal prediction, selective classification, VLM hallucination such as POPE, calibration of CLIP), change-detection (about 8), indian-context (about 5), data-infrastructure (about 4) |
| 3 | eo-foundation (about 8), efficient-inference (about 6), human-factors (about 6), object-detection (about 5) |
| 4 onward | Fill the remaining gaps; upcoming work; anything that challenges NOVELTY.md |
