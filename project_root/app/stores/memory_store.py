# app/stores/memory_store.py
from typing import List, Tuple
from uuid import uuid4
import math

from app.stores.base import VectorStore


def _cosine_similarity(a: List[float], b: List[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


class MemoryStore(VectorStore):
    def __init__(self):
        self._items: List[Tuple[str, str, List[float]]] = []  # (id, text, vector)

    def add(self, text: str, vector: List[float]) -> str:
        doc_id = str(uuid4())
        self._items.append((doc_id, text, vector))
        return doc_id

    def search(self, vector: List[float], top_k: int) -> List[str]:
        scored = [
            (_cosine_similarity(vector, v), text)
            for (_id, text, v) in self._items
        ]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [text for score, text in scored[:top_k] if score > 0]

    def count(self) -> int:
        return len(self._items)

    def is_ready(self) -> bool:
        return True