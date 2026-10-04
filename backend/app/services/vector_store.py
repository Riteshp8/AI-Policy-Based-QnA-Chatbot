"""Tiny file-backed vector store (numpy). Swap for FAISS/Chroma if the corpus grows large."""
import json

import numpy as np

from app.core.config import settings

_cache: dict[int, tuple[np.ndarray, list[dict]]] = {}


def _dir():
    settings.vectorstore_dir.mkdir(parents=True, exist_ok=True)
    return settings.vectorstore_dir


def add_policy(policy_id: int, name: str, chunks: list[dict], vectors: np.ndarray) -> None:
    meta = [{**c, "document": name} for c in chunks]
    np.save(_dir() / f"{policy_id}.npy", vectors)
    (_dir() / f"{policy_id}.json").write_text(json.dumps(meta), encoding="utf-8")
    _cache[policy_id] = (vectors, meta)


def delete_policy(policy_id: int) -> None:
    for ext in ("npy", "json"):
        (_dir() / f"{policy_id}.{ext}").unlink(missing_ok=True)
    _cache.pop(policy_id, None)


def _load():
    for f in _dir().glob("*.npy"):
        pid, meta = int(f.stem), f.with_suffix(".json")
        if pid not in _cache and meta.exists():
            _cache[pid] = (np.load(f), json.loads(meta.read_text(encoding="utf-8")))
    return _cache


def search(qvec: np.ndarray, k: int) -> list[dict]:
    hits = []
    for vecs, meta in _load().values():
        scores = vecs @ qvec
        for i in np.argsort(-scores)[:k]:
            hits.append({**meta[int(i)], "score": float(scores[i])})
    return sorted(hits, key=lambda h: -h["score"])[:k]
