from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class EmptyState(QWidget):
    def __init__(
        self, name=None, parent=None, icon_text="\u2205", title="Nothing here", description=None
    ):
        super().__init__(parent)
        self.setObjectName(name or "emptyState")

        icon_label = QLabel(icon_text)
        icon_label.setObjectName("emptyStateIcon")
        icon_label.setAlignment(Qt.AlignCenter)

        title_label = QLabel(title)
        title_label.setObjectName("emptyStateTitle")
        title_label.setAlignment(Qt.AlignCenter)

        description_label = QLabel(description or "")
        description_label.setObjectName("emptyStateDescription")
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setVisible(bool(description))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(6)
        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(description_label)
