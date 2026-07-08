import os
import shutil
import yaml

base_dir = r"c:\Users\notic\OneDrive\Desktop\Hackathon\GoogleXParul\src\janseva\knowledge\data"
services_dir = os.path.join(base_dir, "services")
schemes_dir = os.path.join(base_dir, "schemes")
subsidies_dir = os.path.join(base_dir, "subsidies")

os.makedirs(services_dir, exist_ok=True)
os.makedirs(schemes_dir, exist_ok=True)
os.makedirs(subsidies_dir, exist_ok=True)

# 1. GENERATE SERVICES (Certificates)
def create_service(id, name_en, name_hi, dept, description_en, description_hi, req_docs, steps, timeline, fee, tags):
    content = {
        "service_id": id,
        "name_en": name_en,
        "name_hi": name_hi,
        "department": dept,
        "issuing_authority": "Revenue / Local Administration",
        "applicable_states": ["all"],
        "description_en": description_en,
        "description_hi": description_hi,
        "required_documents": req_docs,
        "process_steps": steps,
        "estimated_timeline": timeline,
        "approximate_fee": fee,
        "tags": tags,
    }
    with open(os.path.join(services_dir, f"{id}.yaml"), "w", encoding="utf-8") as f:
        yaml.dump(content, f, allow_unicode=True, sort_keys=False)

services = [
    (
        "income_certificate", "Income Certificate", "आय प्रमाण पत्र", "Revenue Department",
        "An official document that certifies the annual income of a person or their family.",
        "एक आधिकारिक दस्तावेज जो किसी व्यक्ति या उनके परिवार की वार्षिक आय को प्रमाणित करता है।",
        [
            {"name_en": "Aadhaar Card", "name_hi": "आधार कार्ड", "mandatory": True},
            {"name_en": "Ration Card or ID Proof", "name_hi": "राशन कार्ड या पहचान पत्र", "mandatory": True},
            {"name_en": "Self Declaration / Affidavit", "name_hi": "स्व-घोषणा / शपथ पत्र", "mandatory": True},
            {"name_en": "Salary Slip (if employed)", "name_hi": "वेतन पर्ची (यदि कार्यरत हैं)", "mandatory": False}
        ],
        [
            {"step": 1, "en": "Visit the state e-District portal or nearest CSC (Common Service Center).", "hi": "राज्य ई-डिस्ट्रिक्ट पोर्टल या नजदीकी सीएससी (CSC) पर जाएं।"},
            {"step": 2, "en": "Fill out the Income Certificate application form.", "hi": "आय प्रमाण पत्र आवेदन पत्र भरें।"},
            {"step": 3, "en": "Upload scanned copies of required documents.", "hi": "आवश्यक दस्तावेजों की स्कैन कॉपी अपलोड करें।"},
            {"step": 4, "en": "Pay the nominal processing fee and get the receipt.", "hi": "नाममात्र शुल्क का भुगतान करें और रसीद प्राप्त करें।"}
        ],
        "10-15 days", "₹20 - ₹50", ["income", "certificate", "revenue", "scholarship"]
    ),
    (
        "caste_certificate", "Caste Certificate", "जाति प्रमाण पत्र", "Revenue Department",
        "Proof of belonging to a particular caste (SC, ST, OBC) to avail government benefits.",
        "सरकारी लाभ प्राप्त करने সরকারী लाभ प्राप्त करने के लिए विशेष जाति (SC, ST, OBC) से संबंधित होने का प्रमाण।",
        [
            {"name_en": "Aadhaar Card", "name_hi": "आधार कार्ड", "mandatory": True},
            {"name_en": "Family member's caste certificate (if available)", "name_hi": "परिवार के सदस्य का जाति प्रमाण पत्र", "mandatory": False},
            {"name_en": "Address Proof (Electricity Bill/Ration Card)", "name_hi": "पता प्रमाण (बिजली बिल/राशन कार्ड)", "mandatory": True},
            {"name_en": "Affidavit confirming caste", "name_hi": "जाति की पुष्टि करने वाला शपथ पत्र", "mandatory": True}
        ],
        [
            {"step": 1, "en": "Visit the state e-District portal or Tehsil office.", "hi": "राज्य ई-डिस्ट्रिक्ट पोर्टल या तहसील कार्यालय पर जाएं।"},
            {"step": 2, "en": "Submit the application with proof of ancestry/caste.", "hi": "वंशावली/जाति के प्रमाण के साथ आवेदन जमा करें।"}
        ],
        "15-30 days", "₹20 - ₹50", ["caste", "certificate", "reservation", "obc", "sc", "st"]
    )
]

for s in services:
    create_service(*s)

# 2. GENERATE SCHEMES (General)
def create_scheme(id, name_en, name_hi, ministry, benefit, eligibility, req_docs, process, helpline):
    content = {
        "scheme_id": id,
        "name_en": name_en,
        "name_hi": name_hi,
        "ministry": ministry,
        "benefit": benefit,
        "eligibility": eligibility,
        "required_documents": req_docs,
        "application_process": process,
        "helpline": helpline,
    }
    with open(os.path.join(schemes_dir, f"{id}.yaml"), "w", encoding="utf-8") as f:
        yaml.dump(content, f, allow_unicode=True, sort_keys=False)

schemes = [
    (
        "ayushman_bharat", "Ayushman Bharat (PM-JAY)", "आयुष्मान भारत (PM-JAY)", "Ministry of Health and Family Welfare",
        "Health insurance coverage of up to ₹5 Lakhs per family per year for secondary and tertiary care hospitalization.",
        [
            "Must be listed in the Socio-Economic Caste Census (SECC) 2011 database.",
            "Families with no adult male member aged 16-59 years.",
            "Landless households deriving major income from manual casual labor."
        ],
        ["Aadhaar Card", "Ration Card", "Active Mobile Number"],
        [
            "Visit the official portal (pmjay.gov.in) and click 'Am I Eligible'.",
            "Enter mobile number and verify via OTP.",
            "Check name in the list and visit an impaneled hospital with Aadhaar to get the Ayushman Card."
        ],
        "14555 or 104"
    ),
    (
        "pm_awas_yojana", "PM Awas Yojana (PMAY)", "पीएम आवास योजना", "Ministry of Housing and Urban Affairs",
        "Financial assistance to build a pucca house. Provides credit-linked subsidy on home loans.",
        [
            "The beneficiary family should not own a pucca house anywhere in India.",
            "Annual household income must be below ₹18 Lakhs (depending on EWS/LIG/MIG category).",
            "A female member must be the co-owner of the property."
        ],
        ["Aadhaar Card", "Income Certificate", "Bank Account Details", "Property Documents"],
        [
            "Apply online through the PMAY official website (pmaymis.gov.in) under 'Citizen Assessment'.",
            "Fill out the required details and print the application.",
            "Track the assessment status online."
        ],
        "1800-11-6163"
    )
]

for s in schemes:
    create_scheme(*s)

# 3. GENERATE SUBSIDIES (For Farmer Agent)
def create_subsidy(id, name_en, name_hi, benefit, eligibility, req_docs, process, helpline):
    content = {
        "scheme_id": id,
        "name_en": name_en,
        "name_hi": name_hi,
        "benefit": benefit,
        "eligibility": eligibility,
        "required_documents": req_docs,
        "application_process": process,
        "helpline": helpline,
    }
    with open(os.path.join(subsidies_dir, f"{id}.yaml"), "w", encoding="utf-8") as f:
        yaml.dump(content, f, allow_unicode=True, sort_keys=False)

subsidies = [
    (
        "pm_kisan", "PM Kisan Samman Nidhi", "पीएम किसान सम्मान निधि",
        "Income support of ₹6,000 per year provided in three equal installments of ₹2,000 to landholding farmer families.",
        ["Must be a landholding farmer family.", "Institutional landholders and professionals (doctors/lawyers) are excluded.", "Income tax payers are excluded."],
        ["Aadhaar Card", "Bank Account details linked to Aadhaar", "Land Ownership Documents (Khatauni)"],
        ["Visit pmkisan.gov.in", "Click on 'New Farmer Registration' in the Farmers Corner", "Fill the required details and upload documents."],
        "155261 / 011-24300606"
    ),
    (
        "kcc", "Kisan Credit Card (KCC)", "किसान क्रेडिट कार्ड (KCC)",
        "Provides farmers with timely and adequate credit support for agricultural expenses at subsidized interest rates.",
        ["All farmers - individuals/joint borrowers who are owner cultivators.", "Tenant farmers, oral lessees & share croppers.", "SHGs or Joint Liability Groups of farmers."],
        ["Aadhaar Card", "PAN Card / Voter ID", "Land documents (Khasra/Khatauni)", "Recent passport size photograph"],
        ["Visit your nearest commercial bank, regional rural bank, or cooperative bank.", "Submit the KCC application form with land records.", "The bank will evaluate and issue the KCC."],
        "Kisan Call Center: 1800-180-1551"
    )
]

for s in subsidies:
    create_subsidy(*s)

print("Generated factual YAML files for Services, Schemes, and Subsidies.")
