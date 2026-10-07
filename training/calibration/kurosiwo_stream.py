"""Stream samples from the Kuro Siwo GRD webdataset on Hugging Face (archive A041; CC BY 4.0) without
downloading whole 11 GB shards: each shard is read as a tar stream and closed after `n` samples."""
from __future__ import annotations

import io
import json
import tarfile
from typing import Iterator

import numpy as np

BASE = "https://huggingface.co/datasets/orion-ai-lab/Kuro-Siwo-Webdataset/resolve/main"
KEYS = ("flood_vv", "flood_vh", "sec1_vv", "sec1_vh", "mask", "valid_mask")


class _Stream(io.RawIOBase):
    def __init__(self, it):
        self.it, self.buf = it, b""

    def readable(self) -> bool:
        return True

    def readinto(self, b) -> int:
        while not self.buf:
            try:
                self.buf = next(self.it)
            except StopIteration:
                return 0
        n = min(len(b), len(self.buf))
        b[:n] = self.buf[:n]
        self.buf = self.buf[n:]
        return n


def _align_to_header(it, first: bytes = b"") -> Iterator[bytes]:
    """Skip bytes until a valid tar header block (512-aligned, checksum ok), then yield from there."""
    buf = first
    while True:
        while len(buf) < 512:
            buf += next(it)
        for off in range(0, len(buf) - 511, 512):
            try:
                tarfile.TarInfo.frombuf(buf[off:off + 512], tarfile.ENCODING, "surrogateescape")
            except tarfile.HeaderError:
                continue
            yield buf[off:]
            yield from it
            return
        buf = buf[(len(buf) // 512) * 512:]


def samples(shard: str, n: int, every: int = 1, offset: int = 0) -> Iterator[dict]:
    """Yield up to n complete samples from e.g. 'train_GRD/shard-00000.tar', keeping one in `every`.
    `offset` (bytes, rounded down to 512) starts the stream mid-shard with an HTTP range request, which
    reaches later flood events without reading the whole 11 GB shard; the first partial sample is skipped."""
    import httpx
    cur_key, cur, seen, kept = None, {}, 0, 0
    offset -= offset % 512
    headers = {"Range": f"bytes={offset}-"} if offset else {}
    with httpx.stream("GET", f"{BASE}/{shard}", follow_redirects=True, timeout=180, headers=headers) as r:
        r.raise_for_status()
        chunks = r.iter_bytes(1 << 20)
        if offset:
            chunks = _align_to_header(chunks)
        tf = tarfile.open(fileobj=io.BufferedReader(_Stream(chunks), 1 << 20), mode="r|")
        for m in tf:
            key, _, field = m.name.partition(".")
            field = field.rsplit(".", 1)[0]
            if key != cur_key:
                # a sample cut by the range start lacks some fields and is dropped by this check
                if cur_key is not None and all(k in cur for k in KEYS):
                    if seen % every == 0:
                        yield {"key": f"{shard}:{cur_key}", **cur}
                        kept += 1
                        if kept >= n:
                            return
                    seen += 1
                cur_key, cur = key, {}
            if field not in KEYS and field != "info":
                continue
            f = tf.extractfile(m)
            if f is None:
                continue
            data = f.read()
            cur[field] = json.loads(data) if field == "info" else np.load(io.BytesIO(data))[0]
