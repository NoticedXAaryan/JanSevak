"""
Seed the knowledge base vector store with all YAML service data.
Run: uv run python scripts/seed_knowledge_base.py
"""
import sys
from pathlib import Path

# Add src to path so we can import janseva
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from janseva.common.logging import setup_logging
from janseva.knowledge.ingestion import ingest_all_services


def main():
    setup_logging()
    print("Ingesting knowledge base data...")
    count = ingest_all_services()
    print(f"Successfully ingested {count} document chunks.")
    print("The knowledge base is ready for RAG queries.")


if __name__ == "__main__":
    main()
