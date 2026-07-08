"""
Encryption for anonymous report content.
Uses Fernet symmetric encryption (AES-128-CBC).
"""

from cryptography.fernet import Fernet

from janseva.config import settings


def get_fernet() -> Fernet:
    """Get the Fernet encryption instance."""
    key = settings.report_encryption_key
    if key == "change-me":
        # Generate a key for development — in production, set a real key
        key = Fernet.generate_key().decode()
    return Fernet(key.encode() if isinstance(key, str) else key)


def encrypt_content(plaintext: str) -> str:
    """Encrypt report content. Returns base64-encoded ciphertext."""
    f = get_fernet()
    return f.encrypt(plaintext.encode("utf-8")).decode("utf-8")


def decrypt_content(ciphertext: str) -> str:
    """Decrypt report content. Returns plaintext."""
    f = get_fernet()
    return f.decrypt(ciphertext.encode("utf-8")).decode("utf-8")
