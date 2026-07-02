# Guide 10: Farmer Services Agent

## What This Does
Adds a specialist agent for farmer-specific queries — subsidy navigation, wholesale market (mandi) prices, and logistics support.

## Prerequisites
- Guide 03 completed (AI agent core)
- Guide 04 completed (knowledge base system)

---

## Features

### 1. Subsidy Navigator
- "What subsidies am I eligible for?" → Based on user profile (crop, land size, district)
- "How do I apply for PM Kisan?" → Step-by-step with required documents
- "What is the deadline for applying?" → Scheme-specific deadlines

### 2. Wholesale Market (Mandi) Information
- "What is the price of wheat today?" → Current mandi prices (from data feed)
- "Which mandi near me has the best price for rice?" → Comparative pricing
- Future: integrate with eNAM (National Agriculture Market) API

### 3. Logistics Support
- "How do I transport my produce to the mandi?" → Local transport options
- "What are the storage facilities near me?" → Cold storage, warehouses

---

## Data Sources

### Subsidy Data (Knowledge Base YAML)
Create files in `src/janseva/knowledge/data/subsidies/`:

```yaml
# pm_kisan.yaml
scheme_id: pm_kisan
name_en: "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)"
name_hi: "पीएम-किसान (प्रधानमंत्री किसान सम्मान निधि)"
ministry: "Ministry of Agriculture & Farmers Welfare"
benefit: "INR 6,000 per year in 3 installments of INR 2,000"
eligibility:
  - "All land-holding farmer families"
  - "Must have cultivable land"
  - "Excluded: institutional landholders, income tax payers"
required_documents:
  - "Aadhaar Card"
  - "Bank account details (linked to Aadhaar)"
  - "Land ownership documents (Khasra/Khatauni)"
application_process:
  - "Visit PM-KISAN portal (pmkisan.gov.in) or CSC center"
  - "Or contact the local Patwari/Lekhpal for offline registration"
helpline: "155261"
```

### Mandi Prices
- Start with static sample data
- Future: Integrate with Agmarknet API (agmarknet.gov.in) or eNAM API

---

## Implementation Steps

1. Create subsidy YAML data files
2. Create mandi price data model + seed data
3. Build the Farmer Services Agent as a LangGraph specialist
4. Implement subsidy eligibility checker tool
5. Implement mandi price query tool
6. Wire into the orchestrator

---

## Git Checkpoint
```bash
git add -A
git commit -m "feat(farmer): implement farmer services agent with subsidy and mandi support"
```
