# app/rag/state.py
from typing import List, Optional, TypedDict


class RagState(TypedDict, total=False):
    question: str
    context: List[str]
    answer: Optional[str]