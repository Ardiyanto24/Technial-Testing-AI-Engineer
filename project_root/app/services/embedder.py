# app/services/embedder.py
import hashlib
import random
from typing import List


# Simple deterministic embedder (stable across restarts)
class Embedder:
    def __init__(self, vector_size: int = 128):
        self.vector_size = vector_size

    # Generate a stable seed from input text
    def _stable_seed(self, text: str) -> int:
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        return int.from_bytes(digest[:8], "big", signed=False)

    # Produce a pseudo-embedding vector for the given text
    def embed(self, text: str) -> List[float]:
        seed = self._stable_seed(text)
        rng = random.Random(seed)  # Local RNG to avoid global side effects
        return [rng.random() for _ in range(self.vector_size)]
