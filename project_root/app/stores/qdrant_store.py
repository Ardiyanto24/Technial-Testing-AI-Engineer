# app/stores/qdrant_store.py
from typing import List
from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

from app.stores.base import VectorStore


# Qdrant-backed vector store implementation
class QdrantStore(VectorStore):
    def __init__(
        self,
        url: str,
        collection_name: str,
        vector_size: int,
        distance: Distance = Distance.COSINE,
        reset_collection: bool = False,
    ):
        self.url = url
        self.collection_name = collection_name
        self.vector_size = vector_size
        self.distance = distance
        self.reset_collection = reset_collection

        # Initialize Qdrant client
        self.client = QdrantClient(url)
        self._ensure_collection()

    def _ensure_collection(self) -> None:
        # Optionally reset collection (demo/testing only)
        if self.reset_collection:
            try:
                self.client.delete_collection(self.collection_name)
            except Exception:
                pass

        # Create collection if it does not exist
        try:
            self.client.get_collection(self.collection_name)
        except Exception:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=self.distance,
                ),
            )

    def add(self, text: str, vector: List[float]) -> str:
        # Store document with a UUID identifier
        doc_id = str(uuid4())
        self.client.upsert(
            collection_name=self.collection_name,
            points=[PointStruct(id=doc_id, vector=vector, payload={"text": text})],
        )
        return doc_id

    def search(self, vector: List[float], top_k: int) -> List[str]:
        # Query Qdrant for nearest vectors
        hits = self.client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            limit=top_k,
        )
        return [hit.payload.get("text", "") for hit in hits]

    def count(self) -> int:
        # Return total number of stored points
        try:
            res = self.client.count(
                collection_name=self.collection_name,
                exact=True,
            )
            return int(res.count)
        except Exception:
            # Fallback when count API is unavailable
            return 0

    def is_ready(self) -> bool:
        # Check collection availability
        try:
            self.client.get_collection(self.collection_name)
            return True
        except Exception:
            return False
