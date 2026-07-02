# Guide 12: WhatsApp Integration

## What This Does
Adds WhatsApp as a second messaging channel, reusing all existing AI agent logic via the Channel Normalizer pattern.

## Prerequisites
- Guides 01-03 completed (full Telegram pipeline working)
- WhatsApp Business API access (via Twilio or Meta Cloud API)

---

## Architecture: Channel Normalizer

The key design pattern: **all channels normalize to a unified message format** before reaching the AI agent.

```python
# src/janseva/common/channel.py

from dataclasses import dataclass
from enum import Enum


class ChannelType(Enum):
    TELEGRAM = "telegram"
    WHATSAPP = "whatsapp"


@dataclass
class UnifiedMessage:
    """Platform-agnostic message format."""
    channel: ChannelType
    user_id: str           # Platform-specific user ID
    text: str | None
    voice_file_url: str | None
    language: str
    timestamp: str
    
    # Platform-specific reply function
    reply_func: callable   # async function to send response back


@dataclass
class UnifiedResponse:
    """Platform-agnostic response format."""
    text: str
    voice_file_path: str | None = None
```

## WhatsApp Implementation Options

### Option A: Twilio WhatsApp API (Recommended for simplicity)
- Create a Twilio account → activate WhatsApp sandbox
- Use webhook to receive messages
- Use REST API to send responses
- Voice note support built-in

### Option B: Meta Cloud API (Direct)
- Register on Meta for Developers
- Set up WhatsApp Business API
- More complex but no middleman costs

---

## Implementation Steps

1. Choose WhatsApp API provider (Twilio recommended for testing)
2. Build WhatsApp webhook handler (FastAPI endpoint)
3. Implement WhatsApp → UnifiedMessage normalizer
4. Reuse the existing agent pipeline (same `process_message` function)
5. Build response sender (text + voice for WhatsApp)
6. Handle WhatsApp-specific features (buttons, lists, media)

---

## Git Checkpoint
```bash
git add -A
git commit -m "feat(whatsapp): add WhatsApp as second messaging channel"
```
