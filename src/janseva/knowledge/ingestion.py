"""
Knowledge base ingestion pipeline.
Loads YAML service files → converts to text chunks → embeds → stores in vector DB.
"""
import glob
import structlog
import yaml
from pathlib import Path
from typing import List, Dict, Any

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from janseva.knowledge.vector_store import get_vector_store

logger = structlog.get_logger()

# Path to knowledge base data
SERVICES_DIR = Path(__file__).parent / "data" / "services"
SUBSIDIES_DIR = Path(__file__).parent / "data" / "subsidies"
HEALTHCARE_DIR = Path(__file__).parent / "data" / "healthcare"


def yaml_to_document(file_path: Path) -> List[Document]:
    """
    Convert a YAML service file into LangChain Document objects.
    Each document contains a human-readable text representation of the service.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not data or data.get("service_id") == "unique_service_id":
        return []  # Skip template files

    # Build a comprehensive text representation
    texts = []

    # Main description block
    main_text = f"""
Service: {data.get('name_en', '')} / {data.get('name_hi', '')}
Service ID: {data.get('service_id', '')}
Department: {data.get('department', '')}
Issuing Authority: {data.get('issuing_authority', '')}
Timeline: {data.get('estimated_timeline', 'varies')}
Fee: {data.get('approximate_fee', 'varies')}

Description (English):
{data.get('description_en', '')}

Description (Hindi):
{data.get('description_hi', '')}
""".strip()

    texts.append(Document(
        page_content=main_text,
        metadata={
            "source": str(file_path),
            "service_id": data.get("service_id", ""),
            "type": "service_description",
            "tags": ", ".join(data.get("tags", [])),
        },
    ))

    # Required documents block
    docs_list = data.get("required_documents", [])
    if docs_list:
        docs_text = f"Required Documents for {data['name_en']} / {data['name_hi']}:\n\n"
        for i, doc in enumerate(docs_list, 1):
            mandatory = "✅ Required" if doc.get("mandatory") else "⭕ Optional"
            docs_text += f"{i}. {doc.get('name_en', '')} / {doc.get('name_hi', '')} — {mandatory}\n"
            if doc.get("note"):
                docs_text += f"   Note: {doc['note']}\n"

        texts.append(Document(
            page_content=docs_text.strip(),
            metadata={
                "source": str(file_path),
                "service_id": data.get("service_id", ""),
                "type": "required_documents",
            },
        ))

    # Process steps block
    steps = data.get("process_steps", [])
    if steps:
        steps_text = f"Process Steps for {data['name_en']} / {data['name_hi']}:\n\n"
        for step in steps:
            steps_text += f"Step {step['step']}: {step.get('en', '')} / {step.get('hi', '')}\n"

        texts.append(Document(
            page_content=steps_text.strip(),
            metadata={
                "source": str(file_path),
                "service_id": data.get("service_id", ""),
                "type": "process_steps",
            },
        ))

    # Common mistakes block
    mistakes = data.get("common_mistakes", [])
    if mistakes:
        mistakes_text = f"Common Mistakes for {data['name_en']} / {data['name_hi']}:\n\n"
        for mistake in mistakes:
            mistakes_text += f"• {mistake.get('en', '')} / {mistake.get('hi', '')}\n"

        texts.append(Document(
            page_content=mistakes_text.strip(),
            metadata={
                "source": str(file_path),
                "service_id": data.get("service_id", ""),
                "type": "common_mistakes",
            },
        ))

    return texts


def ingest_all_services() -> int:
    """
    Load all YAML service files and ingest them into the vector store.
    Returns the number of documents ingested.
    """
    vector_store = get_vector_store()
    all_documents: List[Document] = []

    # Process service files
    service_files = list(SERVICES_DIR.glob("*.yaml")) + list(SERVICES_DIR.glob("*.yml"))
    for file_path in service_files:
        if file_path.name.startswith("_"):
            continue  # Skip template
        try:
            docs = yaml_to_document(file_path)
            all_documents.extend(docs)
            logger.info("ingested_service", file=file_path.name, chunks=len(docs))
        except Exception as e:
            logger.error("ingestion_error", file=file_path.name, error=str(e))

    if all_documents:
        # Split large documents into smaller chunks if needed
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
            separators=["\n\n", "\n", ". ", " "],
        )
        split_docs = splitter.split_documents(all_documents)

        # Add to vector store
        vector_store.add_documents(split_docs)
        logger.info("ingestion_complete", total_documents=len(split_docs))
        return len(split_docs)

    logger.warning("no_documents_found")
    return 0


if __name__ == "__main__":
    """Run directly to ingest: uv run python -m janseva.knowledge.ingestion"""
    from janseva.common.logging import setup_logging
    setup_logging()
    count = ingest_all_services()
    print(f"Ingested {count} document chunks into the vector store.")
