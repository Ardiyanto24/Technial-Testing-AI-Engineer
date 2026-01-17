# app/services/rag_service.py
from typing import Any, List, Tuple


# Service wrapping the RAG workflow invocation
class RagService:
    def __init__(self, chain: Any):
        self.chain = chain

    # Run the RAG pipeline and return answer with context
    def ask(self, question: str) -> Tuple[str, List[str]]:
        result = self.chain.invoke({"question": question})
        answer = result.get("answer", "")
        context = result.get("context", [])
        return answer, context
