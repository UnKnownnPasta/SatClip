# SatClip

**Ask a plain question about any place in India and two dates. Get back an answer you can check.**

SatClip is Team Stardust's Smart India Hackathon 2026 project for problem statement **SIH26167**: "SatQueryAI: an interactive vision-language assistant for multimodal remote sensing image analysis through text queries".

You might ask: *"Was Barpeta flooded after 2 July compared to mid June?"* SatClip finds the right Sentinel-1 radar or Sentinel-2 optical scenes for that area through public STAC catalogues. If clouds block the optical view, it switches to radar on its own. Then it measures the change with a transparent instrument and returns an **evidence card**. The card holds:

- the measured answer and a map mask;
- the scene IDs and acquisition dates;
- a calibrated confidence;
- a receipt that re-runs the same analysis.

When the evidence is not good enough, it says "insufficient evidence" and tells you when the next useful satellite pass is.

## Run it

```bash
# no Docker, in-process queue
cd backend && pip install -e ".[dev]" && uvicorn satclip.api.main:app --reload
# open http://localhost:8000 ; tests: python -m pytest -q

# full stack with Redis and scalable workers
docker compose up --build        # UI on http://localhost:8080, API on :8000
docker compose up --scale worker=8
```

Until M3 lands, real questions return an honest "insufficient evidence" card because the instruments are not implemented yet.

## Who it is for

The people who must answer "where and how bad" questions without GIS skills:

- district disaster officials;
- agriculture and crop-insurance officers;
- journalists and fact-checkers;
- planners.

See [SOLUTION.md](SOLUTION.md) for the full thesis and evidence.

## Project map

| Part | Where | Status |
|---|---|---|
| Solution thesis | [SOLUTION.md](SOLUTION.md) | v1.1 (run 2) |
| Novelty analysis | [NOVELTY.md](NOVELTY.md) | v2 |
| Research archive (target about 200 papers) | [archive/](archive/README.md) | 50 papers |
| Problem evidence brief | [docs/reference/problem-evidence.md](docs/reference/problem-evidence.md) | v1 |
| Idea deck summary | [docs/reference/deck-notes.md](docs/reference/deck-notes.md) | done |
| Architecture | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | M1 done |
| Prototype (FastAPI backend and claymorphism frontend) | [backend/](backend/), [frontend/](frontend/), [config/satclip.yaml](config/satclip.yaml), [docker-compose.yml](docker-compose.yml) | M1 skeleton working; data layer M2, instruments M3, full UI M4 |
| Training code (LoRA, Colab notebook, evaluation, calibration) | `training/` | M5, planned |
| Pitch deck (.pptx) | `deck/` | M7, planned |
| Plan and progress | [PLAN.md](PLAN.md), [STATE.md](STATE.md) | live |

## Team Stardust (RVITM)

- Sai Bhuwan S
- Yashita Mandavilli
- Raj Venkat
- Nikhil S Rao
- Shashwat Mittal
- Sasanuru Anirudh

## Licence

BSD 2-Clause. See [LICENSE](LICENSE).
