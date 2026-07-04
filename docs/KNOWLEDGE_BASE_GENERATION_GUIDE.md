# JanSeva Knowledge Base — Complete Generation Guide

> **Purpose**: This document is the single source of truth for generating JanSeva's knowledge base YAML files. An AI model (Gemini, Claude, etc.) should be able to read this document and produce every YAML file needed to cover **all** government services, schemes, documents, and procedures across India.

---

## Table of Contents
1. [Overview](#1-overview)
2. [File Structure & Naming](#2-file-structure--naming)
3. [YAML Schema — Services & Documents](#3-yaml-schema--services--documents)
4. [YAML Schema — Schemes & Subsidies](#4-yaml-schema--schemes--subsidies)
5. [YAML Schema — Healthcare Facilities](#5-yaml-schema--healthcare-facilities)
6. [Complete Example — Service File](#6-complete-example--service-file)
7. [Complete Example — Scheme File](#7-complete-example--scheme-file)
8. [Master List of Required Files](#8-master-list-of-required-files)
9. [Quality Rules & Validation Checklist](#9-quality-rules--validation-checklist)
10. [Generation Instructions for AI](#10-generation-instructions-for-ai)

---

## 1. Overview

JanSeva is a Telegram bot that helps Indian citizens navigate government services. Its knowledge base is a collection of YAML files that get ingested into a vector database (ChromaDB) for RAG-based question answering.

**Coverage target**: Every government document, certificate, scheme, subsidy, pension, loan, and procedure that an Indian citizen might need — from birth certificate to death certificate, from farm subsidies to startup grants.

**Language requirement**: Every file MUST include both English (`_en`) and Hindi (`_hi`) fields. The bot serves users in both languages.

**Accuracy requirement**: All information must reflect the **current** (2024-2026) state of Indian government procedures. Use official government portal URLs. Do not fabricate helpline numbers or URLs.

---

## 2. File Structure & Naming

```
src/janseva/knowledge/data/
├── services/              # Government documents & certificates
│   ├── _template.yaml     # Do NOT modify, for reference only
│   ├── birth_certificate.yaml
│   ├── income_certificate.yaml
│   └── ...
├── schemes/               # Government schemes, subsidies, pensions, loans
│   ├── pm_kisan.yaml
│   ├── ayushman_bharat.yaml
│   └── ...
└── healthcare/            # Healthcare-specific data (hospitals, programs)
    ├── ayushman_bharat_hospitals.yaml
    └── ...
```

**Naming rules**:
- File name = `snake_case` version of the service/scheme name
- No spaces, no hyphens, no uppercase
- Use the most common short name (e.g., `pm_kisan.yaml` not `pradhan_mantri_kisan_samman_nidhi.yaml`)

> **IMPORTANT**: Rename the existing `subsidies/` directory to `schemes/`. The new schema below applies to all scheme files.

---

## 3. YAML Schema — Services & Documents

Use this schema for any **document, certificate, registration, or license** that a citizen applies for and receives.

```yaml
# REQUIRED FIELDS — every file must have these
service_id: <unique_snake_case_id>          # e.g., "birth_certificate"
name_en: <English name>                      # e.g., "Birth Certificate"
name_hi: <Hindi name>                        # e.g., "जन्म प्रमाण पत्र"
department: <Department name EN / HI>        # e.g., "Health Department / स्वास्थ्य विभाग"
issuing_authority: <Authority EN / HI>       # e.g., "Municipal Corporation / नगर निगम"
applicable_states:
  - all                                      # or list specific states

description_en: |
  2-4 sentence English description. What is this document?
  Why does a citizen need it? When is it required?

description_hi: |
  2-4 sentence Hindi description. Same content as English.
  Must be accurate Hindi, not machine-translated gibberish.

required_documents:
  - name_en: "Document Name"
    name_hi: "दस्तावेज का नाम"
    mandatory: true                          # true or false
    note: "Optional clarification"           # Only include if needed

process_steps:
  - step: 1
    en: "Step description in English"
    hi: "चरण का विवरण हिंदी में"
  - step: 2
    en: "Next step..."
    hi: "अगला चरण..."

estimated_timeline: "X-Y working days"       # Realistic range
approximate_fee: "INR X-Y (varies by state)" # Realistic range

# OPTIONAL BUT HIGHLY RECOMMENDED
online_portals:
  - state: "State Name"
    url: "https://verified-url.gov.in"       # MUST be a real .gov.in URL

common_mistakes:
  - en: "Common error citizens make"
    hi: "नागरिक जो सामान्य गलती करते हैं"

helpline: "helpline number"                  # Only if verified

tags:                                        # 3-8 relevant search terms
  - tag1
  - tag2
  - tag3
```

---

## 4. YAML Schema — Schemes & Subsidies

Use this schema for any **government scheme, subsidy, pension, loan, or financial benefit**.

```yaml
# REQUIRED FIELDS
scheme_id: <unique_snake_case_id>            # e.g., "ayushman_bharat"
name_en: <Full official English name>        # e.g., "Ayushman Bharat - PMJAY"
name_hi: <Full official Hindi name>          # e.g., "आयुष्मान भारत - पीएमजेएवाई"
ministry: <Ministry name>                    # e.g., "Ministry of Health & Family Welfare"
category: <one of the categories below>      # See category list
launched_year: <year>                        # e.g., 2018

description_en: |
  3-5 sentence English description. What does this scheme do?
  Who benefits from it? What problem does it solve?

description_hi: |
  3-5 sentence Hindi description. Same content as English.

benefit: <What the citizen receives>         # e.g., "Health coverage up to INR 5 lakh per family per year"
benefit_hi: <Hindi version>                  # e.g., "प्रति परिवार प्रति वर्ष ₹5 लाख तक का स्वास्थ्य कवर"

eligibility:
  - "Eligibility criterion 1 in English"
  - "Eligibility criterion 2 in English"

eligibility_hi:
  - "पात्रता मानदंड 1 हिंदी में"
  - "पात्रता मानदंड 2 हिंदी में"

exclusions:                                  # Who CANNOT avail this scheme
  - "Exclusion 1"

required_documents:
  - name_en: "Document Name"
    name_hi: "दस्तावेज का नाम"
    mandatory: true

application_process:
  - step: 1
    en: "How to apply - step 1"
    hi: "आवेदन कैसे करें - चरण 1"

official_website: "https://scheme-portal.gov.in"  # MUST be verified .gov.in
helpline: "helpline number"                        # Only if verified
estimated_timeline: "X days/weeks for processing"

# OPTIONAL
income_limit: "INR X per annum"              # If income-based eligibility
age_limit: "X-Y years"                       # If age-based eligibility
applicable_states:
  - all                                      # or specific states

tags:
  - tag1
  - tag2
```

**Valid categories** (use exactly one):
- `education`
- `agriculture`
- `healthcare`
- `housing`
- `employment`
- `women_and_child`
- `social_security` (pensions, disability, widow)
- `financial_inclusion` (bank accounts, insurance, loans)
- `skill_development`
- `rural_development`
- `urban_development`
- `sc_st_obc_welfare`
- `minority_welfare`
- `ex_servicemen`
- `senior_citizen`
- `disability_welfare`
- `digital_governance`
- `environment`
- `food_security`
- `documents` (for certificate/document-specific schemes)

---

## 5. YAML Schema — Healthcare Facilities

```yaml
facility_id: <unique_id>
name_en: <Facility name>
name_hi: <Hindi name>
type: <hospital|phc|chc|dispensary|wellness_center>
district: <District name>
state: <State name>
services_offered:
  - "Service 1"
  - "Service 2"
empaneled_under:
  - "Ayushman Bharat"
contact: "phone number"
address: "Full address"
```

> **Note**: Healthcare facility data is location-specific and cannot be comprehensively generated by AI. Generate a **template** with a few examples per state. Real data will come from government APIs later.

---

## 6. Complete Example — Service File

This is `income_certificate.yaml` — use this as the gold standard for service files:

```yaml
service_id: income_certificate
name_en: Income Certificate
name_hi: आय प्रमाण पत्र
department: Revenue Department / राजस्व विभाग
issuing_authority: Sub-Divisional Magistrate (SDM) / उप-जिलाधिकारी
applicable_states:
  - all

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

---

## 7. Complete Example — Scheme File

This is what a proper scheme file should look like (`ayushman_bharat.yaml`):

```yaml
scheme_id: ayushman_bharat
name_en: "Ayushman Bharat - Pradhan Mantri Jan Arogya Yojana (PM-JAY)"
name_hi: "आयुष्मान भारत - प्रधानमंत्री जन आरोग्य योजना (पीएम-जेएवाई)"
ministry: "Ministry of Health & Family Welfare"
category: healthcare
launched_year: 2018

description_en: |
  Ayushman Bharat PM-JAY is the world's largest health insurance scheme,
  providing health coverage of INR 5 lakh per family per year for secondary
  and tertiary care hospitalization. It targets over 12 crore poor and
  vulnerable families (approximately 55 crore beneficiaries) identified
  through SECC 2011 data. The scheme covers 3 days of pre-hospitalization
  and 15 days of post-hospitalization expenses.

description_hi: |
  आयुष्मान भारत पीएम-जेएवाई विश्व की सबसे बड़ी स्वास्थ्य बीमा योजना है,
  जो प्रति परिवार प्रति वर्ष ₹5 लाख तक का स्वास्थ्य कवरेज प्रदान करती है।
  यह SECC 2011 डेटा के माध्यम से पहचाने गए 12 करोड़ से अधिक गरीब और
  कमजोर परिवारों (लगभग 55 करोड़ लाभार्थी) को लक्षित करती है। योजना में
  अस्पताल में भर्ती होने से 3 दिन पहले और 15 दिन बाद के खर्चे शामिल हैं।

benefit: "Health coverage up to INR 5,00,000 per family per year for hospitalization"
benefit_hi: "अस्पताल में भर्ती के लिए प्रति परिवार प्रति वर्ष ₹5,00,000 तक का स्वास्थ्य कवरेज"

eligibility:
  - "Families identified in SECC 2011 database"
  - "No cap on family size or age of members"
  - "Coverage from day one — no waiting period"
  - "Pre-existing diseases are covered"

eligibility_hi:
  - "SECC 2011 डेटाबेस में पहचाने गए परिवार"
  - "परिवार के आकार या सदस्यों की उम्र पर कोई सीमा नहीं"
  - "पहले दिन से कवरेज — कोई प्रतीक्षा अवधि नहीं"
  - "पहले से मौजूद बीमारियां कवर हैं"

exclusions:
  - "Families with a member who is a government employee"
  - "Families with annual income above the SECC poverty threshold"
  - "Families with motorized vehicles or mechanized farming equipment (in some categories)"

required_documents:
  - name_en: "Aadhaar Card"
    name_hi: "आधार कार्ड"
    mandatory: true
  - name_en: "Ration Card"
    name_hi: "राशन कार्ड"
    mandatory: false
    note: "Helps verify SECC eligibility"
  - name_en: "SECC 2011 letter (if available)"
    name_hi: "SECC 2011 पत्र (यदि उपलब्ध हो)"
    mandatory: false

application_process:
  - step: 1
    en: "Check eligibility at mera.pmjay.gov.in by entering your mobile number or ration card number."
    hi: "mera.pmjay.gov.in पर अपना मोबाइल नंबर या राशन कार्ड नंबर दर्ज करके पात्रता जांचें।"
  - step: 2
    en: "Visit any empaneled hospital with your Aadhaar card."
    hi: "अपने आधार कार्ड के साथ किसी भी सूचीबद्ध अस्पताल में जाएं।"
  - step: 3
    en: "Approach the Ayushman Mitra at the hospital for e-KYC verification."
    hi: "ई-केवाईसी सत्यापन के लिए अस्पताल में आयुष्मान मित्र से संपर्क करें।"
  - step: 4
    en: "Once verified, your Ayushman card will be created and treatment can begin."
    hi: "सत्यापन के बाद, आपका आयुष्मान कार्ड बनाया जाएगा और उपचार शुरू हो सकता है।"

official_website: "https://pmjay.gov.in"
helpline: "14555"
estimated_timeline: "Instant verification at hospital; card creation within 30 minutes"

tags:
  - healthcare
  - insurance
  - hospitalization
  - poor
  - PMJAY
  - ayushman
  - medical
  - hospital
```

---

## 8. Master List of Required Files

Generate **every file** in this list. Each entry shows: `filename.yaml` → brief description.

### 8A. DOCUMENTS & CERTIFICATES (`services/` directory)

#### Identity & Civil Registration
1. `birth_certificate.yaml` → Birth Certificate (जन्म प्रमाण पत्र)
2. `death_certificate.yaml` → Death Certificate (मृत्यु प्रमाण पत्र)
3. `marriage_certificate.yaml` → Marriage Certificate (विवाह प्रमाण पत्र)
4. `aadhaar_card.yaml` → Aadhaar Card enrollment/update (आधार कार्ड)
5. `voter_id.yaml` → Voter ID / EPIC Card (मतदाता पहचान पत्र)
6. `pan_card.yaml` → PAN Card (पैन कार्ड)
7. `passport.yaml` → Indian Passport (पासपोर्ट)
8. `ration_card.yaml` → Ration Card (राशन कार्ड)
9. `domicile_certificate.yaml` → Domicile / Residence Certificate (मूल निवास प्रमाण पत्र)

#### Revenue & Land Records
10. `income_certificate.yaml` → ✅ Already exists
11. `caste_certificate.yaml` → ✅ Already exists
12. `obc_certificate.yaml` → OBC Non-Creamy Layer Certificate (ओबीसी नॉन-क्रीमी लेयर प्रमाण पत्र)
13. `ews_certificate.yaml` → EWS Certificate (आर्थिक रूप से कमजोर वर्ग प्रमाण पत्र)
14. `land_record_mutation.yaml` → Land Record Mutation / Namantaran (नामांतरण / दाखिल खारिज)
15. `khata_transfer.yaml` → Khata Transfer (खाता स्थानांतरण)
16. `encumbrance_certificate.yaml` → Encumbrance Certificate (भार मुक्ति प्रमाण पत्र)
17. `land_conversion.yaml` → Agricultural to Non-Agricultural Land Conversion (भूमि परिवर्तन)
18. `fard_jamabandi.yaml` → Fard / Jamabandi / Khasra-Khatauni (फर्द / जमाबंदी / खसरा-खतौनी)

#### Police & Legal
19. `police_clearance_certificate.yaml` → Police Clearance Certificate (पुलिस क्लीयरेंस प्रमाण पत्र)
20. `character_certificate.yaml` → Character Certificate (चरित्र प्रमाण पत्र)
21. `fir_registration.yaml` → FIR Registration process (एफआईआर दर्ज करना)
22. `noc_police.yaml` → Police NOC for various purposes (पुलिस अनापत्ति प्रमाण पत्र)

#### Transport & Vehicles
23. `driving_license.yaml` → Driving License — new, renewal, international (ड्राइविंग लाइसेंस)
24. `learner_license.yaml` → Learner's License (लर्नर लाइसेंस)
25. `vehicle_registration.yaml` → Vehicle Registration / RC (वाहन पंजीकरण)
26. `vehicle_transfer.yaml` → Vehicle Ownership Transfer (वाहन स्वामित्व हस्तांतरण)
27. `vehicle_fitness_certificate.yaml` → Fitness Certificate for commercial vehicles (फिटनेस प्रमाण पत्र)
28. `pollution_certificate.yaml` → PUC — Pollution Under Control (प्रदूषण नियंत्रण प्रमाण पत्र)
29. `road_tax.yaml` → Road Tax payment (सड़क कर)

#### Business & Commercial
30. `gst_registration.yaml` → GST Registration (जीएसटी पंजीकरण)
31. `shop_establishment_license.yaml` → Shop & Establishment License (दुकान एवं प्रतिष्ठान लाइसेंस)
32. `trade_license.yaml` → Trade License from Municipal Corporation (व्यापार लाइसेंस)
33. `fssai_license.yaml` → FSSAI Food License (खाद्य लाइसेंस)
34. `msme_udyam_registration.yaml` → Udyam / MSME Registration (उद्यम पंजीकरण)
35. `import_export_code.yaml` → IEC — Import Export Code (आयात निर्यात कोड)
36. `company_incorporation.yaml` → Company/LLP Registration via MCA (कंपनी पंजीकरण)
37. `startup_india_registration.yaml` → DPIIT Startup Recognition (स्टार्टअप इंडिया पंजीकरण)

#### Building & Property
38. `building_permission.yaml` → Building Plan Approval (भवन निर्माण अनुमति)
39. `occupancy_certificate.yaml` → Occupancy / Completion Certificate (अधिभोग / पूर्णता प्रमाण पत्र)
40. `property_registration.yaml` → Property / Sale Deed Registration (संपत्ति पंजीकरण)
41. `stamp_duty.yaml` → Stamp Duty payment process (स्टाम्प शुल्क)
42. `water_connection.yaml` → New Water Connection (नया जल कनेक्शन)
43. `electricity_connection.yaml` → New Electricity Connection (नया बिजली कनेक्शन)
44. `gas_connection.yaml` → LPG Gas Connection — Ujjwala & general (गैस कनेक्शन)

#### Disability & Senior Citizen
45. `disability_certificate.yaml` → Disability Certificate / UDID (विकलांगता प्रमाण पत्र)
46. `senior_citizen_card.yaml` → Senior Citizen ID Card (वरिष्ठ नागरिक पहचान पत्र)

#### Education
47. `school_leaving_certificate.yaml` → School Leaving / Transfer Certificate (स्कूल छोड़ने का प्रमाण पत्र)
48. `degree_verification.yaml` → Degree/Marksheet Verification & Apostille (उपाधि सत्यापन)
49. `equivalence_certificate.yaml` → Foreign Degree Equivalence (विदेशी डिग्री समकक्षता)
50. `rti_application.yaml` → RTI Application Process (सूचना का अधिकार आवेदन)

#### Other
51. `arms_license.yaml` → Arms License (शस्त्र लाइसेंस)
52. `noc_fire.yaml` → Fire NOC (अग्निशमन अनापत्ति प्रमाण पत्र)
53. `legal_heir_certificate.yaml` → Legal Heir Certificate (कानूनी उत्तराधिकार प्रमाण पत्र)
54. `succession_certificate.yaml` → Succession Certificate (उत्तराधिकार प्रमाण पत्र)
55. `freedom_fighter_certificate.yaml` → Freedom Fighter Dependent Certificate (स्वतंत्रता सेनानी आश्रित प्रमाण पत्र)

---

### 8B. SCHEMES & SUBSIDIES (`schemes/` directory)

#### Agriculture & Farmer Welfare
56. `pm_kisan.yaml` → ✅ Already exists (needs upgrade to new schema)
57. `pm_fasal_bima.yaml` → PM Fasal Bima Yojana (crop insurance)
58. `kisan_credit_card.yaml` → KCC — Kisan Credit Card
59. `soil_health_card.yaml` → Soil Health Card Scheme
60. `pm_krishi_sinchai.yaml` → PM Krishi Sinchai Yojana (irrigation)
61. `enam.yaml` → eNAM — National Agriculture Market
62. `paramparagat_krishi.yaml` → Paramparagat Krishi Vikas Yojana (organic farming)
63. `nfsm.yaml` → National Food Security Mission
64. `rkvy.yaml` → Rashtriya Krishi Vikas Yojana
65. `pm_aasha.yaml` → PM-AASHA (price support for farmers)
66. `agriculture_infrastructure_fund.yaml` → Agriculture Infrastructure Fund
67. `dairy_entrepreneurship.yaml` → Dairy Entrepreneurship Development Scheme
68. `fisheries_pmmsy.yaml` → PM Matsya Sampada Yojana (fisheries)

#### Education & Scholarships
69. `pre_matric_scholarship.yaml` → Pre-Matric Scholarship (SC/ST/OBC/Minority)
70. `post_matric_scholarship.yaml` → Post-Matric Scholarship
71. `national_merit_scholarship.yaml` → National Merit Scholarship / NMMS
72. `pm_vidyalakshmi.yaml` → Vidyalakshmi Education Loan Portal
73. `central_sector_scholarship.yaml` → Central Sector Scheme of Scholarships
74. `national_overseas_scholarship.yaml` → National Overseas Scholarship (SC)
75. `pm_yashasvi.yaml` → PM-YASHASVI (OBC, EBC, DNT)
76. `ishan_uday.yaml` → Ishan Uday Scholarship (NE region)
77. `pragati_scholarship.yaml` → Pragati Scholarship for Girls (AICTE)
78. `begum_hazrat_mahal_scholarship.yaml` → Begum Hazrat Mahal Scholarship (minority girls)
79. `pmkvy.yaml` → Pradhan Mantri Kaushal Vikas Yojana (skill training)
80. `ddugky.yaml` → DDU-GKY (Deen Dayal Upadhyaya Grameen Kaushalya Yojana)
81. `naps.yaml` → National Apprenticeship Promotion Scheme
82. `mid_day_meal.yaml` → PM POSHAN (Mid Day Meal Scheme)

#### Healthcare
83. `ayushman_bharat.yaml` → PM-JAY health insurance
84. `janani_suraksha.yaml` → Janani Suraksha Yojana (maternal care)
85. `pmsma.yaml` → PM Surakshit Matritva Abhiyan (pregnancy checkups)
86. `mission_indradhanush.yaml` → Mission Indradhanush (immunization)
87. `nikshay_poshan.yaml` → Nikshay Poshan Yojana (TB patients)
88. `rashtriya_swasthya_bima.yaml` → RSBY (for BPL families)
89. `national_health_mission.yaml` → NHM services
90. `pm_jan_aushadhi.yaml` → PM Jan Aushadhi Yojana (affordable medicines)
91. `ayushman_bharat_health_account.yaml` → ABHA Health ID

#### Housing & Urban Development
92. `pmay_urban.yaml` → PM Awas Yojana — Urban (housing subsidy)
93. `pmay_gramin.yaml` → PM Awas Yojana — Gramin (rural housing)
94. `smart_city_mission.yaml` → Smart Cities Mission
95. `swachh_bharat_urban.yaml` → Swachh Bharat Mission — Urban (toilets, sanitation)
96. `swachh_bharat_gramin.yaml` → Swachh Bharat Mission — Gramin
97. `amrut.yaml` → AMRUT (urban water supply & sewerage)

#### Employment & Self-Employment
98. `mgnrega.yaml` → MGNREGA (100-day employment guarantee)
99. `pmegp.yaml` → PM Employment Generation Programme (micro enterprises)
100. `mudra_loan.yaml` → PM Mudra Yojana (Shishu, Kishore, Tarun loans)
101. `startup_india_scheme.yaml` → Startup India benefits (tax exemptions, funding)
102. `stand_up_india.yaml` → Stand Up India (SC/ST/Women entrepreneurs)
103. `pm_svanidhi.yaml` → PM SVANidhi (street vendor micro loans)
104. `deendayal_antyodaya.yaml` → DAY-NULM (National Urban Livelihoods Mission)
105. `pm_vishwakarma.yaml` → PM Vishwakarma (traditional artisans & craftsmen)

#### Women & Child Development
106. `beti_bachao_beti_padhao.yaml` → Beti Bachao Beti Padhao
107. `sukanya_samriddhi.yaml` → Sukanya Samriddhi Yojana (girl child savings)
108. `pmmvy.yaml` → PM Matru Vandana Yojana (maternity benefit ₹5000)
109. `ujjwala_yojana.yaml` → PM Ujjwala Yojana (free LPG connection)
110. `one_stop_centre.yaml` → One Stop Centre (Sakhi) for women in distress
111. `women_helpline.yaml` → Women Helpline 181
112. `mahila_shakti_kendra.yaml` → Mahila Shakti Kendra
113. `poshan_abhiyan.yaml` → POSHAN Abhiyan (nutrition mission)
114. `icds.yaml` → Integrated Child Development Services (anganwadi)

#### Social Security & Pensions
115. `pm_jeevan_jyoti.yaml` → PMJJBY (life insurance ₹330/year)
116. `pm_suraksha_bima.yaml` → PMSBY (accident insurance ₹20/year)
117. `atal_pension.yaml` → Atal Pension Yojana (unorganized sector pension)
118. `nsap_old_age.yaml` → IGNOAPS — Old Age Pension
119. `nsap_widow.yaml` → IGNWPS — Widow Pension
120. `nsap_disability.yaml` → IGNDPS — Disability Pension
121. `pm_kisan_mandhan.yaml` → PM Kisan Maandhan Yojana (farmer pension)
122. `pm_shram_yogi_mandhan.yaml` → PM Shram Yogi Maandhan (worker pension)
123. `epfo_services.yaml` → EPF withdrawal, transfer, pension (EPFO)
124. `esic_services.yaml` → ESIC — Employee State Insurance

#### Financial Inclusion
125. `jan_dhan.yaml` → PM Jan Dhan Yojana (zero-balance bank account)
126. `pm_jeevan_jyoti_bima.yaml` → Already covered in 115
127. `atal_beemit_vyakti_kalyan.yaml` → ESIC Atal Beemit Vyakti Kalyan Yojana

#### SC/ST/OBC Welfare
128. `venture_capital_fund_sc.yaml` → Venture Capital Fund for SC
129. `national_scheduled_tribes_finance.yaml` → NSTFDC loans and schemes
130. `nbcfdc_schemes.yaml` → NBCFDC schemes for backward classes
131. `post_matric_scholarship_sc.yaml` → Specific SC scholarship details

#### Rural Development
132. `pm_gram_sadak.yaml` → PM Gram Sadak Yojana (rural roads)
133. `ddugjy.yaml` → Deen Dayal Upadhyaya Gram Jyoti Yojana (rural electrification)
134. `saubhagya.yaml` → Saubhagya — household electrification
135. `saansad_adarsh_gram.yaml` → Saansad Adarsh Gram Yojana
136. `shyama_prasad_mukherjee_rurban.yaml` → SPMRM — Rurban Mission
137. `jal_jeevan_mission.yaml` → Jal Jeevan Mission (tap water)

#### Digital & Governance
138. `digilocker.yaml` → DigiLocker registration and usage
139. `umang_app.yaml` → UMANG App — unified mobile app for services
140. `common_service_centre.yaml` → CSC — Common Service Centres
141. `e_court_services.yaml` → e-Courts case status, filing
142. `rti_online.yaml` → RTI Online Filing

#### Food Security
143. `national_food_security.yaml` → NFSA — subsidized ration
144. `annapurna.yaml` → Annapurna Scheme (free food grains for senior citizens)
145. `one_nation_one_ration.yaml` → One Nation One Ration Card (portability)

#### Ex-Servicemen
146. `ex_servicemen_welfare.yaml` → ECHS, CSD, resettlement schemes

#### Environment
147. `green_india_mission.yaml` → National Mission for Green India

---

### 8C. HEALTHCARE (`healthcare/` directory)

148. `healthcare_programs_overview.yaml` → Overview of all public health programs
149. `primary_health_centres.yaml` → What PHCs offer, how to access
150. `community_health_centres.yaml` → CHC services
151. `ayush_wellness_centres.yaml` → AYUSH wellness centre information

---

## 9. Quality Rules & Validation Checklist

Every generated file MUST pass these checks:

### Content Rules
- [ ] `service_id` or `scheme_id` is unique across all files
- [ ] Both English and Hindi fields are filled (no empty `_hi` fields)
- [ ] Hindi text is proper Hindi, not transliterated English
- [ ] All URLs are real, verified `.gov.in` or `.nic.in` domains
- [ ] Helpline numbers are real government helplines (verify before including)
- [ ] Fee amounts and timelines are realistic (don't guess — say "varies by state" if unsure)
- [ ] Eligibility criteria are specific, not vague ("all farmers" is too vague)
- [ ] At least 3 `required_documents` entries per file
- [ ] At least 3 `process_steps` per file
- [ ] At least 3 `tags` per file
- [ ] No placeholder text like "TBD", "TODO", "fill in later"

### Formatting Rules
- [ ] File uses UTF-8 encoding (for Hindi text)
- [ ] Multi-line text uses YAML `|` block scalar, not inline strings
- [ ] No tabs — use 2-space indentation
- [ ] No trailing whitespace
- [ ] File ends with a newline

### Factual Accuracy Rules
- [ ] Scheme names match official government nomenclature
- [ ] Ministry/department names are current (post-2024 restructuring)
- [ ] If a scheme has been renamed or merged, use the CURRENT name
- [ ] Don't include discontinued schemes without marking them as discontinued
- [ ] Cross-reference official scheme websites for benefit amounts

---

## 10. Generation Instructions for AI

If you are an AI model generating these files, follow this exact workflow:

### Step 1: Generate Service Files
For each entry in section 8A, create a YAML file in `src/janseva/knowledge/data/services/` following the schema in section 3 and the example in section 6.

### Step 2: Generate Scheme Files
For each entry in section 8B, create a YAML file in `src/janseva/knowledge/data/schemes/` following the schema in section 4 and the example in section 7.

### Step 3: Generate Healthcare Files
For each entry in section 8C, create a YAML file in `src/janseva/knowledge/data/healthcare/`.

### Step 4: Upgrade Existing Files
The following existing files need to be upgraded to match the new schema:
- `subsidies/pm_kisan.yaml` → Move to `schemes/pm_kisan.yaml` and upgrade to full schema
- `services/caste_certificate.yaml` → Add `applicable_states`, `online_portals`, verify completeness
- `services/income_certificate.yaml` → Verify completeness (already good)

### Step 5: Validate
Run through every file against the checklist in section 9. Fix any issues.

### Generation Tips
1. **Be specific**: "Visit the Tehsil office" is better than "Visit the concerned authority"
2. **Include state variations**: Major states have different portals — include at least UP, MP, Bihar, Rajasthan, Maharashtra, Tamil Nadu, Karnataka, West Bengal
3. **Cover edge cases**: What if documents are lost? What if name is mismatched? Include these as `common_mistakes`
4. **Think like a rural citizen**: They may not know English terms. Hindi descriptions should use simple, everyday Hindi — not bureaucratic language
5. **Cross-reference**: If scheme A requires certificate B, mention B explicitly (e.g., "Ayushman Bharat requires Aadhaar Card — see `aadhaar_card.yaml`")

### File Count Summary
| Directory   | Files to Generate | Already Exist |
|-------------|-------------------|---------------|
| `services/` | 53                | 2             |
| `schemes/`  | 92                | 1 (needs upgrade) |
| `healthcare/` | 4               | 0             |
| **TOTAL**   | **~150 files**    | **3**         |

---

> **End of generation guide. The AI generating the files should produce all ~150 YAML files following the schemas and examples above, covering every government service and scheme listed in section 8.**
