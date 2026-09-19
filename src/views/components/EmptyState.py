from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class EmptyState(QWidget):
    def __init__(
        self, name=None, parent=None, icon_text="\u2205", title="Nothing here", description=None
    ):
        super().__init__(parent)
        self.setObjectName(name or "emptyState")

        self.icon_label = QLabel(icon_text)
        self.icon_label.setObjectName("emptyStateIcon")
        self.icon_label.setAlignment(Qt.AlignCenter)

        self.title_label = QLabel(title)
        self.title_label.setObjectName("emptyStateTitle")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.description_label = QLabel(description or "")
        self.description_label.setObjectName("emptyStateDescription")
        self.description_label.setAlignment(Qt.AlignCenter)
        self.description_label.setVisible(bool(description))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(6)
        layout.addWidget(self.icon_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.description_label)
