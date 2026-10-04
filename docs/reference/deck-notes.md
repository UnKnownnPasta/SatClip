# Notes on the submitted idea deck (Team Stardust, SIH 2026)

A summary, in our own words, of what the team proposed in the idea submission. It is the starting point; [SOLUTION.md](../../SOLUTION.md) refines it based on evidence.

## Problem statement

- **ID:** SIH26167, "SatQueryAI: An Interactive Vision-Language Assistant for Multimodal Remote Sensing Image Analysis through Text Queries".
- **Theme:** Space Technology. **Category:** Software.

## The pitch

One place where a person types a plain question about satellite imagery and gets an answer back, covering five kinds of task:

1. Scene classification
2. Captioning
3. Visual question answering
4. Object detection
5. Change detection between two dates

## Key ideas

- **Multimodal fusion.** Use Sentinel-1 radar and Sentinel-2 optical together (Landsat as an extra optical source). Aim for accuracy comparable to EarthDial on BigEarthNet multi-label classification.
- **Temporal change.** Compare two dates, detect what changed and show where.
- **Pipeline.**
  1. The user supplies an area (or an image) and dates.
  2. Scenes are found through STAC catalogues for Sentinel-1/2 and Landsat.
  3. The question is pre-processed and matching scenes are retrieved.
  4. A vision encoder, a projector and a task router feed an open vision-language model tuned with LoRA for optical and radar.
  5. The answer is grounded in scene metadata.
- **Every answer carries evidence:** a mask, the scene ID, the acquisition date and a calibrated confidence. If confidence is below a threshold, the system says "insufficient evidence" instead of guessing.

## Feasibility choices

- **No pretraining.** LoRA fine-tuning of an existing open model, following what EarthDial showed.
- **Indian training data generated automatically.** Question and answer pairs come from BigEarthNet labels and from Bhuvan and OpenStreetMap land-use layers.
- **SAR fallback** when monsoon cloud blocks optical imagery.
- **Tile-by-tile inference** through a background job queue, streaming results per tile.
- **Narrow scope by design.** Queries outside the five supported types are refused.

## Claimed benefits

- **Speed:** analysis drops from hours to minutes.
- **Cost:** free data and open model weights.
- **Trust:** every answer is tied to a scene, a region, a date and a confidence.
- **Sovereignty:** can run offline on ISRO or government infrastructure.

## References cited in the deck

| Reference | What it is | Archive entry |
|---|---|---|
| EarthDial | InternVL2 fine-tuned for multispectral, multitemporal and multiresolution remote sensing chat | [003](../../archive/papers/003-earthdial.md) |
| A unified multimodal LLM for cross-sensor Earth observation, evaluated on SAR and BigEarthNet | Most likely EarthGPT or a similar model (to be confirmed with the team) | [002](../../archive/papers/002-earthgpt.md) |
| BigEarthNet (Sentinel-1/2) | Multi-label classification benchmark | [017](../../archive/papers/017-bigearthnet-mm.md) |
| RSVQA | Remote sensing VQA benchmark | [011](../../archive/papers/011-rsvqa.md) |
| VRSBench | Remote sensing vision-language benchmark | [012](../../archive/papers/012-vrsbench.md) |
| Copernicus Data Space | STAC and OData access to Sentinel data | See `docs/reference/problem-evidence.md`, section 5 |
