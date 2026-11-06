"""Folha de estilo (QSS) e paleta geradas a partir do tema ativo.

Fica num módulo à parte (em vez de dentro de main_window.py) para poder ser
aplicada também no SettingsDialog: em alguns ambientes Linux, um QDialog não
herda automaticamente o stylesheet do widget pai, e acabava aparecendo com o
tema claro padrão do sistema — destoando do resto do app.
"""

from __future__ import annotations

from PySide6.QtGui import QColor, QPalette

from app.themes import Theme


def _rgba(hex_color: str, alpha: float) -> str:
    color = QColor(hex_color)
    return f"rgba({color.red()}, {color.green()}, {color.blue()}, {alpha})"


def build_palette(theme: Theme) -> QPalette:
    """Cobre o que o QSS não alcança, como barras de rolagem e links em QLabel."""
    palette = QPalette()
    role = QPalette.ColorRole
    for color_role, color in (
        (role.Window, theme.bg_start),
        (role.WindowText, theme.text),
        (role.Base, theme.input_bg),
        (role.AlternateBase, theme.panel),
        (role.Text, theme.text),
        (role.PlaceholderText, theme.text_muted),
        (role.Button, theme.panel),
        (role.ButtonText, theme.text),
        (role.ToolTipBase, theme.panel),
        (role.ToolTipText, theme.text),
        (role.Highlight, theme.accent),
        (role.HighlightedText, theme.on_accent),
        (role.Link, theme.accent_line),
        (role.LinkVisited, theme.accent_line),
    ):
        palette.setColor(color_role, QColor(color))
    return palette


def style_panel_button(button, theme: Theme) -> None:
    button.set_color_scheme(
        theme.panel,
        theme.panel_hover,
        theme.accent,
        text_color=theme.text,
        disabled_color=theme.disabled_bg,
        disabled_text_color=theme.disabled_text,
    )


def style_accent_button(button, theme: Theme) -> None:
    button.set_color_scheme(
        theme.accent,
        theme.accent_hover,
        theme.accent_pressed,
        text_color=theme.on_accent,
        disabled_color=theme.disabled_bg,
        disabled_text_color=theme.disabled_text,
    )


def build_style_sheet(theme: Theme) -> str:
    return f"""
QMainWindow, QDialog {{
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 {theme.bg_start}, stop:1 {theme.bg_end});
}}
QWidget#central {{
    background: transparent;
}}
QWidget {{
    color: {theme.text};
    font-family: 'Segoe UI', sans-serif;
}}
QToolTip {{
    background-color: {theme.panel};
    color: {theme.text};
    border: 1px solid {theme.border};
}}
QLabel#appTitle {{
    font-size: 22px;
    font-weight: 700;
    letter-spacing: 0.5px;
}}
QLabel#appSubtitle {{
    font-size: 12px;
    color: {theme.text_muted};
}}
QLabel#dropIcon {{
    border: none;
    background: transparent;
}}
QLabel#dropTitle {{
    font-size: 14px;
    font-weight: 600;
    border: none;
    background: transparent;
}}
QLabel#dropSubtitle {{
    font-size: 11px;
    color: {theme.text_muted};
    border: none;
    background: transparent;
}}
QLabel#statusLabel {{
    font-size: 12px;
    min-height: 16px;
}}
QLabel#sectionTitle {{
    font-size: 12px;
    font-weight: 600;
    color: {theme.text_muted};
}}
QPushButton {{
    background-color: {theme.panel};
    color: {theme.text};
    border: 1px solid {theme.border};
    border-radius: 14px;
    padding: 8px 16px;
    font-weight: 600;
}}
QPushButton:hover:!disabled {{
    background-color: {theme.panel_hover};
    border-color: {theme.accent_line};
}}
QPushButton:pressed:!disabled {{
    background-color: {theme.accent};
    border-color: {theme.accent};
    color: {theme.on_accent};
}}
QPushButton:disabled {{
    background-color: {theme.disabled_bg};
    color: {theme.disabled_text};
    border-color: {theme.border};
}}
QPushButton#iconButton {{
    background-color: transparent;
    border: none;
    color: {theme.text};
    border-radius: 18px;
    padding: 0px;
}}
QPushButton#iconButton:hover:!disabled {{
    background-color: {_rgba(theme.text, 0.10)};
}}
QPushButton#iconButton:pressed:!disabled {{
    background-color: {_rgba(theme.text, 0.18)};
}}
QTextEdit, QLineEdit {{
    background-color: {theme.input_bg};
    border: 1px solid {theme.border};
    border-radius: 16px;
    padding: 10px 14px;
    font-size: 13px;
}}
QLineEdit:focus, QTextEdit:focus {{
    border-color: {theme.accent_line};
}}
QComboBox {{
    background-color: {theme.input_bg};
    border: 1px solid {theme.border};
    border-radius: 14px;
    padding: 5px 10px;
}}
QComboBox:hover {{
    border-color: {theme.accent_line};
}}
QComboBox::drop-down {{
    border: none;
}}
QComboBox QAbstractItemView {{
    background-color: {theme.panel};
    color: {theme.text};
    border: 1px solid {theme.border};
    border-radius: 10px;
    outline: none;
    selection-background-color: {theme.accent};
    selection-color: {theme.on_accent};
}}
QComboBox QAbstractItemView::item {{
    padding: 6px 10px 6px 8px;
    border-left: 3px solid transparent;
}}
QComboBox QAbstractItemView::item:selected {{
    background-color: {_rgba(theme.accent_line, 0.18)};
    color: {theme.text};
    border-left: 3px solid {theme.accent_line};
}}
QComboBox QAbstractItemView::item:hover {{
    background-color: {_rgba(theme.text_muted, 0.16)};
}}
"""
