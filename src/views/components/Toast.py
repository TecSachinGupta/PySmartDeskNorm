from __future__ import annotations

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QLabel


class Toast(QLabel):
    def __init__(self, name=None, parent=None, duration_ms=2000):
        super().__init__(parent)
        self.setObjectName(name or "toast")
        self._duration_ms = duration_ms
        self.setAlignment(Qt.AlignCenter)
        self.setVisible(False)
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.hide)

    def show_message(self, message: str) -> None:
        self.setText(message)
        self.setVisible(True)
        self._timer.start(self._duration_ms)
