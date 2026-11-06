"""Persistência local de configurações do usuário (chave de API da Groq e tema)."""

import json
from typing import Optional

from app.config import SETTINGS_DIR, SETTINGS_FILE


def _read_settings() -> dict:
    try:
        data = json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return data if isinstance(data, dict) else {}


def _save_setting(key: str, value: str) -> None:
    """Grava uma configuração preservando as demais do arquivo."""
    data = _read_settings()
    data[key] = value
    SETTINGS_DIR.mkdir(parents=True, exist_ok=True)
    SETTINGS_FILE.write_text(json.dumps(data), encoding="utf-8")


def load_api_key() -> Optional[str]:
    """Lê a chave de API salva no disco, se existir."""
    return _read_settings().get("groq_api_key") or None


def save_api_key(api_key: str) -> None:
    """Salva a chave de API no disco, em um arquivo fora do repositório."""
    _save_setting("groq_api_key", api_key)


def load_theme_key() -> Optional[str]:
    return _read_settings().get("theme")


def save_theme_key(theme_key: str) -> None:
    _save_setting("theme", theme_key)
