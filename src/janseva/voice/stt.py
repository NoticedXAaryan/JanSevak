"""Speech-to-Text service using IndicWhisper or standard Whisper."""

import structlog
from faster_whisper import WhisperModel

logger = structlog.get_logger()

# Load model once at module level
_model = None


def get_model():
    global _model
    if _model is None:
        # Use "base" or "tiny" for speed, "large-v3" for production
        _model = WhisperModel("base", device="cpu", compute_type="int8")
        logger.info("faster_whisper_model_loaded", model="base")
    return _model


import asyncio

async def transcribe(audio_path: str) -> dict:
    """
    Transcribe audio file to text.
    Runs asynchronously off the main thread to prevent blocking the event loop.

    Returns:
        dict with keys: text, language, segments
    """
    model = get_model()
    
    # Run heavy whisper processing in a thread pool
    # faster-whisper returns an iterator of segments and an info object
    def _run_transcription():
        segments, info = model.transcribe(audio_path, beam_size=5)
        text = "".join([segment.text for segment in segments])
        return {"text": text, "language": info.language, "segments": segments}
        
    result = await asyncio.to_thread(_run_transcription)

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
