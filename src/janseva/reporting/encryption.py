"""
Encryption for anonymous report content.
Uses Fernet symmetric encryption (AES-128-CBC).
"""

from cryptography.fernet import Fernet

from janseva.config import settings

_dev_fernet_key: str | None = None


def get_fernet() -> Fernet:
    """Get the Fernet encryption instance.

    A placeholder key must not mint a new secret on every call, or development
    ciphertext written earlier in the process can never be decrypted.
    """
    global _dev_fernet_key
    key = settings.report_encryption_key
    if not key or key == "change-me":
        if settings.env == "production":
            raise ValueError(
                "REPORT_ENCRYPTION_KEY must be set in production to prevent data loss."
            )
        if _dev_fernet_key is None:
            _dev_fernet_key = Fernet.generate_key().decode()
        key = _dev_fernet_key
    return Fernet(key.encode() if isinstance(key, str) else key)


def encrypt_content(plaintext: str) -> str:
    """Encrypt report content. Returns base64-encoded ciphertext."""
    f = get_fernet()
    return f.encrypt(plaintext.encode("utf-8")).decode("utf-8")


def decrypt_content(ciphertext: str) -> str:
    """Decrypt report content. Returns plaintext."""
    f = get_fernet()
    return f.decrypt(ciphertext.encode("utf-8")).decode("utf-8")
