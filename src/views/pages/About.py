from __future__ import annotations

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from constants import PAGE_ID_ABOUT
from views.components.PageHeader import PageHeader
from views.components.SectionCard import SectionCard


class About(QWidget):
    page_id = PAGE_ID_ABOUT

    def __init__(self, name=None, parent=None, settings=None):
        super().__init__(parent)
        self.setObjectName(name or "aboutPage")
        self.settings = settings or {}

        app_name = self.settings.get("app_name", "")
        version = self.settings.get("version", "")
        description = self.settings.get("description", "")
        copyright_text = self.settings.get("copyright", "")
        year = self.settings.get("year", "")

        header = PageHeader(title=app_name, subtitle=f"Version {version}")

        description_label = QLabel(description)
        description_label.setObjectName("aboutDescription")
        description_label.setWordWrap(True)

        copyright_label = QLabel(f"{copyright_text} {year}".strip())
        copyright_label.setObjectName("aboutCopyright")

        section = SectionCard(title="About", content_widgets=[description_label, copyright_label])

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        layout.addWidget(header)
        layout.addWidget(section)
        layout.addStretch(1)
