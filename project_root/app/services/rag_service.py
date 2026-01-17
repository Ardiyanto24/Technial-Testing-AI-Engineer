# app/services/rag_service.py
from typing import Any, Dict, List, Tuple


class RagService:
    def __init__(self, chain: Any):
        self.chain = chain

    def ask(self, question: str) -> Tuple[str, List[str]]:
        result = self.chain.invoke({"question": question})
        answer = result.get("answer", "")
        context = result.get("context", [])
        return answer, context