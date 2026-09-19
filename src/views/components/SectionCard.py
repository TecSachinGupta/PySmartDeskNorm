from __future__ import annotations

from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout


class SectionCard(QFrame):
    def __init__(self, name=None, parent=None, title=None, content_widgets=None):
        super().__init__(parent)
        self.setObjectName(name or "sectionCard")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)

        if title:
            title_label = QLabel(title)
            title_label.setObjectName("sectionCardTitle")
            layout.addWidget(title_label)

        for widget in content_widgets or []:
            layout.addWidget(widget)
