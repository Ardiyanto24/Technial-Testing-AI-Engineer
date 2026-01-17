# app/config.py
from pydantic_settings import BaseSettings


# Application configuration loaded from environment variables
class Settings(BaseSettings):
    qdrant_url: str = "http://localhost:6333"
    collection_name: str = "demo_collection"

    vector_size: int = 128
    top_k: int = 2
    snippet_len: int = 100

    reset_collection: bool = False

    # Prefix for environment variables (e.g. RAG_QDRANT_URL)
    class Config:
        env_prefix = "RAG_"


# Helper to construct Settings instance
def get_settings() -> Settings:
    return Settings()
