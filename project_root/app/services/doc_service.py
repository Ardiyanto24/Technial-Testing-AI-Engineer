# app/services/doc_service.py
from app.services.embedder import Embedder
from app.stores.base import VectorStore


# Service responsible for adding documents into the vector store
class DocService:
    def __init__(self, store: VectorStore, embedder: Embedder):
        self.store = store
        self.embedder = embedder

    # Embed text and persist it into the store
    def add_document(self, text: str) -> str:
        vector = self.embedder.embed(text)
        doc_id = self.store.add(text, vector)
        return doc_id
