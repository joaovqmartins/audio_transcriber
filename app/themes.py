"""Temas do aplicativo: cada ícone selecionável define a paleta completa da interface."""

from dataclasses import dataclass
from pathlib import Path

from app.config import ICONS_DIR


@dataclass(frozen=True)
class Theme:
    key: str
    label: str
    icon_path: Path
    is_dark: bool  # controla os botões nativos da barra de título do Windows
    bg_start: str  # degradê vertical do fundo da janela
    bg_end: str
    panel: str  # botões secundários e popups
    panel_hover: str
    input_bg: str  # campos de texto e combos
    border: str
    text: str
    text_muted: str
    accent: str  # botão principal
    accent_hover: str
    accent_pressed: str
    on_accent: str  # texto sobre o botão principal
    accent_line: str  # bordas e indicadores finos; pode ser mais escuro que `accent` para contrastar
    disabled_bg: str
    disabled_text: str
    danger: str = "#dc2626"
    danger_hover: str = "#ef4444"
    danger_pressed: str = "#b91c1c"
    error: str = "#b91c1c"  # texto de erro na linha de status


THEMES = {
    theme.key: theme
    for theme in (
        Theme(
            key="default",
            label="Padrão",
            icon_path=ICONS_DIR / "app-icon-default.png",
            is_dark=True,
            bg_start="#0d1117",
            bg_end="#10141b",
            panel="#161b22",
            panel_hover="#1c2129",
            input_bg="#0d1117",
            border="#252b35",
            text="#e2e8f0",
            text_muted="#a1aab7",
            accent="#6366f1",
            accent_hover="#818cf8",
            accent_pressed="#4f52c1",
            on_accent="#ffffff",
            accent_line="#6366f1",
            disabled_bg="#12161d",
            disabled_text="#4a4f58",
            error="#f87171",
        ),
        Theme(
            key="cyan-wine",
            label="Ciano e Vinho",
            icon_path=ICONS_DIR / "app-icon-cyan-wine.png",
            is_dark=True,
            bg_start="#5a2e4d",
            bg_end="#3f1f36",
            panel="#6d3a5e",
            panel_hover="#7a4469",
            input_bg="#321829",
            border="#7d4f6f",
            text="#f2fbfa",
            text_muted="#d9c9d4",
            accent="#6ae5d9",
            accent_hover="#8eeee4",
            accent_pressed="#45c4b8",
            on_accent="#2a1322",
            accent_line="#6ae5d9",
            disabled_bg="#4a2740",
            disabled_text="#94768b",
            error="#ffb3b3",
        ),
        Theme(
            key="gray-bronze",
            label="Cinza e Bronze",
            icon_path=ICONS_DIR / "app-icon-gray-bronze.png",
            is_dark=False,
            bg_start="#f1f2f4",
            bg_end="#dfe2e5",
            panel="#fbfbfc",
            panel_hover="#e9ebee",
            input_bg="#ffffff",
            border="#b9bfc5",
            text="#1a1d20",
            text_muted="#505960",
            accent="#a88b6c",
            accent_hover="#b99e82",
            accent_pressed="#8f7355",
            on_accent="#050505",
            accent_line="#8a6d4e",
            disabled_bg="#e4e6e9",
            disabled_text="#8a9198",
        ),
        Theme(
            key="blue-lime",
            label="Azul e Verde Limão",
            icon_path=ICONS_DIR / "app-icon-blue-lime.png",
            is_dark=False,
            bg_start="#96c2f9",
            bg_end="#7fa8e0",
            panel="#dbe9fb",
            panel_hover="#c6dbf7",
            input_bg="#eef5fe",
            border="#5f7fa8",
            text="#0f2238",
            text_muted="#1b3350",
            accent="#85e236",
            accent_hover="#9cec57",
            accent_pressed="#6cc421",
            on_accent="#12263d",
            accent_line="#2a4666",
            disabled_bg="#a9c8ee",
            disabled_text="#4f6e96",
            error="#7a0f0f",
        ),
        Theme(
            key="pastel",
            label="Pastéis",
            icon_path=ICONS_DIR / "app-icon-pastel.png",
            is_dark=False,
            bg_start="#a7c9be",
            bg_end="#dfb3a3",
            panel="#f3ece6",
            panel_hover="#e8ddd4",
            input_bg="#f8f3ee",
            border="#8e9a95",
            text="#262626",
            text_muted="#3a3f3d",
            accent="#d6817c",
            accent_hover="#e09a95",
            accent_pressed="#bf6a65",
            on_accent="#1f1f1f",
            accent_line="#a8504b",
            disabled_bg="#c9c0b6",
            disabled_text="#7b7570",
            error="#7a0f0f",
        ),
    )
}

DEFAULT_THEME_KEY = "default"


def get_theme(key: str | None) -> Theme:
    """Retorna o tema salvo, ou o padrão se a chave for desconhecida."""
    return THEMES.get(key, THEMES[DEFAULT_THEME_KEY])
