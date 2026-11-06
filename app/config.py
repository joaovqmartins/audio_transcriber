"""Configurações e constantes do aplicativo (caminhos, modelos, idiomas)."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

APP_NAME = "Audio Transcriber"
APP_SUBTITLE = "Transcrição de áudio na nuvem (Groq)"

SUPPORTED_EXTENSIONS = (".mp3", ".ogg", ".wav", ".m4a")

BASE_DIR = Path(__file__).resolve().parent.parent
ICONS_DIR = BASE_DIR / "assets" / "icons"
AUDIO_LOADED_ICON_PATH = ICONS_DIR / "audio-loaded-icon.png"

# Limite de tamanho de arquivo da API de transcrição da Groq.
MAX_FILE_SIZE_MB = 25

# Onde a chave de API é salva localmente (fora do repositório do projeto).
SETTINGS_DIR = Path.home() / ".audio_transcriber"
SETTINGS_FILE = SETTINGS_DIR / "settings.json"

GROQ_API_KEYS_URL = "https://console.groq.com/keys"


@dataclass(frozen=True)
class ModelOption:
    label: str
    model_id: str
    description: str


# Modelos Whisper hospedados pela Groq. Trocar de modelo é só mudar o
# "model_id" (nome aceito pela API da Groq).
MODEL_OPTIONS = [
    ModelOption(
        "Rápido",
        "whisper-large-v3-turbo",
        "Mais rápido e barato, ótima precisão para a maioria dos áudios.",
    ),
    ModelOption(
        "Preciso",
        "whisper-large-v3",
        "Máxima precisão da Groq, um pouco mais lento e com custo maior por minuto.",
    ),
]
DEFAULT_MODEL_INDEX = 1  # "Preciso": o app prioriza qualidade, conforme solicitado

LANGUAGE_OPTIONS: list[tuple[str, Optional[str]]] = [
    ("Detectar automaticamente", None),
    ("Português", "pt"),
    ("Inglês", "en"),
    ("Espanhol", "es"),
]
