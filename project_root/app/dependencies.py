# app/dependencies.py
from app.config import Settings
from app.services.embedder import Embedder
from app.stores.qdrant_store import QdrantStore
from app.stores.memory_store import MemoryStore
from app.services.doc_service import DocService
from app.services.rag_service import RagService
from app.rag.workflow import build_workflow


# Create vector store with graceful fallback
def create_store(settings: Settings):
    """
    Try QdrantStore first.
    If unavailable, fall back to in-memory store.
    """
    try:
        store = QdrantStore(
            url=settings.qdrant_url,
            collection_name=settings.collection_name,
            vector_size=settings.vector_size,
            reset_collection=settings.reset_collection,
        )
        return store, "qdrant"
    except Exception:
        store = MemoryStore()
        return store, "memory"


# Wire workflow and service layer
def create_services(store, embedder, settings):
    chain = build_workflow(
        store=store,
        embedder=embedder,
        top_k=settings.top_k,
        snippet_len=settings.snippet_len,
    )

    doc_service = DocService(store=store, embedder=embedder)
    rag_service = RagService(chain=chain)

    return chain, doc_service, rag_service
