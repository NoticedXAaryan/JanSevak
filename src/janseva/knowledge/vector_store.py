"""
Vector store interface for RAG.
Uses ChromaDB for development. Can be swapped to pgvector for production.
"""

from pathlib import Path
from typing import Any

import structlog

from janseva.config import settings

logger = structlog.get_logger()

# Persistent storage for ChromaDB
CHROMA_PERSIST_DIR = Path(__file__).parent.parent.parent.parent / ".chromadb"

_vector_store: Any | None = None


def get_embeddings() -> Any:
    """Get the embedding model based on LLM provider."""
    provider = settings.embedding_provider.lower()

    if provider in {"gemini", "google"}:
        if not settings.google_api_key:
            raise ValueError("GOOGLE_API_KEY is required when EMBEDDING_PROVIDER=gemini")

        from langchain_google_genai import GoogleGenerativeAIEmbeddings

        return GoogleGenerativeAIEmbeddings(
            model=settings.embedding_model or "models/embedding-001",
            google_api_key=settings.google_api_key,
        )

    if provider == "ollama":
        from langchain_community.embeddings import OllamaEmbeddings

        return OllamaEmbeddings(
            model=settings.embedding_model or "nomic-embed-text",
            base_url=settings.ollama_base_url,
        )

    if provider == "huggingface":
        from langchain_community.embeddings import HuggingFaceEmbeddings
        
        return HuggingFaceEmbeddings(
            model_name=settings.embedding_model or "sentence-transformers/all-MiniLM-L6-v2"
        )

    raise ValueError(
        f"Unknown embedding provider: {settings.embedding_provider}. "
        "Set EMBEDDING_PROVIDER to 'gemini' or 'ollama'."
    )


def get_vector_store() -> Any:
    """
    Get or create the ChromaDB vector store singleton.
    Uses persistent storage so embeddings survive restarts.
    """
    global _vector_store
    if _vector_store is None:
        from langchain_community.vectorstores import Chroma

        _vector_store = Chroma(
            collection_name="janseva_knowledge",
            embedding_function=get_embeddings(),
            persist_directory=str(CHROMA_PERSIST_DIR),
        )
        logger.info("vector_store_initialized", persist_dir=str(CHROMA_PERSIST_DIR))
    return _vector_store


def search_knowledge(query: str, k: int = 5) -> list:
    """
    Search the knowledge base for documents relevant to the query.

    Args:
        query: The user's question
        k: Number of results to return

    Returns:
        List of (Document, score) tuples, most relevant first
    """
    store = get_vector_store()
    results = store.similarity_search_with_relevance_scores(query, k=k)
    logger.info(
        "knowledge_search",
        query_preview=query[:50],
        results_count=len(results),
        top_score=results[0][1] if results else 0.0,
    )
    return results
