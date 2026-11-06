"""Notificações nativas do sistema, usadas quando o app não está em foco."""

from __future__ import annotations

from PySide6.QtCore import QObject, QTimer, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QSystemTrayIcon

from app.config import APP_NAME


class SystemNotifier(QObject):
    """Mostra notificações via bandeja do sistema, sem deixar um ícone fixo nela.

    O Qt só exibe notificações com o ícone da bandeja visível, então ele
    aparece junto com a mensagem e some logo depois. Sem suporte a bandeja
    (alguns ambientes Linux), a notificação é simplesmente ignorada.
    """

    clicked = Signal()

    DISPLAY_MS = 8000
    TRAY_LINGER_MS = 10000

    def __init__(self, parent=None):
        super().__init__(parent)
        self._icon = QIcon()
        self._tray = QSystemTrayIcon(self)
        self._tray.setToolTip(APP_NAME)
        self._tray.messageClicked.connect(self._on_message_clicked)

        self._hide_timer = QTimer(self)
        self._hide_timer.setSingleShot(True)
        self._hide_timer.setInterval(self.TRAY_LINGER_MS)
        self._hide_timer.timeout.connect(self._tray.hide)

    def set_icon(self, icon: QIcon) -> None:
        self._icon = icon
        self._tray.setIcon(icon)

    def notify(self, title: str, message: str, error: bool = False) -> None:
        if not (QSystemTrayIcon.isSystemTrayAvailable() and QSystemTrayIcon.supportsMessages()):
            return

        self._tray.show()
        icon = QSystemTrayIcon.MessageIcon.Critical if error else self._icon
        self._tray.showMessage(title, message, icon, self.DISPLAY_MS)
        self._hide_timer.start()

    def _on_message_clicked(self) -> None:
        self._hide_timer.stop()
        self._tray.hide()
        self.clicked.emit()
