# app/api.py
import time
from fastapi import APIRouter, HTTPException, Request

from app.schemas import (
    QuestionRequest,
    DocumentRequest,
    AskResponse,
    AddResponse,
    StatusResponse,
)

def create_router() -> APIRouter:
    router = APIRouter()

    @router.post("/ask", response_model=AskResponse)
    def ask_question(req: QuestionRequest, request: Request):
        question = (req.question or "").strip()
        if not question:
            raise HTTPException(status_code=400, detail="Question must not be empty.")

        store = request.app.state.store
        rag_service = request.app.state.rag_service

        if not store.is_ready():
            raise HTTPException(status_code=503, detail="Vector store is not ready.")

        start = time.time()
        try:
            answer, context = rag_service.ask(question)
            return {
                "question": question,
                "answer": answer,
                "context_used": context,
                "latency_sec": round(time.time() - start, 3),
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/add", response_model=AddResponse)
    def add_document(req: DocumentRequest, request: Request):
        text = (req.text or "").strip()
        if not text:
            raise HTTPException(status_code=400, detail="Text must not be empty.")

        store = request.app.state.store
        doc_service = request.app.state.doc_service

        if not store.is_ready():
            raise HTTPException(status_code=503, detail="Vector store is not ready.")

        try:
            doc_id = doc_service.add_document(text)
            return {"id": doc_id, "status": "added"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/status", response_model=StatusResponse)
    def status(request: Request):
        store = request.app.state.store
        chain = request.app.state.chain
        store_kind = getattr(request.app.state, "store_kind", "unknown")

        return {
            "store_ready": store.is_ready(),
            "docs_count": store.count(),
            "graph_ready": chain is not None,
            "store_kind": store_kind,  # opsional: jujur pakai qdrant/memory
        }

    return router