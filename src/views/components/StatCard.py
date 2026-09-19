from __future__ import annotations

from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout


class StatCard(QFrame):
    def __init__(
        self, name=None, parent=None, icon_text="\u25cf", title="", value="", description=None
    ):
        super().__init__(parent)
        self.setObjectName(name or "statCard")

        icon_label = QLabel(icon_text)
        title_label = QLabel(title)
        title_label.setObjectName("statCardTitle")
        self.value_label = QLabel(value)
        self.value_label.setObjectName("statCardValue")
        description_label = QLabel(description or "")
        description_label.setObjectName("statCardDescription")
        description_label.setVisible(bool(description))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(4)
        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(description_label)
