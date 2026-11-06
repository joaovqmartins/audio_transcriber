"""Diálogo de configurações: chave de API da Groq e tema do aplicativo."""

from __future__ import annotations

from typing import Optional

from PySide6.QtCore import QTimer, Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QVBoxLayout,
)

from app.config import GROQ_API_KEYS_URL
from app.themes import THEMES, Theme
from app.ui.icons import lock_icon
from app.ui.style import build_style_sheet, style_accent_button, style_panel_button
from app.ui.title_bar import apply_title_bar
from app.ui.widgets import RoundedButton, ThemeIconButton
from app.utils.settings import load_api_key, save_api_key, save_theme_key


class SettingsDialog(QDialog):
    theme_selected = Signal(object)

    def __init__(self, theme: Theme, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configurações")
        self.setMinimumWidth(420)
        self._initial_theme = theme
        self.theme = theme

        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        info = QLabel(
            "A transcrição é feita pela API da Groq. Informe sua chave de API "
            f'gratuita (obtida em <a href="{GROQ_API_KEYS_URL}">{GROQ_API_KEYS_URL}</a>).'
        )
        info.setWordWrap(True)
        info.setOpenExternalLinks(True)
        layout.addWidget(info)

        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_input.setPlaceholderText("gsk_...")
        saved_key = load_api_key()
        if saved_key:
            self.api_key_input.setText(saved_key)
        layout.addWidget(self.api_key_input)

        self.show_key_button = RoundedButton("Mostrar", bg_color=theme.panel, radius=14)
        self.show_key_button.setCheckable(True)
        self.show_key_button.toggled.connect(self._toggle_visibility)

        row = QHBoxLayout()
        row.addWidget(self.show_key_button)
        row.addStretch()
        layout.addLayout(row)

        theme_title = QLabel("Tema")
        theme_title.setObjectName("sectionTitle")
        layout.addWidget(theme_title)

        self._theme_buttons: dict[str, ThemeIconButton] = {}
        theme_group = QButtonGroup(self)
        theme_row = QHBoxLayout()
        theme_row.setSpacing(8)
        for option in THEMES.values():
            button = ThemeIconButton(option.icon_path, option.label)
            button.setChecked(option.key == theme.key)
            button.clicked.connect(lambda _checked, key=option.key: self._select_theme(key))
            theme_group.addButton(button)
            theme_row.addWidget(button)
            self._theme_buttons[option.key] = button
        theme_row.addStretch()
        layout.addLayout(theme_row)

        self.theme_name_label = QLabel(theme.label)
        self.theme_name_label.setObjectName("appSubtitle")
        layout.addWidget(self.theme_name_label)

        buttons_row = QHBoxLayout()
        buttons_row.addStretch()
        self.cancel_button = RoundedButton("Cancelar", bg_color=theme.panel, radius=14)
        self.cancel_button.clicked.connect(self.reject)
        self.save_button = RoundedButton("Salvar", bg_color=theme.accent, radius=14)
        self.save_button.clicked.connect(self._on_save)
        buttons_row.addWidget(self.cancel_button)
        buttons_row.addWidget(self.save_button)
        layout.addLayout(buttons_row)

        self._apply_theme()

    def showEvent(self, event) -> None:  # noqa: N802 (nome exigido pelo Qt)
        super().showEvent(event)
        QTimer.singleShot(0, lambda: apply_title_bar(self, self.theme))

    def _apply_theme(self) -> None:
        # Aplicado explicitamente (não basta herdar do pai): em alguns
        # ambientes Linux um QDialog não herda o stylesheet da janela pai e
        # aparece com o tema claro padrão do sistema.
        self.setStyleSheet(build_style_sheet(self.theme))
        self.setWindowIcon(lock_icon(self.theme.text, size=32))
        style_panel_button(self.show_key_button, self.theme)
        style_panel_button(self.cancel_button, self.theme)
        style_accent_button(self.save_button, self.theme)
        self.theme_name_label.setText(self.theme.label)
        for button in self._theme_buttons.values():
            button.set_ring_colors(self.theme.accent_line, self.theme.text_muted)
        if self.isVisible():
            apply_title_bar(self, self.theme)

    def _select_theme(self, key: str) -> None:
        """Aplica na hora, como prévia; só fica salvo ao clicar em Salvar."""
        self.theme = THEMES[key]
        self._apply_theme()
        self.theme_selected.emit(self.theme)

    def _toggle_visibility(self, checked: bool) -> None:
        mode = QLineEdit.EchoMode.Normal if checked else QLineEdit.EchoMode.Password
        self.api_key_input.setEchoMode(mode)
        self.show_key_button.setText("Ocultar" if checked else "Mostrar")

    def _on_save(self) -> None:
        api_key = self.api_key_input.text().strip()
        if api_key:
            save_api_key(api_key)
        save_theme_key(self.theme.key)
        self.accept()

    def reject(self) -> None:
        if self.theme is not self._initial_theme:
            self.theme_selected.emit(self._initial_theme)
        super().reject()

    @staticmethod
    def get_saved_api_key() -> Optional[str]:
        return load_api_key()
