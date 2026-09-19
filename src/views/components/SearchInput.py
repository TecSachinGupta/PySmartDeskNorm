from __future__ import annotations

from PySide6.QtWidgets import QLineEdit


class SearchInput(QLineEdit):
    def __init__(self, name=None, parent=None, placeholder="Search..."):
        super().__init__(parent)
        self.setObjectName(name or "searchInput")
        self.setPlaceholderText(placeholder)
        self.setClearButtonEnabled(True)
