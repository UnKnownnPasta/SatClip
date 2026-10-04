"""Tile result cache keyed by (tile, scenes, instrument@version, params)."""
from __future__ import annotations

import json
import threading
from typing import Optional, Protocol

from .receipt import digest


def cache_key(tile_id: str, instrument: str, windows: list, params: dict | None = None) -> str:
    return "satclip:tile:" + digest({"t": tile_id, "i": instrument, "w": windows, "p": params or {}})


class Cache(Protocol):
    def get(self, key: str) -> Optional[dict]: ...
    def set(self, key: str, value: dict) -> None: ...


class MemoryCache:
    def __init__(self) -> None:
        self._d: dict[str, str] = {}
        self._lock = threading.Lock()

    def get(self, key: str) -> Optional[dict]:
        with self._lock:
            v = self._d.get(key)
        return json.loads(v) if v else None

    def set(self, key: str, value: dict) -> None:
        with self._lock:
            self._d[key] = json.dumps(value, default=str)


class RedisCache:
    def __init__(self, client, ttl_s: int = 7 * 86400) -> None:
        self.r, self.ttl = client, ttl_s

    def get(self, key: str) -> Optional[dict]:
        v = self.r.get(key)
        return json.loads(v) if v else None

    def set(self, key: str, value: dict) -> None:
        self.r.set(key, json.dumps(value, default=str), ex=self.ttl)
