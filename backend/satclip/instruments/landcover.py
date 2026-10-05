"""Land cover and description instruments (optical, single date).

zero_shot_landcover (land_cover)
  RemoteCLIP ViT-B/32 (archive A008) scores each ~1.25 km sub-patch of a cloud-free Sentinel-2
  true-colour tile against class prompts. Probabilities come from a softmax with a calibration
  temperature (archive A031). Experimental: RemoteCLIP was trained mostly on sub-metre aerial
  imagery, so 10 m Sentinel-2 is out of its training distribution; the card says so. If torch,
  open_clip or the weights are missing, the tile abstains instead of guessing.

index_caption (describe)
  A grounded, template description from spectral indices: shares of water (NDWI > 0), dense
  vegetation (NDVI >= 0.5), sparse vegetation (0.2 to 0.5) and other surfaces (NDVI < 0.2:
  built-up, bare or fallow). No generative model, so nothing can be hallucinated.
"""
from __future__ import annotations

import os
import threading
from pathlib import Path
from typing import Any, Optional

import numpy as np

from ..calibration import load as load_cal
from ..data.provider import get_provider
from ..models import TileJob, TileResult, TileStatus
from . import register
from .common import ROOT, abstain, norm_diff, pixel_km2, region_mask, save_overlay, scene_ev

CLEAR_SCL = (4, 5, 6, 7, 11)

CLASSES: dict[str, list[str]] = {
    "water": ["a satellite image of a river", "a satellite image of a lake or pond", "a satellite image of flood water"],
    "built-up": ["a satellite image of a town with buildings and roads", "a satellite image of a dense residential area"],
    "cropland": ["a satellite image of farmland with crop fields", "a satellite image of paddy fields"],
    "forest": ["a satellite image of a dense forest", "a satellite image of tree plantations"],
    "grassland or shrubland": ["a satellite image of grassland", "a satellite image of shrubs and scrub"],
    "bare land": ["a satellite image of bare soil", "a satellite image of sand or a dry riverbed"],
    "wetland": ["a satellite image of a wetland or marsh"],
}
LC_PALETTE = {1: (37, 99, 235, 160), 2: (220, 38, 38, 150), 3: (234, 179, 8, 150), 4: (21, 128, 61, 160),
              5: (132, 204, 22, 140), 6: (168, 162, 158, 150), 7: (14, 165, 233, 150)}
GRID = 4  # 4 x 4 sub-patches per tile

_MODEL: dict[str, Any] = {}
_LOCK = threading.Lock()


def _load_clip(cfg: dict[str, Any]):
    """Lazy, once per process. Returns (model, preprocess, text_features) or raises ImportError/OSError."""
    with _LOCK:
        if "model" in _MODEL:
            return _MODEL["model"], _MODEL["pre"], _MODEL["text"]
        import open_clip
        import torch
        mc = cfg.get("models", {}).get("landcover", {})
        arch = mc.get("arch", "ViT-B-32")
        weights = mc.get("weights")
        if not weights or not Path(weights).exists():
            from huggingface_hub import hf_hub_download
            weights = hf_hub_download(mc.get("hf_repo", "chendelong/RemoteCLIP"), mc.get("hf_file", "RemoteCLIP-ViT-B-32.pt"),
                                      cache_dir=str(ROOT / cfg.get("models", {}).get("cache_dir", "backend/runtime/models")))
        model, _, pre = open_clip.create_model_and_transforms(arch)
        state = torch.load(weights, map_location="cpu")
        model.load_state_dict(state)
        model.eval()
        tok = open_clip.get_tokenizer(arch)
        feats = []
        with torch.no_grad():
            for prompts in CLASSES.values():
                f = model.encode_text(tok(prompts))
                f = f / f.norm(dim=-1, keepdim=True)
                m = f.mean(0)
                feats.append(m / m.norm())
        text = torch.stack(feats)
        _MODEL.update(model=model, pre=pre, text=text)
        return model, pre, text


def _rgb(prov, scene, bbox) -> tuple[np.ndarray, Any]:
    bands = [prov.read(scene, b, bbox, 10.0) for b in ("red", "green", "blue")]
    arr = np.stack([b.data for b in bands], -1)
    img = np.clip(np.nan_to_num(arr, nan=0.0) * 3.5, 0, 1) ** (1 / 1.2)
    return (img * 255).astype("uint8"), bands[0]


@register("zero_shot_landcover", "1.0")
def zero_shot_landcover(job: TileJob) -> TileResult:
    prov = get_provider()
    cfg = prov.cfg
    sel = prov.for_tile(job.intent, job.windows, job.bbox)[0]
    if not sel.ok:
        return abstain(job, sel.reason)
    clear, frac, _ = prov.tile_is_clear(sel.scene, job.bbox, 20.0)
    if not clear:
        return abstain(job, f"cloud: {frac:.0%} of the tile is cloud or shadow on {sel.scene.date}")
    try:
        model, pre, text = _load_clip(cfg)
    except (ImportError, OSError, RuntimeError) as exc:
        return abstain(job, f"land-cover model unavailable on this server ({type(exc).__name__}); install torch and open_clip")
    import torch
    from PIL import Image
    img, ref = _rgb(prov, sel.scene, job.bbox)
    reg = region_mask(job, ref)
    h, w = img.shape[:2]
    cal = load_cal("zero_shot_landcover")
    names = list(CLASSES)
    crops, cells = [], []
    for i in range(GRID):
        for j in range(GRID):
            ys, xs = slice(i * h // GRID, (i + 1) * h // GRID), slice(j * w // GRID, (j + 1) * w // GRID)
            if reg is not None and reg[ys, xs].mean() < 0.5:
                continue
            if (img[ys, xs].sum(-1) == 0).mean() > 0.2:
                continue
            crops.append(pre(Image.fromarray(img[ys, xs])))
            cells.append((ys, xs))
    if not crops:
        return abstain(job, "no usable sub-patches inside the district for this tile")
    with torch.no_grad():
        f = model.encode_image(torch.stack(crops))
        f = f / f.norm(dim=-1, keepdim=True)
        logits = (model.logit_scale.exp() * f @ text.T) / cal.temperature()
        probs = logits.softmax(-1).numpy()
    top = probs.argmax(1)
    counts = np.bincount(top, minlength=len(names)) / len(top)
    breakdown = {n: round(float(c), 3) for n, c in zip(names, counts) if c > 0}
    raw = float(probs.max(1).mean())
    classes = np.zeros((h, w), dtype="uint8")
    for (ys, xs), k in zip(cells, top):
        classes[ys, xs] = k + 1
    mask = save_overlay(job, ref, classes, LC_PALETTE, {str(i + 1): n for i, n in enumerate(names)}, cfg)
    cell_km2 = (h // GRID) * (w // GRID) * pixel_km2(10.0)
    return TileResult(job_id=job.job_id, tile_id=job.tile_id, status=TileStatus.ok, value=round(len(cells) * cell_km2, 4),
                      unit="km2", confidence=round(raw, 3), scenes=[scene_ev(sel.scene)], mask=mask,
                      params={"method": "RemoteCLIP ViT-B/32 zero-shot over 4 x 4 sub-patches of Sentinel-2 true colour",
                              "sensor": "S2", "selection": sel.reason, "breakdown": breakdown, "label": names[int(np.argmax(counts))],
                              "patches": len(cells), "measured_km2": round(len(cells) * cell_km2, 4), "cloud_share": round(frac, 3),
                              "temperature": cal.temperature(), "calibration": cal.status, "experimental": True})


@register("index_caption", "1.0")
def index_caption(job: TileJob) -> TileResult:
    prov = get_provider()
    cfg = prov.cfg
    res = float(cfg.get("outputs", {}).get("read_res_m", 20))
    sel = prov.for_tile(job.intent, job.windows, job.bbox)[0]
    if not sel.ok:
        return abstain(job, sel.reason)
    clear, frac, scl = prov.tile_is_clear(sel.scene, job.bbox, res)
    if not clear:
        return abstain(job, f"cloud: {frac:.0%} of the tile is cloud or shadow on {sel.scene.date}")
    red, green, nir = (prov.read(sel.scene, b, job.bbox, res) for b in ("red", "green", "nir"))
    ndvi, ndwi = norm_diff(nir.data, red.data), norm_diff(green.data, nir.data)
    reg = region_mask(job, nir)
    valid = np.isfinite(ndvi) & np.isfinite(ndwi) & np.isin(scl.data, CLEAR_SCL) & (reg if reg is not None else True)
    inside = reg.mean() if reg is not None else 1.0
    if inside == 0:
        return abstain(job, "tile lies outside the named district")
    if valid.sum() < 0.5 * inside * valid.size:
        return abstain(job, f"only {valid.mean():.0%} of the tile is clear and valid")
    cls = np.zeros(ndvi.shape, dtype="uint8")
    cls[valid & (ndvi < 0.2)] = 4
    cls[valid & (ndvi >= 0.2) & (ndvi < 0.5)] = 3
    cls[valid & (ndvi >= 0.5)] = 2
    cls[valid & (ndwi > 0)] = 1
    names = {1: "water", 2: "dense vegetation", 3: "sparse vegetation", 4: "other (built-up, bare or fallow)"}
    n = valid.sum()
    breakdown = {names[k]: round(float((cls == k).sum() / n), 3) for k in names if (cls == k).any()}
    amb = float((((np.abs(ndvi - 0.2) < 0.03) | (np.abs(ndvi - 0.5) < 0.03) | (np.abs(ndwi) < 0.03)) & valid).sum() / n)
    raw = 0.9 * (1 - amb) * (1 - frac)
    cal = load_cal("index_caption")
    mask = save_overlay(job, nir, cls, {1: (37, 99, 235, 150), 2: (21, 128, 61, 140), 3: (132, 204, 22, 120),
                                         4: (168, 162, 158, 120)}, {str(k): v for k, v in names.items()}, cfg)
    return TileResult(job_id=job.job_id, tile_id=job.tile_id, status=TileStatus.ok, value=round(float(n) * pixel_km2(res), 4),
                      unit="km2", confidence=round(cal(raw), 3), scenes=[scene_ev(sel.scene)], mask=mask,
                      params={"method": "Sentinel-2 NDVI and NDWI class shares (no generative model)", "sensor": "S2",
                              "selection": sel.reason, "breakdown": breakdown, "res_m": res, "ambiguous_share": round(amb, 4),
                              "cloud_share": round(frac, 3), "raw_quality": round(raw, 4),
                              "measured_km2": round(float(n) * pixel_km2(res), 4), "calibration": cal.status})
