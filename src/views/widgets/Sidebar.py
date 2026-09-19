from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from constants import (
    PAGE_ID_ABOUT,
    PAGE_ID_APPLICATIONS,
    PAGE_ID_DASHBOARD,
    PAGE_ID_SETTINGS,
    PAGE_ID_TOOLS,
)
from views.components.Column import Column


class SidebarItem(QWidget):
    clicked = Signal(str)

    def __init__(
        self,
        page_id: str,
        label: str,
        icon_text: str = "•",
        active: bool = False,
        badge: str | None = None,
        parent=None,
    ):
        super().__init__(parent)
        self.page_id = page_id
        self.active = active
        self.icon_label = QLabel(icon_text)
        self.label = QLabel(label)
        self.badge_label = QLabel(badge) if badge else None
        self._build_ui()

    def _build_ui(self):
        self.setObjectName("sidebarItem")
        self.setCursor(Qt.PointingHandCursor)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(4)

        icon_row = QWidget()
        icon_layout = QVBoxLayout(icon_row)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.addWidget(self.icon_label, 0, Qt.AlignCenter)
        self.icon_label.setAlignment(Qt.AlignCenter)

        text_widget = QWidget()
        text_layout = QVBoxLayout(text_widget)
        text_layout.setContentsMargins(0, 0, 0, 0)
        self.label.setAlignment(Qt.AlignCenter)
        text_layout.addWidget(self.label)

        layout.addWidget(icon_row)
        layout.addWidget(text_widget)

        if self.badge_label is not None:
            self.badge_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(self.badge_label)

        self._apply_state()

    def _apply_state(self):
        # Styling comes from the applied theme's QSS via this dynamic property.
        self.setProperty("active", self.active)
        self.style().unpolish(self)
        self.style().polish(self)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.page_id)
        super().mousePressEvent(event)


class Sidebar(QWidget):
    def __init__(self, name=None, parent=None, settings=None):
        super().__init__(parent)
        if name is not None:
            self.setObjectName(name)
        self.settings = settings or {}
        self.items = [
            SidebarItem(PAGE_ID_DASHBOARD, "Dashboard", icon_text="⌂", active=True),
            SidebarItem(PAGE_ID_APPLICATIONS, "Apps", icon_text="▣"),
            SidebarItem(PAGE_ID_TOOLS, "Tools", icon_text="⌕"),
            SidebarItem(PAGE_ID_SETTINGS, "Settings", icon_text="⚙"),
            SidebarItem(PAGE_ID_ABOUT, "About", icon_text="i"),
        ]
        self._build_ui()

    def _build_ui(self):
        self.setMinimumWidth(120)
        self.setObjectName("sidebar")
        column = Column(name="sidebarColumn", widgets=self.items)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        layout.addWidget(column)

    def set_active_page(self, page_id: str) -> None:
        for item in self.items:
            item.active = item.page_id == page_id
            item._apply_state()
