# app/schemas.py
from pydantic import BaseModel


# Request schema for /ask endpoint
class QuestionRequest(BaseModel):
    question: str


# Request schema for /add endpoint
class DocumentRequest(BaseModel):
    text: str


# Response schema for /ask
class AskResponse(BaseModel):
    question: str
    answer: str
    context_used: list[str]
    latency_sec: float


# Response schema for /add
class AddResponse(BaseModel):
    id: str
    status: str


# Response schema for /status
class StatusResponse(BaseModel):
    store_ready: bool
    docs_count: int
    graph_ready: bool
    store_kind: str
