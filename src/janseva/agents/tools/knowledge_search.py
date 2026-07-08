"""
Knowledge search tool — used by agents to query the knowledge base.
"""

import structlog

logger = structlog.get_logger()


def search_services(query: str) -> str:
    """
    Search the JanSeva knowledge base for government service information.

    Args:
        query: The user's question about a government service

    Returns:
        A formatted string with relevant knowledge base entries
    """
    try:
        from janseva.knowledge.vector_store import search_knowledge

        results = search_knowledge(query, k=3)
    except Exception as e:
        logger.warning(
            "knowledge_search_unavailable",
            error=str(e),
            query_preview=query[:50],
        )
        return "Knowledge base is not available. Please answer based on your general knowledge."

    if not results:
        return "No relevant information found in the knowledge base."

    context_parts = []
    for doc, score in results:
        # Require a minimum similarity to avoid hallucinating from irrelevant noise
        if score > 0.3:
            context_parts.append(
                f"--- Source: {doc.metadata.get('service_id', 'unknown')} "
                f"(relevance: {score:.2f}) ---\n"
                f"{doc.page_content}"
            )

    if not context_parts:
        return "No sufficiently relevant information found."

    return "\n\n".join(context_parts)
