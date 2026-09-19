from __future__ import annotations

from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout


class ActivityCard(QFrame):
    def __init__(self, name=None, parent=None, title="Recent Activity", entries=None):
        super().__init__(parent)
        self.setObjectName(name or "activityCard")

        title_label = QLabel(title)
        title_label.setObjectName("activityCardTitle")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)
        layout.addWidget(title_label)

        for entry in entries or []:
            row = QHBoxLayout()
            text_label = QLabel(entry.get("text", ""))
            timestamp_label = QLabel(entry.get("timestamp", ""))
            timestamp_label.setObjectName("activityCardTimestamp")
            row.addWidget(text_label)
            row.addStretch(1)
            row.addWidget(timestamp_label)
            layout.addLayout(row)
