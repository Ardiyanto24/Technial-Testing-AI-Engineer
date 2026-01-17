# main.py
from fastapi import FastAPI
from app.config import get_settings
from app.services.embedder import Embedder
from app.api import create_router
from app.dependencies import create_store, create_services

app = FastAPI(title="Learning RAG Demo")
settings = get_settings()

# Register API routes (dependencies are resolved from app.state per request)
app.include_router(create_router())

@app.on_event("startup")
def on_startup():
    # Initialize runtime dependencies at startup (avoid module-level globals)
    embedder = Embedder(vector_size=settings.vector_size)

    # Prefer Qdrant; fall back to in-memory store if unavailable
    store, store_kind = create_store(settings)

    # Build workflow + service layer
    chain, doc_service, rag_service = create_services(store, embedder, settings)

    # Store dependencies in app.state for API handlers
    app.state.embedder = embedder
    app.state.store = store
    app.state.store_kind = store_kind
    app.state.chain = chain
    app.state.doc_service = doc_service
    app.state.rag_service = rag_service
