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
