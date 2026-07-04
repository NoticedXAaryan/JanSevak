"""
Knowledge base ingestion pipeline.
Loads YAML service/scheme files → converts to text chunks → embeds → stores in vector DB.
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
DATA_ROOT = Path(__file__).parent / "data"
SERVICES_DIR = DATA_ROOT / "services"
SCHEMES_DIR = DATA_ROOT / "schemes"
SUBSIDIES_DIR = DATA_ROOT / "subsidies"  # Legacy — kept for backwards compat
HEALTHCARE_DIR = DATA_ROOT / "healthcare"


def yaml_to_document(file_path: Path) -> List[Document]:
    """
    Convert a YAML service/scheme file into LangChain Document objects.
    Handles both service schema (service_id) and scheme schema (scheme_id).
    """
    with open(file_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not data:
        return []

    # Skip template files
    if data.get("service_id") == "unique_service_id":
        return []

    # Detect schema type
    is_scheme = "scheme_id" in data
    doc_id = data.get("scheme_id") or data.get("service_id") or file_path.stem

    texts = []

    if is_scheme:
        texts.extend(_scheme_to_documents(data, file_path, doc_id))
    else:
        texts.extend(_service_to_documents(data, file_path, doc_id))

    return texts


def _service_to_documents(data: dict, file_path: Path, doc_id: str) -> List[Document]:
    """Convert a service/document YAML to Document objects."""
    texts = []

    # Main description block
    main_text = f"""
Service: {data.get('name_en', '')} / {data.get('name_hi', '')}
Service ID: {doc_id}
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
            "service_id": doc_id,
            "type": "service_description",
            "tags": ", ".join(data.get("tags", [])),
        },
    ))

    # Required documents block
    docs_list = data.get("required_documents", [])
    if docs_list:
        docs_text = f"Required Documents for {data.get('name_en', '')} / {data.get('name_hi', '')}:\n\n"
        for i, doc in enumerate(docs_list, 1):
            doc_name_en = doc.get("name_en") or doc if isinstance(doc, str) else doc.get("name_en", "")
            doc_name_hi = doc.get("name_hi", "") if isinstance(doc, dict) else ""
            mandatory = "✅ Required" if (isinstance(doc, dict) and doc.get("mandatory")) else "⭕ Optional"
            docs_text += f"{i}. {doc_name_en}"
            if doc_name_hi:
                docs_text += f" / {doc_name_hi}"
            docs_text += f" — {mandatory}\n"
            if isinstance(doc, dict) and doc.get("note"):
                docs_text += f"   Note: {doc['note']}\n"

        texts.append(Document(
            page_content=docs_text.strip(),
            metadata={
                "source": str(file_path),
                "service_id": doc_id,
                "type": "required_documents",
            },
        ))

    # Process steps block
    steps = data.get("process_steps", [])
    if steps:
        steps_text = f"Process Steps for {data.get('name_en', '')} / {data.get('name_hi', '')}:\n\n"
        for step in steps:
            if isinstance(step, dict):
                steps_text += f"Step {step.get('step', '')}: {step.get('en', '')} / {step.get('hi', '')}\n"
            else:
                steps_text += f"• {step}\n"

        texts.append(Document(
            page_content=steps_text.strip(),
            metadata={
                "source": str(file_path),
                "service_id": doc_id,
                "type": "process_steps",
            },
        ))

    # Common mistakes block
    mistakes = data.get("common_mistakes", [])
    if mistakes:
        mistakes_text = f"Common Mistakes for {data.get('name_en', '')} / {data.get('name_hi', '')}:\n\n"
        for mistake in mistakes:
            if isinstance(mistake, dict):
                mistakes_text += f"• {mistake.get('en', '')} / {mistake.get('hi', '')}\n"
            else:
                mistakes_text += f"• {mistake}\n"

        texts.append(Document(
            page_content=mistakes_text.strip(),
            metadata={
                "source": str(file_path),
                "service_id": doc_id,
                "type": "common_mistakes",
            },
        ))

    # Online portals block
    portals = data.get("online_portals", [])
    if portals:
        portals_text = f"Online Portals for {data.get('name_en', '')} / {data.get('name_hi', '')}:\n\n"
        for portal in portals:
            if isinstance(portal, dict):
                portals_text += f"• {portal.get('state', '')}: {portal.get('url', '')}\n"
            else:
                portals_text += f"• {portal}\n"

        texts.append(Document(
            page_content=portals_text.strip(),
            metadata={
                "source": str(file_path),
                "service_id": doc_id,
                "type": "online_portals",
            },
        ))

    return texts


def _scheme_to_documents(data: dict, file_path: Path, doc_id: str) -> List[Document]:
    """Convert a scheme/subsidy YAML to Document objects."""
    texts = []

    # Main description
    main_text = f"""
Scheme: {data.get('name_en', '')} / {data.get('name_hi', '')}
Scheme ID: {doc_id}
Ministry: {data.get('ministry', '')}
Category: {data.get('category', '')}
Launched: {data.get('launched_year', '')}

Benefit: {data.get('benefit', '')}
Benefit (Hindi): {data.get('benefit_hi', '')}

Description (English):
{data.get('description_en', '')}

Description (Hindi):
{data.get('description_hi', '')}
""".strip()

    if data.get("official_website"):
        main_text += f"\nOfficial Website: {data['official_website']}"
    if data.get("helpline"):
        main_text += f"\nHelpline: {data['helpline']}"

    texts.append(Document(
        page_content=main_text,
        metadata={
            "source": str(file_path),
            "service_id": doc_id,
            "type": "scheme_description",
            "category": data.get("category", ""),
            "tags": ", ".join(data.get("tags", [])),
        },
    ))

    # Eligibility block
    eligibility = data.get("eligibility", [])
    eligibility_hi = data.get("eligibility_hi", [])
    if eligibility:
        elig_text = f"Eligibility for {data.get('name_en', '')}:\n\n"
        for i, criterion in enumerate(eligibility):
            elig_text += f"• {criterion}"
            if i < len(eligibility_hi):
                elig_text += f" / {eligibility_hi[i]}"
            elig_text += "\n"

        exclusions = data.get("exclusions", [])
        if exclusions:
            elig_text += "\nExclusions (who cannot avail):\n"
            for exc in exclusions:
                elig_text += f"• {exc}\n"

        if data.get("income_limit"):
            elig_text += f"\nIncome Limit: {data['income_limit']}"
        if data.get("age_limit"):
            elig_text += f"\nAge Limit: {data['age_limit']}"

        texts.append(Document(
            page_content=elig_text.strip(),
            metadata={
                "source": str(file_path),
                "service_id": doc_id,
                "type": "eligibility",
            },
        ))

    # Application process
    app_process = data.get("application_process", [])
    if app_process:
        app_text = f"How to Apply for {data.get('name_en', '')}:\n\n"
        for step in app_process:
            if isinstance(step, dict):
                app_text += f"Step {step.get('step', '')}: {step.get('en', '')} / {step.get('hi', '')}\n"
            else:
                app_text += f"• {step}\n"

        texts.append(Document(
            page_content=app_text.strip(),
            metadata={
                "source": str(file_path),
                "service_id": doc_id,
                "type": "application_process",
            },
        ))

    # Required documents (if present in scheme)
    docs_list = data.get("required_documents", [])
    if docs_list:
        docs_text = f"Required Documents for {data.get('name_en', '')}:\n\n"
        for i, doc in enumerate(docs_list, 1):
            if isinstance(doc, dict):
                doc_name = doc.get("name_en", "")
                doc_name_hi = doc.get("name_hi", "")
                docs_text += f"{i}. {doc_name}"
                if doc_name_hi:
                    docs_text += f" / {doc_name_hi}"
                docs_text += "\n"
            else:
                docs_text += f"{i}. {doc}\n"

        texts.append(Document(
            page_content=docs_text.strip(),
            metadata={
                "source": str(file_path),
                "service_id": doc_id,
                "type": "required_documents",
            },
        ))

    return texts


def _collect_yaml_files(*dirs: Path) -> List[Path]:
    """Collect all YAML files from multiple directories, skipping templates."""
    files = []
    for d in dirs:
        if not d.exists():
            continue
        for ext in ("*.yaml", "*.yml"):
            for f in d.glob(ext):
                if not f.name.startswith("_"):
                    files.append(f)
    return files


def ingest_all_services() -> int:
    """
    Load all YAML files from all data directories and ingest into vector store.
    Returns the number of documents ingested.
    """
    vector_store = get_vector_store()
    all_documents: List[Document] = []

    # Scan all data directories
    yaml_files = _collect_yaml_files(
        SERVICES_DIR, SCHEMES_DIR, SUBSIDIES_DIR, HEALTHCARE_DIR
    )

    logger.info("ingestion_starting", file_count=len(yaml_files))

    for file_path in yaml_files:
        try:
            docs = yaml_to_document(file_path)
            all_documents.extend(docs)
            logger.info("ingested_file", file=file_path.name, chunks=len(docs))
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

