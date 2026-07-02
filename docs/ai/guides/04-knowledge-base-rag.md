# Guide 04: Knowledge Base & RAG (Retrieval-Augmented Generation)

## What This Does
Builds the knowledge base system that gives JanSeva accurate, up-to-date information about government services. Instead of relying solely on the LLM's training data (which may be outdated or inaccurate), RAG retrieves relevant information from our curated knowledge base before generating a response.

## Prerequisites
- Guide 01 completed (project setup)
- Guide 03 completed (AI agent core working)

---

## Concept: How RAG Works in JanSeva

```
User asks: "आय प्रमाण पत्र कैसे बनाएं?"
    │
    ▼
1. EMBED the question → vector representation
    │
    ▼
2. SEARCH the vector store for similar documents
    │
    ▼
3. RETRIEVE top 3-5 matching knowledge base entries
    │
    ▼
4. AUGMENT the LLM prompt with retrieved context
    │
    ▼
5. GENERATE response using LLM + retrieved knowledge
```

---

## Files to Create

### 1. Knowledge Base Data Files (YAML)

These are the curated government service descriptions. Start with a few, add more over time.

**File: `src/janseva/knowledge/data/services/income_certificate.yaml`**

```yaml
service_id: income_certificate
name_en: Income Certificate
name_hi: आय प्रमाण पत्र
department: Revenue Department / राजस्व विभाग
issuing_authority: Sub-Divisional Magistrate (SDM) / उप-जिलाधिकारी
applicable_states:
  - all  # Most states follow similar process

description_en: |
  An Income Certificate is an official document issued by the state government
  that certifies the annual income of an individual or family. It is commonly
  required for admission to educational institutions, scholarships, government
  job applications, subsidized services, and various government schemes.

description_hi: |
  आय प्रमाण पत्र राज्य सरकार द्वारा जारी एक आधिकारिक दस्तावेज है जो किसी
  व्यक्ति या परिवार की वार्षिक आय को प्रमाणित करता है। यह शैक्षणिक संस्थानों
  में प्रवेश, छात्रवृत्ति, सरकारी नौकरी के आवेदन, सब्सिडी वाली सेवाओं और
  विभिन्न सरकारी योजनाओं के लिए आवश्यक है।

required_documents:
  - name_en: "Aadhaar Card"
    name_hi: "आधार कार्ड"
    mandatory: true

  - name_en: "Ration Card"
    name_hi: "राशन कार्ड"
    mandatory: true

  - name_en: "Self-declaration / Affidavit of income"
    name_hi: "आय का स्व-घोषणा पत्र / शपथ पत्र"
    mandatory: true

  - name_en: "Salary slip (for employed individuals)"
    name_hi: "वेतन पर्ची (नौकरीपेशा लोगों के लिए)"
    mandatory: false
    note: "Required if employed. Self-employed can provide business income proof."

  - name_en: "Form 16 / ITR (Income Tax Return)"
    name_hi: "फॉर्म 16 / आयकर रिटर्न"
    mandatory: false
    note: "If available, strengthens the application."

  - name_en: "Passport-size photographs (2)"
    name_hi: "पासपोर्ट साइज फोटो (2)"
    mandatory: true

  - name_en: "Application form (available at Tehsil office or online portal)"
    name_hi: "आवेदन पत्र (तहसील कार्यालय या ऑनलाइन पोर्टल पर उपलब्ध)"
    mandatory: true

process_steps:
  - step: 1
    en: "Collect all required documents listed above."
    hi: "ऊपर सूचीबद्ध सभी आवश्यक दस्तावेज इकट्ठा करें।"

  - step: 2
    en: "Visit the Tehsil or SDM office, or apply online through your state's e-District portal."
    hi: "तहसील या SDM कार्यालय जाएं, या अपने राज्य के ई-जिला पोर्टल के माध्यम से ऑनलाइन आवेदन करें।"

  - step: 3
    en: "Fill the application form and attach all documents."
    hi: "आवेदन पत्र भरें और सभी दस्तावेज संलग्न करें।"

  - step: 4
    en: "Submit the application. You will receive an acknowledgment receipt."
    hi: "आवेदन जमा करें। आपको एक पावती रसीद मिलेगी।"

  - step: 5
    en: "A field verification may be conducted by the Patwari/Lekhpal."
    hi: "पटवारी/लेखपाल द्वारा क्षेत्रीय सत्यापन किया जा सकता है।"

  - step: 6
    en: "Certificate is issued within 7-15 working days (varies by state)."
    hi: "प्रमाण पत्र 7-15 कार्य दिवसों में जारी किया जाता है (राज्य के अनुसार भिन्न)।"

estimated_timeline: "7-15 working days"
approximate_fee: "INR 10-50 (varies by state)"
online_portals:
  - state: "Uttar Pradesh"
    url: "https://edistrict.up.gov.in"
  - state: "Madhya Pradesh"
    url: "https://mpedistrict.gov.in"
  - state: "Bihar"
    url: "https://serviceonline.bihar.gov.in"
  - state: "Rajasthan"
    url: "https://emitra.rajasthan.gov.in"

common_mistakes:
  - en: "Not getting the income affidavit notarized"
    hi: "आय शपथ पत्र को नोटरी नहीं करवाना"
  - en: "Submitting expired or unclear photocopies"
    hi: "समय सीमा समाप्त या अस्पष्ट फोटोकॉपी जमा करना"
  - en: "Mismatch between Aadhaar name and application name"
    hi: "आधार में नाम और आवेदन में नाम का मेल न खाना"

tags:
  - income
  - certificate
  - revenue
  - SDM
  - scholarship
  - government_scheme
```

**File: `src/janseva/knowledge/data/services/caste_certificate.yaml`**

```yaml
service_id: caste_certificate
name_en: Caste Certificate
name_hi: जाति प्रमाण पत्र
department: Revenue Department / राजस्व विभाग
issuing_authority: Sub-Divisional Magistrate (SDM) / उप-जिलाधिकारी

description_en: |
  A Caste Certificate is an official document that certifies a person belongs
  to a specific Scheduled Caste (SC), Scheduled Tribe (ST), or Other Backward
  Class (OBC). Required for reservations in education, government jobs, and
  various welfare schemes.

description_hi: |
  जाति प्रमाण पत्र एक आधिकारिक दस्तावेज है जो प्रमाणित करता है कि व्यक्ति
  एक विशिष्ट अनुसूचित जाति (SC), अनुसूचित जनजाति (ST), या अन्य पिछड़ा
  वर्ग (OBC) से संबंधित है। शिक्षा, सरकारी नौकरियों और विभिन्न कल्याणकारी
  योजनाओं में आरक्षण के लिए आवश्यक है।

required_documents:
  - name_en: "Aadhaar Card"
    name_hi: "आधार कार्ड"
    mandatory: true

  - name_en: "Father's/Grandfather's Caste Certificate (if available)"
    name_hi: "पिता/दादा का जाति प्रमाण पत्र (यदि उपलब्ध हो)"
    mandatory: false
    note: "Strongly recommended. Speeds up verification."

  - name_en: "School/College records mentioning caste"
    name_hi: "जाति का उल्लेख करने वाले स्कूल/कॉलेज रिकॉर्ड"
    mandatory: false

  - name_en: "Voter ID Card"
    name_hi: "मतदाता पहचान पत्र"
    mandatory: true

  - name_en: "Ration Card"
    name_hi: "राशन कार्ड"
    mandatory: true

  - name_en: "Affidavit / Self-declaration on stamp paper"
    name_hi: "स्टाम्प पेपर पर शपथ पत्र / स्व-घोषणा"
    mandatory: true

  - name_en: "Passport-size photographs (2)"
    name_hi: "पासपोर्ट साइज फोटो (2)"
    mandatory: true

process_steps:
  - step: 1
    en: "Collect all required documents."
    hi: "सभी आवश्यक दस्तावेज इकट्ठा करें।"

  - step: 2
    en: "Get an affidavit prepared on stamp paper (INR 10-100) from a notary."
    hi: "नोटरी से स्टाम्प पेपर (₹10-100) पर शपथ पत्र तैयार करवाएं।"

  - step: 3
    en: "Visit the Tehsil/SDM office or apply online via e-District portal."
    hi: "तहसील/SDM कार्यालय जाएं या ई-जिला पोर्टल से ऑनलाइन आवेदन करें।"

  - step: 4
    en: "Submit the application with all documents."
    hi: "सभी दस्तावेजों के साथ आवेदन जमा करें।"

  - step: 5
    en: "Field verification will be conducted by revenue officials."
    hi: "राजस्व अधिकारियों द्वारा क्षेत्रीय सत्यापन किया जाएगा।"

  - step: 6
    en: "Certificate issued within 15-30 working days."
    hi: "15-30 कार्य दिवसों में प्रमाण पत्र जारी।"

estimated_timeline: "15-30 working days"
approximate_fee: "INR 10-100 (varies by state)"

tags:
  - caste
  - certificate
  - SC
  - ST
  - OBC
  - reservation
  - revenue
```

Create similar YAML files for other services. Here's a minimal template:

**File: `src/janseva/knowledge/data/services/_template.yaml`**

```yaml
# Copy this template to create new service entries.
# File name should be: <service_name_snake_case>.yaml

service_id: unique_service_id
name_en: Service Name in English
name_hi: सेवा का नाम हिंदी में
department: Department Name
issuing_authority: Authority Name

description_en: |
  English description of the service.

description_hi: |
  हिंदी में सेवा का विवरण।

required_documents:
  - name_en: "Document Name"
    name_hi: "दस्तावेज का नाम"
    mandatory: true

process_steps:
  - step: 1
    en: "Step description in English"
    hi: "चरण का विवरण हिंदी में"

estimated_timeline: "X working days"
approximate_fee: "INR X-Y"

tags:
  - tag1
  - tag2
```

---

### 2. Document Ingestion Pipeline

**File: `src/janseva/knowledge/ingestion.py`**

```python
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
            "tags": data.get("tags", []),
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
```

---

### 3. Vector Store Interface

**File: `src/janseva/knowledge/vector_store.py`**

```python
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
```

---

### 4. Knowledge Search Tool (for Agents)

**File: `src/janseva/agents/tools/knowledge_search.py`**

```python
"""
Knowledge search tool — used by agents to query the knowledge base.
"""
from janseva.knowledge.vector_store import search_knowledge


def search_services(query: str) -> str:
    """
    Search the JanSeva knowledge base for government service information.
    
    Args:
        query: The user's question about a government service
        
    Returns:
        A formatted string with relevant knowledge base entries
    """
    results = search_knowledge(query, k=3)
    
    if not results:
        return "No relevant information found in the knowledge base."
    
    context_parts = []
    for doc, score in results:
        if score > 0.3:  # Only include sufficiently relevant results
            context_parts.append(
                f"--- Source: {doc.metadata.get('service_id', 'unknown')} "
                f"(relevance: {score:.2f}) ---\n"
                f"{doc.page_content}"
            )
    
    if not context_parts:
        return "No sufficiently relevant information found."
    
    return "\n\n".join(context_parts)
```

---

### 5. Update Service Navigator to Use RAG

**File: `src/janseva/agents/specialists/service_navigator.py`** — REPLACE entire file:

```python
"""
Service Navigator Agent — Enhanced with RAG.
Retrieves relevant knowledge base entries and uses them to provide
accurate, sourced answers about government services.
"""
from langchain_core.messages import SystemMessage
from janseva.agents.llm import get_llm
from janseva.agents.tools.knowledge_search import search_services


SERVICE_RAG_PROMPT = """You are JanSeva (जनसेवा), an expert AI assistant for Indian government services.

You have access to a curated knowledge base about government services.
Below is relevant information retrieved from the knowledge base for this query:

--- KNOWLEDGE BASE CONTEXT ---
{knowledge_context}
--- END CONTEXT ---

RULES:
1. ALWAYS respond in the SAME LANGUAGE the user used (Hindi, English, or mixed).
2. Use the knowledge base context above as your PRIMARY source of information.
3. If the context contains specific requirements, list them exactly as documented.
4. If the context doesn't cover the question, say so clearly and suggest checking locally.
5. NEVER fabricate specific addresses, phone numbers, or fees not in the context.
6. Format with bullet points and numbered lists for clarity.
7. Include both Hindi and English names when available in the context.

User's language: {user_language}
User's district: {user_district}"""


def handle_service_query(state: dict) -> dict:
    """
    Process a government service query using RAG.
    
    1. Search the knowledge base for relevant information
    2. Augment the LLM prompt with retrieved context
    3. Generate a response grounded in the knowledge base
    """
    llm = get_llm()
    user_language = state.get("user_language", "hi")
    user_district = state.get("user_district", "unknown")
    
    # Get the latest user message
    latest_message = state["messages"][-1].content if state["messages"] else ""
    
    # RAG: Search knowledge base
    knowledge_context = search_services(latest_message)
    
    # Build the prompt with retrieved context
    system_msg = SystemMessage(content=SERVICE_RAG_PROMPT.format(
        knowledge_context=knowledge_context,
        user_language=user_language,
        user_district=user_district,
    ))
    
    # Include recent conversation for context
    recent_messages = list(state["messages"][-6:])
    all_messages = [system_msg] + recent_messages
    
    response = llm.invoke(all_messages)
    
    return {"response": response.content}
```

---

### 6. Seed Script for Knowledge Base

**File: `scripts/seed_knowledge_base.py`**

```python
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
    print("🔄 Ingesting knowledge base data...")
    count = ingest_all_services()
    print(f"✅ Successfully ingested {count} document chunks.")
    print("The knowledge base is ready for RAG queries.")


if __name__ == "__main__":
    main()
```

---

## Running the Ingestion

```bash
# Make sure you have at least the income_certificate.yaml and caste_certificate.yaml files
# Then run:
uv run python scripts/seed_knowledge_base.py
```

Expected output:
```
🔄 Ingesting knowledge base data...
ingested_service file=income_certificate.yaml chunks=4
ingested_service file=caste_certificate.yaml chunks=3
ingestion_complete total_documents=9
✅ Successfully ingested 9 document chunks.
```

---

## Verification Checklist

- [ ] `scripts/seed_knowledge_base.py` runs without errors
- [ ] `.chromadb/` directory is created with persisted data
- [ ] Bot now answers "आय प्रमाण पत्र के लिए क्या चाहिए?" with specific document lists from the knowledge base
- [ ] Bot includes both Hindi and English document names
- [ ] Bot mentions common mistakes and process steps
- [ ] For unknown services (not in knowledge base), bot says so clearly instead of fabricating

---

## Adding More Services

To add a new service to the knowledge base:

1. Copy `src/janseva/knowledge/data/services/_template.yaml`
2. Rename to `<service_name>.yaml`
3. Fill in all fields
4. Re-run `uv run python scripts/seed_knowledge_base.py`
5. The new service is immediately available for RAG queries

---

## Git Checkpoint

```bash
git add -A
git commit -m "feat(rag): implement knowledge base with RAG for government services

- YAML-based service catalog (income certificate, caste certificate)
- Document ingestion pipeline: YAML → text chunks → embeddings → ChromaDB
- Vector store interface with similarity search
- Knowledge search tool for agents
- Updated Service Navigator to use RAG-augmented responses
- Seed script for populating the knowledge base"
```
