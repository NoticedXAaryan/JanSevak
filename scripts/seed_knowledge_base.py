"""
Seed the knowledge base vector store with all YAML service data.
Run: uv run python scripts/seed_knowledge_base.py
"""
import argparse
import sys
from pathlib import Path

# Add src to path so we can import janseva
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from janseva.common.logging import setup_logging
from janseva.knowledge.ingestion import ingest_all_services
from janseva.knowledge.vector_store import get_vector_store


def get_existing_document_count() -> int | None:
    """Return the Chroma collection count when available."""
    vector_store = get_vector_store()
    collection = getattr(vector_store, "_collection", None)
    if collection is None or not hasattr(collection, "count"):
        return None
    return int(collection.count())


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Seed the JanSeva knowledge base.")
    parser.add_argument(
        "--skip-if-populated",
        action="store_true",
        help="Exit successfully when the Chroma collection already has documents.",
    )
    args = parser.parse_args(argv)

    setup_logging()

    if args.skip_if_populated:
        existing_count = get_existing_document_count()
        if existing_count and existing_count > 0:
            print(f"Knowledge base already contains {existing_count} documents; skipping seed.")
            return

    print("Ingesting knowledge base data...")
    count = ingest_all_services()
    print(f"Successfully ingested {count} document chunks.")
    print("The knowledge base is ready for RAG queries.")


if __name__ == "__main__":
    main()
