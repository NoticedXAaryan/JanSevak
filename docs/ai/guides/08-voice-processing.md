# Guide 08: Voice Processing Pipeline

## What This Does
Enables users to send voice notes in Hindi or any Indian language and receive voice responses. The pipeline: Voice Note → STT (IndicWhisper) → AI Agent → TTS (IndicTTS) → Voice Response.

## Prerequisites
- Guide 02 completed (Telegram bot with voice handler stub)
- Guide 03 completed (AI agent core)
- `ffmpeg` installed on the system (for audio conversion)

---

## Technology

### Speech-to-Text: AI4Bharat IndicWhisper
- Fine-tuned OpenAI Whisper for 22 Indian languages
- Handles code-mixing (Hinglish)
- Models on HuggingFace: `ai4bharat/indicwhisper-large-v3`

### Text-to-Speech: AI4Bharat IndicTTS
- Natural-sounding voices for Indian languages
- Multiple speaker options per language

### Alternative: Bhashini API
- If self-hosting models is not feasible (GPU requirements), use the Bhashini API
- Free API from the Government of India's NLTM project
- Provides ASR, TTS, and translation as cloud services

---

## Implementation Steps

### 1. Audio Utilities

**File: `src/janseva/voice/audio_utils.py`**

```python
"""Audio format conversion utilities."""
from pathlib import Path
from pydub import AudioSegment
import tempfile


def ogg_to_wav(ogg_path: str) -> str:
    """Convert Telegram's OGG voice file to WAV for STT model."""
    audio = AudioSegment.from_ogg(ogg_path)
    audio = audio.set_frame_rate(16000).set_channels(1)  # 16kHz mono for Whisper
    
    wav_path = tempfile.mktemp(suffix=".wav")
    audio.export(wav_path, format="wav")
    return wav_path


def text_to_audio_file(audio_bytes: bytes, format: str = "mp3") -> str:
    """Save audio bytes to a temporary file."""
    path = tempfile.mktemp(suffix=f".{format}")
    with open(path, "wb") as f:
        f.write(audio_bytes)
    return path
```

### 2. STT Service

**File: `src/janseva/voice/stt.py`**

```python
"""Speech-to-Text service using IndicWhisper or standard Whisper."""
import whisper
import structlog

logger = structlog.get_logger()

# Load model once at module level
_model = None

def get_model():
    global _model
    if _model is None:
        # Use "large-v3" for best quality, "base" for speed
        _model = whisper.load_model("base")  # Change to "large-v3" for production
        logger.info("whisper_model_loaded", model="base")
    return _model


def transcribe(audio_path: str) -> dict:
    """
    Transcribe audio file to text.
    
    Returns:
        dict with keys: text, language, segments
    """
    model = get_model()
    result = model.transcribe(
        audio_path,
        task="transcribe",
        language=None,  # Auto-detect
    )
    
    logger.info(
        "transcription_complete",
        language=result.get("language"),
        text_length=len(result.get("text", "")),
    )
    
    return {
        "text": result["text"].strip(),
        "language": result.get("language", "hi"),
        "segments": result.get("segments", []),
    }
```

### 3. TTS Service (stub — implementation depends on model choice)

```python
"""Text-to-Speech service. 
Choose implementation based on whether you self-host or use Bhashini API."""
# Option A: Bhashini API (recommended for simplicity)
# Option B: Self-hosted IndicTTS models
```

### 4. Updated Voice Handler

Update `src/janseva/bot/routers/voice.py` to:
1. Download the voice file from Telegram
2. Convert OGG → WAV
3. Run STT → get text + detected language
4. Pass text through the AI agent pipeline
5. (Optional) Convert response to speech via TTS
6. Send text response (and voice response if TTS available)

---

## System Requirements for Voice

| Model | RAM | GPU | Speed |
|-------|-----|-----|-------|
| Whisper base | 1 GB | Not needed | ~10x realtime |
| Whisper large-v3 | 10 GB | 8GB+ VRAM recommended | ~1x realtime |
| IndicWhisper large | 10 GB | 8GB+ VRAM recommended | ~1x realtime |

For testing without GPU: use Whisper "base" model — lower accuracy but works on CPU.
For production: use IndicWhisper large-v3 on a GPU-enabled server, or use Bhashini API.

---

## Git Checkpoint

```bash
git add -A
git commit -m "feat(voice): implement voice processing pipeline

- Audio conversion: OGG → WAV (pydub + ffmpeg)
- STT service with Whisper (auto language detection)
- Voice handler: download → transcribe → agent → respond
- Language persistence for voice users"
```
