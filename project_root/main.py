# main.py
from fastapi import FastAPI
from app.config import get_settings
from app.services.embedder import Embedder
from app.api import create_router
from app.dependencies import create_store, create_services

app = FastAPI(title="Learning RAG Demo")
settings = get_settings()

# router bisa di-include sekarang karena handler ambil dependency dari app.state saat request
app.include_router(create_router())

@app.on_event("startup")
def on_startup():
    # 1) init embedder
    embedder = Embedder(vector_size=settings.vector_size)

    # 2) init store (qdrant -> fallback memory)
    store, store_kind = create_store(settings)

    # 3) init workflow + services
    chain, doc_service, rag_service = create_services(store, embedder, settings)

    # 4) save to app.state (no module-level globals)
    app.state.embedder = embedder
    app.state.store = store
    app.state.store_kind = store_kind
    app.state.chain = chain
    app.state.doc_service = doc_service
    app.state.rag_service = rag_service