# app/schemas.py
from pydantic import BaseModel


class QuestionRequest(BaseModel):
    question: str


class DocumentRequest(BaseModel):
    text: str


# Optional response schemas (boleh dipakai atau tidak)
class AskResponse(BaseModel):
    question: str
    answer: str
    context_used: list[str]
    latency_sec: float


class AddResponse(BaseModel):
    id: str
    status: str


class StatusResponse(BaseModel):
    store_ready: bool
    docs_count: int
    graph_ready: bool
    store_kind: str