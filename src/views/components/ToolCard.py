from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout


class ToolCard(QFrame):
    clicked = Signal(str)

    def __init__(self, name=None, parent=None, tool_id="", title="", category="", description=None):
        super().__init__(parent)
        self.setObjectName(name or "toolCard")
        self.tool_id = tool_id
        self.title_text = title
        self.category = category
        self.setCursor(Qt.PointingHandCursor)

        title_label = QLabel(title)
        title_label.setObjectName("toolCardTitle")
        category_label = QLabel(category)
        category_label.setObjectName("toolCardCategory")
        description_label = QLabel(description or "")
        description_label.setObjectName("toolCardDescription")
        description_label.setVisible(bool(description))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)
        layout.addWidget(title_label)
        layout.addWidget(category_label)
        layout.addWidget(description_label)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.tool_id)
        super().mousePressEvent(event)
