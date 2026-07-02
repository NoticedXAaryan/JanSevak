"""
Vector store interface for RAG.
Uses ChromaDB for development. Can be swapped to pgvector for production.
"""
import structlog
from pathlib import Path

from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.embeddings import OllamaEmbeddings

from janseva.config import settings

logger = structlog.get_logger()

# Persistent storage for ChromaDB
CHROMA_PERSIST_DIR = Path(__file__).parent.parent.parent.parent / ".chromadb"

_vector_store = None


def get_embeddings():
    """Get the embedding model based on LLM provider."""
    if settings.llm_provider == "gemini":
        return GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=settings.google_api_key,
        )
    elif settings.llm_provider == "openrouter":
        # Let's use text-embedding-3-small via openrouter if available or fallback
        # Wait, OpenRouter doesn't host an embedding model directly in a way that matches OpenAI's embedding API.
        # So typically we just use Ollama locally or HuggingFace for embeddings when using OpenRouter.
        # I'll default to HuggingFace embeddings for a free robust option
        from langchain_huggingface import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    elif settings.llm_provider == "ollama":
        return OllamaEmbeddings(
            model="nomic-embed-text",  # Good multilingual embedding model
            base_url=settings.ollama_base_url,
        )
    else:
        raise ValueError(f"Unknown LLM provider: {settings.llm_provider}")


def get_vector_store() -> Chroma:
    """
    Get or create the ChromaDB vector store singleton.
    Uses persistent storage so embeddings survive restarts.
    """
    global _vector_store
    if _vector_store is None:
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
