"""SatClip HTTP API. Stateless: all job state lives in the queue backend.

Run:  uvicorn satclip.api.main:app --reload   (from backend/)
"""
from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles

from .. import __version__
from ..aggregate import card_for_problems
from ..config import settings
from ..jobqueue import make_queue, new_job_id
from ..models import Job, JobState, QueryRequest, TileJob
from ..parser import parse
from ..receipt import build_receipt
from ..tiling import tiles_for_bbox


def create_app(cfg: Optional[dict[str, Any]] = None) -> FastAPI:
    cfg = cfg or settings()
    queue = make_queue(cfg)
    app = FastAPI(title="SatClip API", version=__version__,
                  description="Plain-language questions about land, answered with evidence cards.")
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET", "POST"], allow_headers=["*"])
    app.state.queue, app.state.cfg = queue, cfg

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok", "version": __version__, "queue": cfg.get("queue", {}).get("backend", "inline")}

    @app.get("/v1/intents")
    def intents() -> dict:
        return {"intents": cfg.get("intents", {})}

    @app.post("/v1/queries", status_code=202)
    def create_query(req: QueryRequest) -> dict:
        parsed = parse(req)
        job = Job(job_id=new_job_id(), parsed=parsed)
        if parsed.problems:
            job.card, job.state = card_for_problems(job), JobState.done
            receipt = build_receipt(parsed.model_dump(mode="json"), [], job.card.model_dump(mode="json"))
            job.card.receipt_id = receipt["receipt_id"]
            queue.store_done(job, receipt)
            return {"job_id": job.job_id, "parsed": parsed.model_dump(mode="json"), "n_tiles": 0,
                    "card": job.card.model_dump(mode="json")}
        size = float(cfg.get("tiling", {}).get("tile_deg", 0.05))
        tiles = tiles_for_bbox(parsed.bbox, size)  # type: ignore[arg-type]
        limit = int(cfg.get("tiling", {}).get("max_tiles_per_job", 400))
        if len(tiles) > limit:
            raise HTTPException(413, f"Area too large: {len(tiles)} tiles (limit {limit}). Pick a smaller area.")
        instrument = cfg.get("intents", {}).get(parsed.intent.value, "not_implemented")
        tile_jobs = [TileJob(job_id=job.job_id, tile_id=tid, bbox=tb, intent=parsed.intent,
                             windows=parsed.windows, instrument=instrument) for tid, tb in tiles]
        queue.submit(job, tile_jobs)
        return {"job_id": job.job_id, "parsed": parsed.model_dump(mode="json"), "n_tiles": len(tiles)}

    @app.get("/v1/jobs/{job_id}")
    def get_job(job_id: str) -> dict:
        job = queue.get(job_id)
        if not job:
            raise HTTPException(404, "job not found")
        return job.model_dump(mode="json")

    @app.get("/v1/jobs/{job_id}/events")
    async def job_events(job_id: str) -> StreamingResponse:
        if not queue.get(job_id):
            raise HTTPException(404, "job not found")

        async def stream():
            sent = 0
            while True:
                job = queue.get(job_id)
                for r in job.results[sent:]:
                    yield f"event: tile\ndata: {r.model_dump_json()}\n\n"
                sent = len(job.results)
                if job.state in (JobState.done, JobState.failed):
                    yield f"event: card\ndata: {json.dumps(job.card.model_dump(mode='json') if job.card else None)}\n\n"
                    return
                await asyncio.sleep(0.25)

        return StreamingResponse(stream(), media_type="text/event-stream")

    @app.get("/v1/receipts/{receipt_id}")
    def get_receipt(receipt_id: str) -> dict:
        rec = queue.receipt(receipt_id)
        if not rec:
            raise HTTPException(404, "receipt not found")
        return rec

    frontend = Path(__file__).resolve().parents[3] / "frontend"
    if frontend.is_dir():  # single-process demo: serve the UI from the API too
        app.mount("/", StaticFiles(directory=frontend, html=True), name="frontend")
    return app


app = create_app()
