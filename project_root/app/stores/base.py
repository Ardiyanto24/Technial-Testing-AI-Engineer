# app/stores/base.py
from abc import ABC, abstractmethod
from typing import List


class VectorStore(ABC):
    @abstractmethod
    def add(self, text: str, vector: List[float]) -> str:
        """Store a document and return its doc_id."""
        raise NotImplementedError

    @abstractmethod
    def search(self, vector: List[float], top_k: int) -> List[str]:
        """Return list of texts (top_k most similar)."""
        raise NotImplementedError

    @abstractmethod
    def count(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def is_ready(self) -> bool:
        raise NotImplementedError