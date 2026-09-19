from __future__ import annotations

from PySide6.QtWidgets import QComboBox


class ComboBox(QComboBox):
    def __init__(self, name=None, parent=None, items=None, current=None):
        super().__init__(parent)
        self.setObjectName(name or "comboBox")
        for item in items or []:
            self.addItem(item)
        if current is not None:
            index = self.findText(current)
            if index >= 0:
                self.setCurrentIndex(index)
