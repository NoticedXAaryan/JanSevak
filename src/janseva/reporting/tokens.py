"""
Anonymous report token system.
Generates secure, random tokens for two-way communication
without revealing the reporter's identity.
"""

import secrets
import string


def generate_report_token() -> str:
    """
    Generate a secure, human-readable report token.
    Format: XXXX-XXXX-XXXX (12 alphanumeric chars, uppercase)

    Example: "K7M2-P9X4-R1N6"

    This token is the reporter's ONLY way to check their report status.
    It cannot be linked back to their Telegram account.
    """
    chars = string.ascii_uppercase + string.digits
    # Remove confusing characters (O/0, I/1, L)
    chars = (
        chars.replace("O", "").replace("0", "").replace("I", "").replace("1", "").replace("L", "")
    )

    part1 = "".join(secrets.choice(chars) for _ in range(4))
    part2 = "".join(secrets.choice(chars) for _ in range(4))
    part3 = "".join(secrets.choice(chars) for _ in range(4))

    return f"{part1}-{part2}-{part3}"
