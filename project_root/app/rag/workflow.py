# app/rag/workflow.py
from langgraph.graph import StateGraph, END

from app.rag.state import RagState
from app.stores.base import VectorStore
from app.services.embedder import Embedder


# Build the LangGraph workflow with injected dependencies (no module-level globals)
def build_workflow(
    store: VectorStore,
    embedder: Embedder,
    top_k: int,
    snippet_len: int,
):
    """
    Build and compile a LangGraph workflow.
    The compiled graph can be invoked with: {"question": "..."}.
    """

    # Retrieve context: embed question -> vector store search -> fill state["context"]
    def retrieve(state: RagState) -> RagState:
        query = state["question"]
        vector = embedder.embed(query)
        state["context"] = store.search(vector, top_k=top_k)
        return state

    # Answer: produce a short snippet from the best context match
    def answer(state: RagState) -> RagState:
        ctx = state.get("context", [])
        state["answer"] = (
            f"I found this: '{ctx[0][:snippet_len]}...'" if ctx else "Sorry, I don't know."
        )
        return state

    # Wire nodes into a simple retrieve -> answer flow
    workflow = StateGraph(RagState)
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("answer", answer)
    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "answer")
    workflow.add_edge("answer", END)

    return workflow.compile()
