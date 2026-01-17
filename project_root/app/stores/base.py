# app/stores/base.py
from abc import ABC, abstractmethod
from typing import List


# Base interface for vector storage implementations
class VectorStore(ABC):
    @abstractmethod
    def add(self, text: str, vector: List[float]) -> str:
        # Store a document and return its unique identifier
        raise NotImplementedError

    @abstractmethod
    def search(self, vector: List[float], top_k: int) -> List[str]:
        # Return top_k most similar document texts
        raise NotImplementedError

    @abstractmethod
    def count(self) -> int:
        # Return number of stored documents
        raise NotImplementedError

    @abstractmethod
    def is_ready(self) -> bool:
        # Indicate whether the store is available for use
        raise NotImplementedError
