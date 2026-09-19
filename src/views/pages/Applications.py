from __future__ import annotations

from typing import ClassVar

from PySide6.QtWidgets import QVBoxLayout, QWidget

from constants import PAGE_ID_APPLICATIONS
from views.components.ActionButton import ActionButton
from views.components.PageHeader import PageHeader
from views.components.Row import Row
from views.components.SectionCard import SectionCard


class Applications(QWidget):
    page_id = PAGE_ID_APPLICATIONS

    # Illustrative placeholders only; no real application tracking yet.
    DEMO_ENTRIES: ClassVar[list[dict[str, str]]] = [
        {"title": "Visual Studio Code", "description": "Code editor"},
        {"title": "Terminal", "description": "Command line"},
        {"title": "Browser", "description": "Web browser"},
    ]

    def __init__(self, name=None, parent=None, settings=None):
        super().__init__(parent)
        self.setObjectName(name or "applicationsPage")
        self.settings = settings or {}

        header = PageHeader(title="Applications", subtitle="Tracked applications (demo data)")

        self.entry_buttons = [
            ActionButton(icon_text="\u25a3", title=entry["title"], description=entry["description"])
            for entry in self.DEMO_ENTRIES
        ]
        entries_row = Row(name="applicationsRow", widgets=self.entry_buttons)
        section = SectionCard(title="Tracked Applications", content_widgets=[entries_row])

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        layout.addWidget(header)
        layout.addWidget(section)
        layout.addStretch(1)
