# app/rag/state.py
from typing import List, Optional, TypedDict


# Shared state contract for the LangGraph workflow
class RagState(TypedDict, total=False):
    question: str
    context: List[str]
    answer: Optional[str]
