# app/services/embedder.py
import hashlib
import random
from typing import List


class Embedder:
    def __init__(self, vector_size: int = 128):
        self.vector_size = vector_size

    def _stable_seed(self, text: str) -> int:
        # sha256 menghasilkan output stabil lintas restart
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        # ambil 8 bytes pertama jadi integer seed (cukup besar & stabil)
        return int.from_bytes(digest[:8], "big", signed=False)

    def embed(self, text: str) -> List[float]:
        seed = self._stable_seed(text)
        rng = random.Random(seed)  # RNG lokal (tidak ganggu random global)
        return [rng.random() for _ in range(self.vector_size)]