# app/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    qdrant_url: str = "http://localhost:6333"
    collection_name: str = "demo_collection"

    vector_size: int = 128
    top_k: int = 2
    snippet_len: int = 100

    reset_collection: bool = False

    class Config:
        env_prefix = "RAG_"


def get_settings() -> Settings:
    return Settings()