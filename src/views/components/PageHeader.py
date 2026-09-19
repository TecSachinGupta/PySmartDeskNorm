from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget


class PageHeader(QWidget):
    def __init__(self, name=None, parent=None, title="", subtitle=None, actions=None):
        super().__init__(parent)
        self.setObjectName(name or "pageHeader")

        self.title_label = QLabel(title)
        self.title_label.setObjectName("pageHeaderTitle")

        self.subtitle_label = QLabel(subtitle or "")
        self.subtitle_label.setObjectName("pageHeaderSubtitle")
        self.subtitle_label.setVisible(bool(subtitle))

        text_column = QVBoxLayout()
        text_column.setContentsMargins(0, 0, 0, 0)
        text_column.setSpacing(2)
        text_column.addWidget(self.title_label)
        text_column.addWidget(self.subtitle_label)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(text_column)
        layout.addStretch(1)
        for action in actions or []:
            layout.addWidget(action)
