from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout


class ActionButton(QFrame):
    clicked = Signal()

    def __init__(self, name=None, parent=None, icon_text="\u25cf", title="", description=None):
        super().__init__(parent)
        self.setObjectName(name or "actionButton")
        self.setCursor(Qt.PointingHandCursor)

        icon_label = QLabel(icon_text)
        title_label = QLabel(title)
        title_label.setObjectName("actionButtonTitle")
        description_label = QLabel(description or "")
        description_label.setObjectName("actionButtonDescription")
        description_label.setVisible(bool(description))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)
        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(description_label)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)
