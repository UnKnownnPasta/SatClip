"""Shared settings: config/satclip.yaml plus SATCLIP_* environment overrides.

Nested keys are joined with a double underscore, e.g. SATCLIP_QUEUE__BACKEND=redis.
Values are parsed as YAML scalars, so numbers and booleans keep their types.
"""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

DEFAULT_PATH = Path(__file__).resolve().parents[2] / "config" / "satclip.yaml"
PREFIX = "SATCLIP_"


def _apply_env(cfg: dict[str, Any], environ: dict[str, str]) -> dict[str, Any]:
    for key, raw in environ.items():
        if not key.startswith(PREFIX) or key == PREFIX + "CONFIG":
            continue
        path = key[len(PREFIX):].lower().split("__")
        node = cfg
        for part in path[:-1]:
            node = node.setdefault(part, {})
        node[path[-1]] = yaml.safe_load(raw)
    return cfg


def load_settings(path: str | os.PathLike | None = None, environ: dict[str, str] | None = None) -> dict[str, Any]:
    environ = dict(os.environ if environ is None else environ)
    path = Path(path or environ.get(PREFIX + "CONFIG") or DEFAULT_PATH)
    with open(path, encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    return _apply_env(cfg, environ)


@lru_cache(maxsize=1)
def settings() -> dict[str, Any]:
    return load_settings()
