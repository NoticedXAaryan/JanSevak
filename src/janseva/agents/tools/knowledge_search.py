"""
Knowledge search tool — used by agents to query the knowledge base.
"""


def search_services(query: str) -> str:
    """
    Search the JanSeva knowledge base for government service information.

    Args:
        query: The user's question about a government service

    Returns:
        A formatted string with relevant knowledge base entries
    """
    from janseva.knowledge.vector_store import search_knowledge

    results = search_knowledge(query, k=3)

    if not results:
        return "No relevant information found in the knowledge base."

    context_parts = []
    for doc, score in results:
        if score > 0.0:
            context_parts.append(
                f"--- Source: {doc.metadata.get('service_id', 'unknown')} "
                f"(relevance: {score:.2f}) ---\n"
                f"{doc.page_content}"
            )

    if not context_parts:
        return "No sufficiently relevant information found."

    return "\n\n".join(context_parts)
