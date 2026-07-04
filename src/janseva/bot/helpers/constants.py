"""
Constants for the JanSeva bot.
Includes all 22 scheduled languages of India and State-District mapping.
"""

# The 22 Scheduled Languages of India + English
# Format: lang_code: ("English Name", "Native Name")
LANGUAGES = {
    "hi": ("Hindi", "हिंदी"),
    "en": ("English", "English"),
    "as": ("Assamese", "অসমীয়া"),
    "bn": ("Bengali", "বাংলা"),
    "brx": ("Bodo", "बड़ो"),
    "doi": ("Dogri", "डोगरी"),
    "gu": ("Gujarati", "ગુજરાતી"),
    "kn": ("Kannada", "ಕನ್ನಡ"),
    "ks": ("Kashmiri", "कॉशुर"),
    "kok": ("Konkani", "कोंकणी"),
    "mai": ("Maithili", "मैथिली"),
    "ml": ("Malayalam", "മലയാളം"),
    "mni": ("Manipuri", "মৈতৈলোন্"),
    "mr": ("Marathi", "मराठी"),
    "ne": ("Nepali", "नेपाली"),
    "or": ("Odia", "ଓଡ଼ିଆ"),
    "pa": ("Punjabi", "ਪੰਜਾਬੀ"),
    "sa": ("Sanskrit", "संस्कृतम्"),
    "sat": ("Santali", "ᱥᱟᱱᱛᱟᱲᱤ"),
    "sd": ("Sindhi", "سنڌي"),
    "ta": ("Tamil", "தமிழ்"),
    "te": ("Telugu", "తెలుగు"),
    "ur": ("Urdu", "اردو"),
}

# State to District mapping (Representative subset of major districts for UI)
# A complete 780+ district list should be synced from a DB in a real production environment.
INDIA_DISTRICTS = {
    "Andhra Pradesh": ["Visakhapatnam", "Vijayawada", "Guntur", "Nellore", "Kurnool", "Other"],
    "Arunachal Pradesh": ["Itanagar", "Tawang", "Pasighat", "Other"],
    "Assam": ["Guwahati", "Silchar", "Dibrugarh", "Jorhat", "Other"],
    "Bihar": ["Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Other"],
    "Chhattisgarh": ["Raipur", "Bhilai", "Bilaspur", "Korba", "Other"],
    "Goa": ["North Goa", "South Goa"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Other"],
    "Haryana": ["Gurugram", "Faridabad", "Panipat", "Ambala", "Other"],
    "Himachal Pradesh": ["Shimla", "Manali", "Dharamshala", "Other"],
    "Jharkhand": ["Ranchi", "Jamshedpur", "Dhanbad", "Bokaro", "Other"],
    "Karnataka": ["Bengaluru", "Mysuru", "Hubballi", "Mangaluru", "Other"],
    "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur", "Other"],
    "Madhya Pradesh": ["Indore", "Bhopal", "Jabalpur", "Gwalior", "Ujjain", "Other"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Thane", "Nashik", "Other"],
    "Manipur": ["Imphal", "Churachandpur", "Thoubal", "Other"],
    "Meghalaya": ["Shillong", "Tura", "Jowai", "Other"],
    "Mizoram": ["Aizawl", "Lunglei", "Champhai", "Other"],
    "Nagaland": ["Kohima", "Dimapur", "Mokokchung", "Other"],
    "Odisha": ["Bhubaneswar", "Cuttack", "Rourkela", "Puri", "Other"],
    "Punjab": ["Ludhiana", "Amritsar", "Jalandhar", "Patiala", "Other"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Kota", "Bikaner", "Other"],
    "Sikkim": ["Gangtok", "Namchi", "Other"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Other"],
    "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Karimnagar", "Other"],
    "Tripura": ["Agartala", "Dharmanagar", "Udaipur", "Other"],
    "Uttar Pradesh": ["Lucknow", "Kanpur", "Varanasi", "Agra", "Noida", "Other"],
    "Uttarakhand": ["Dehradun", "Haridwar", "Roorkee", "Nainital", "Other"],
    "West Bengal": ["Kolkata", "Howrah", "Darjeeling", "Siliguri", "Other"],
    "Delhi": ["Central Delhi", "New Delhi", "South Delhi", "Other"],
    "Jammu and Kashmir": ["Srinagar", "Jammu", "Anantnag", "Other"],
    "Other UTs": ["Chandigarh", "Puducherry", "Andaman", "Lakshadweep", "Ladakh"]
}
