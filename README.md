# 🧩 Code Quality Exercise — Refactored RAG Service

For Associate Software Engineer Candidates

---

## 📌 Overview

This repository contains a refactored version of a small Python application implementing a simple **Retrieval-Augmented Generation (RAG)** service using:

- FastAPI  
- LangGraph  
- Qdrant (with in-memory fallback)

The original implementation was provided as a single working file, intentionally containing common structural issues such as global state, tight coupling, and limited separation of concerns.

The goal of this refactor is **not to add new features**, but to reorganize the code into a **cleaner, more maintainable, and production-suitable structure**, while preserving the original behavior.

---

## 🎯 Refactoring Goals

This refactored version focuses on improving code quality through:

- **Encapsulation**  
  Related responsibilities are grouped into cohesive classes and modules.

- **Separation of concerns**  
  Web/API handling, business logic, workflow orchestration, and storage access are clearly separated.

- **Explicit dependencies**  
  Global state is avoided; dependencies are constructed explicitly and injected where needed.

- **Testability by design**  
  Although unit tests are not implemented, the code is structured so individual components (services, stores, workflow) can be tested in isolation.

- **Readability & maintainability**  
  The project is organized into logical folders with clear naming and minimal hidden behavior.


---

## ▶️ Running the Application
1. Create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\activate   # Windows

2. Install dependencies
pip install fastapi uvicorn pydantic pydantic-settings qdrant-client langgraph

3. Start the server
uvicorn main:app --reload

The API will be available at:
http://127.0.0.1:8000
Swagger UI: http://127.0.0.1:8000/docs
---

## 🗂 Project Structure

```text
project_root/
├── main.py                 # Application entry point & lifecycle management
├── app/
│   ├── api.py              # HTTP routes (thin API layer)
│   ├── config.py           # Centralized configuration
│   ├── dependencies.py     # Dependency construction & wiring
│   ├── schemas.py          # Request / response models
│   ├── rag/
│   │   ├── state.py        # LangGraph state contract
│   │   └── workflow.py    # RAG workflow builder
│   ├── services/
│   │   ├── embedder.py     # Deterministic embedding service
│   │   ├── doc_service.py # Document ingestion logic
│   │   └── rag_service.py # RAG execution service
│   └── stores/
│       ├── base.py         # VectorStore interface
│       ├── memory_store.py # In-memory fallback store
│       └── qdrant_store.py # Qdrant-backed store
└── notes.md                # Design decisions & trade-offs
