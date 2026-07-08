import os
import shutil

import yaml

base_dir = r"c:\Users\notic\OneDrive\Desktop\Hackathon\GoogleXParul\src\janseva\knowledge\data"
services_dir = os.path.join(base_dir, "services")
schemes_dir = os.path.join(base_dir, "schemes")
subsidies_dir = os.path.join(base_dir, "subsidies")

os.makedirs(services_dir, exist_ok=True)
os.makedirs(schemes_dir, exist_ok=True)

if os.path.exists(subsidies_dir):
    shutil.rmtree(subsidies_dir)


# Template for services
def create_service(id, name_en, name_hi, dept):
    content = {
        "service_id": id,
        "name_en": name_en,
        "name_hi": name_hi,
        "department": dept,
        "issuing_authority": "Relevant State Authority",
        "applicable_states": ["all"],
        "description_en": f"{name_en} is an essential document issued by the {dept}.",
        "description_hi": f"{name_hi} एक आवश्यक दस्तावेज़ है।",
        "required_documents": [
            {"name_en": "Aadhaar Card", "name_hi": "आधार कार्ड", "mandatory": True}
        ],
        "process_steps": [
            {"step": 1, "en": "Visit the official portal", "hi": "आधिकारिक पोर्टल पर जाएं"}
        ],
        "estimated_timeline": "15-30 days",
        "approximate_fee": "INR 50",
        "tags": [id.replace("_", " "), "certificate"],
    }
    with open(os.path.join(services_dir, f"{id}.yaml"), "w", encoding="utf-8") as f:
        yaml.dump(content, f, allow_unicode=True, sort_keys=False)


services = [
    ("domicile_certificate", "Domicile Certificate", "मूल निवास प्रमाण पत्र", "Revenue Department"),
    ("birth_certificate", "Birth Certificate", "जन्म प्रमाण पत्र", "Municipal Corporation"),
    ("death_certificate", "Death Certificate", "मृत्यु प्रमाण पत्र", "Municipal Corporation"),
    ("land_records", "Land Records (Bhulekh)", "भूलेख", "Revenue Department"),
    ("ration_card", "Ration Card", "राशन कार्ड", "Food and Civil Supplies"),
    ("voter_id", "Voter ID", "मतदाता पहचान पत्र", "Election Commission"),
    ("passport", "Passport", "पासपोर्ट", "Ministry of External Affairs"),
    ("driving_license", "Driving License", "ड्राइविंग लाइसेंस", "Transport Department"),
    ("pan_card", "PAN Card", "पैन कार्ड", "Income Tax Department"),
    ("marriage_certificate", "Marriage Certificate", "विवाह प्रमाण पत्र", "Registrar of Marriages"),
    ("property_registration", "Property Registration", "संपत्ति पंजीकरण", "Stamps and Registration"),
    ("building_permit", "Building Permit", "भवन निर्माण अनुमति", "Municipal Corporation"),
    ("water_connection", "Water Connection", "जल कनेक्शन", "Jal Board"),
    ("electricity_connection", "Electricity Connection", "बिजली कनेक्शन", "Power Corporation"),
    ("pension_application", "Pension Application", "पेंशन आवेदन", "Social Welfare Department"),
]

for s in services:
    create_service(*s)


# Template for schemes
def create_scheme(id, name_en, name_hi, ministry):
    content = {
        "scheme_id": id,
        "name_en": name_en,
        "name_hi": name_hi,
        "ministry": ministry,
        "benefit": "Financial assistance or specific benefits as per scheme guidelines",
        "eligibility": ["Eligibility criteria apply as per official notifications."],
        "required_documents": ["Aadhaar Card", "Bank account details (linked to Aadhaar)"],
        "application_process": ["Visit the official portal or nearest CSC center."],
        "helpline": "1076",
    }
    with open(os.path.join(schemes_dir, f"{id}.yaml"), "w", encoding="utf-8") as f:
        yaml.dump(content, f, allow_unicode=True, sort_keys=False)


schemes = [
    ("ayushman_bharat", "Ayushman Bharat (PMJAY)", "आयुष्मान भारत", "Ministry of Health"),
    ("pm_awas_yojana", "PM Awas Yojana", "पीएम आवास योजना", "Ministry of Housing"),
    ("pm_ujjwala_yojana", "PM Ujjwala Yojana", "पीएम उज्ज्वला योजना", "Ministry of Petroleum"),
    ("sukanya_samriddhi", "Sukanya Samriddhi Yojana", "सुकन्या समृद्धि योजना", "Ministry of Finance"),
    ("mudra_loan", "Mudra Loan", "मुद्रा लोन", "Ministry of Finance"),
    (
        "pmfby",
        "Pradhan Mantri Fasal Bima Yojana",
        "प्रधानमंत्री फसल बीमा योजना",
        "Ministry of Agriculture",
    ),
    ("nrega", "MGNREGA", "मनरेगा", "Ministry of Rural Development"),
    ("scholarships_obc_sc_st", "OBC/SC/ST Scholarships", "छात्रवृत्ति", "Ministry of Social Justice"),
    ("old_age_pension", "Old Age Pension", "वृद्धावस्था पेंशन", "Social Welfare Department"),
    ("widow_pension", "Widow Pension", "विधवा पेंशन", "Social Welfare Department"),
]

for s in schemes:
    create_scheme(*s)

print("Generated all YAML files.")
