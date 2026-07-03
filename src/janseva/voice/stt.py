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
