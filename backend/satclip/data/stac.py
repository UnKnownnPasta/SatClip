"""STAC API Item Search with failover across public catalogues (ARCHITECTURE.md 6.6).

- POST /search with paging through `next` links.
- An endpoint that errors is put in cooldown and skipped until it expires.
- Endpoints that cannot serve readable pixels for a sensor are tried only as a last resort.
- Identical requests are answered from an in-memory cache; every attempt is logged for receipts.
"""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from datetime import date
from typing import Any, Callable, Optional

import httpx

from .scene import Scene, normalize_item


class StacError(RuntimeError):
    """No configured catalogue could answer."""


@dataclass
class Endpoint:
    name: str
    url: str
    s2_collection: str
    s1_collection: str
    signing: Optional[str] = None
    readable: dict[str, bool] = field(default_factory=lambda: {"S1": True, "S2": True})

    def __post_init__(self):
        self.readable = {k.upper(): bool(v) for k, v in (self.readable or {}).items()}

    def collection(self, sensor: str) -> str:
        return self.s1_collection if sensor == "S1" else self.s2_collection

    def can_read(self, sensor: str) -> bool:
        return self.readable.get(sensor, True)


class StacClient:
    def __init__(self, endpoints: list[Endpoint], transport: Optional[httpx.BaseTransport] = None,
                 clock: Callable[[], float] = time.monotonic, cooldown_s: float = 120, timeout_s: float = 20,
                 page_size: int = 100, max_items: int = 200):
        self.endpoints = endpoints
        self.clock = clock
        self.cooldown_s = cooldown_s
        self.page_size = page_size
        self.max_items = max_items
        self.http = httpx.Client(transport=transport, timeout=timeout_s, follow_redirects=True)
        self._down_until: dict[str, float] = {}
        self._cache: dict[str, list[Scene]] = {}
        self.log: list[dict[str, Any]] = []

    @classmethod
    def from_settings(cls, cfg: dict[str, Any], **kw) -> "StacClient":
        s = cfg.get("stac", {})
        eps = [Endpoint(e["name"], e["url"], e["s2_collection"], e["s1_collection"], signing=e.get("signing"),
                        readable=e.get("readable") or {}) for e in s.get("endpoints", [])]
        return cls(eps, cooldown_s=s.get("cooldown_s", 120), timeout_s=s.get("timeout_s", 20),
                   page_size=s.get("page_size", 100), max_items=s.get("max_items", 200), **kw)

    def health(self) -> dict[str, str]:
        now = self.clock()
        return {e.name: ("cooldown" if self._down_until.get(e.name, 0) > now else "ok") for e in self.endpoints}

    @staticmethod
    def body(collection: str, bbox, start: date, end: date, max_cloud: Optional[float], limit: int) -> dict:
        b: dict[str, Any] = {"collections": [collection], "bbox": list(bbox),
                             "datetime": f"{start.isoformat()}T00:00:00Z/{end.isoformat()}T23:59:59Z", "limit": limit}
        if max_cloud is not None:
            b["query"] = {"eo:cloud_cover": {"lte": max_cloud}}
        return b

    def _ordered(self, sensor: str) -> list[Endpoint]:
        return [e for e in self.endpoints if e.can_read(sensor)] + [e for e in self.endpoints if not e.can_read(sensor)]

    def _fetch(self, ep: Endpoint, body: dict) -> list[dict]:
        url, payload, items = ep.url.rstrip("/") + "/search", dict(body), []
        while url and len(items) < self.max_items:
            r = self.http.post(url, json=payload)
            r.raise_for_status()
            data = r.json()
            items.extend(data.get("features", []))
            nxt = next((l for l in data.get("links", []) if l.get("rel") == "next"), None)
            if not nxt or not data.get("features"):
                break
            url = nxt.get("href")
            if (nxt.get("method") or "GET").upper() == "POST":
                payload = {**payload, **(nxt.get("body") or {})} if nxt.get("merge", True) else nxt.get("body", {})
            else:  # GET-style next link: fall back to posting the original body with the token in the URL
                payload = dict(body)
        return items[: self.max_items]

    def search(self, sensor: str, bbox, start: date, end: date, max_cloud: Optional[float] = None) -> list[Scene]:
        sensor = sensor.upper()
        errors = []
        for ep in self._ordered(sensor):
            body = self.body(ep.collection(sensor), bbox, start, end, max_cloud if sensor == "S2" else None, self.page_size)
            key = hashlib.sha256(json.dumps([ep.url, body], sort_keys=True).encode()).hexdigest()
            if key in self._cache:
                self.log.append({"endpoint": ep.name, "sensor": sensor, "cache_hit": True, "ok": True})
                return list(self._cache[key])
            if self._down_until.get(ep.name, 0) > self.clock():
                errors.append(f"{ep.name}: cooling down")
                continue
            t0 = time.monotonic()
            try:
                feats = self._fetch(ep, body)
            except (httpx.HTTPError, ValueError) as exc:
                self._down_until[ep.name] = self.clock() + self.cooldown_s
                errors.append(f"{ep.name}: {type(exc).__name__}")
                self.log.append({"endpoint": ep.name, "sensor": sensor, "cache_hit": False, "ok": False,
                                 "error": repr(exc)[:200]})
                continue
            scenes = [normalize_item(f, catalog=ep.name, needs_signing=ep.signing, readable=ep.can_read(sensor))
                      for f in feats]
            if max_cloud is not None and sensor == "S2":  # enforce client-side too: not every server honours `query`
                scenes = [s for s in scenes if s.cloud_cover is not None and s.cloud_cover <= max_cloud]
            self._cache[key] = scenes
            self.log.append({"endpoint": ep.name, "sensor": sensor, "cache_hit": False, "ok": True,
                             "items": len(scenes), "ms": round((time.monotonic() - t0) * 1000)})
            return list(scenes)
        raise StacError("; ".join(errors) or "no endpoints configured")
