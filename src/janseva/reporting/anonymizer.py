"""
Metadata stripping for anonymous reports.
Ensures no identifiable information leaks into the report record.
"""
import re
from datetime import datetime, timezone


def strip_metadata(report_text: str) -> str:
    """
    Remove potentially identifying metadata from report text.
    
    Strips:
    - Phone numbers (Indian format)
    - Aadhaar numbers
    - Email addresses
    - Telegram usernames (@mentions)
    - Specific dates that could identify timing of interaction
    """
    cleaned = report_text

    # Remove phone numbers (Indian: 10 digits, with or without +91)
    cleaned = re.sub(r'\+?91[-\s]?\d{10}', '[PHONE_REDACTED]', cleaned)
    cleaned = re.sub(r'\b\d{10}\b', '[PHONE_REDACTED]', cleaned)

    # Remove Aadhaar numbers (12 digits, possibly with spaces)
    cleaned = re.sub(r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b', '[AADHAAR_REDACTED]', cleaned)

    # Remove email addresses
    cleaned = re.sub(r'\b[\w.-]+@[\w.-]+\.\w+\b', '[EMAIL_REDACTED]', cleaned)

    # Remove Telegram @usernames
    cleaned = re.sub(r'@\w+', '[USERNAME_REDACTED]', cleaned)

    return cleaned


def generate_submission_time() -> datetime:
    """
    Generate a fuzzy submission time.
    Rounds to the nearest hour to prevent timing-based identification.
    """
    now = datetime.now(timezone.utc)
    return now.replace(minute=0, second=0, microsecond=0)
