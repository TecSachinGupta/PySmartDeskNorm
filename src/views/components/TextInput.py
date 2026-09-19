from __future__ import annotations

from PySide6.QtWidgets import QLineEdit


class TextInput(QLineEdit):
    def __init__(self, name=None, parent=None, placeholder="", text=""):
        super().__init__(parent)
        self.setObjectName(name or "textInput")
        if placeholder:
            self.setPlaceholderText(placeholder)
        if text:
            self.setText(text)
