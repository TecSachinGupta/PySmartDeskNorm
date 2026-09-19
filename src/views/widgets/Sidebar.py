from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QLabel, QSizePolicy, QVBoxLayout, QWidget

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
        # Plain QWidget subclasses ignore QSS backgrounds without this.
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(66)

        self.icon_label.setObjectName("sidebarItemIcon")
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.label.setObjectName("sidebarItemLabel")
        self.label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(2)
        layout.addWidget(self.icon_label)
        layout.addWidget(self.label)

        if self.badge_label is not None:
            self.badge_label.setObjectName("sidebarItemBadge")
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
    WIDTH = 136
    TOP_PAGE_IDS = (PAGE_ID_DASHBOARD, PAGE_ID_APPLICATIONS, PAGE_ID_TOOLS)
    BOTTOM_PAGE_IDS = (PAGE_ID_SETTINGS, PAGE_ID_ABOUT)

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
        self.setObjectName("sidebar")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedWidth(self.WIDTH)

        self.top_items = [i for i in self.items if i.page_id in self.TOP_PAGE_IDS]
        self.bottom_items = [i for i in self.items if i.page_id in self.BOTTOM_PAGE_IDS]

        top_group = Column(name="sidebarTopGroup", widgets=self.top_items)
        top_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        bottom_group = Column(name="sidebarBottomGroup", widgets=self.bottom_items)
        bottom_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 12, 10, 12)
        layout.setSpacing(8)
        layout.addWidget(top_group)
        # Flexible spacer keeps the bottom group flush to the sidebar's bottom edge.
        layout.addStretch(1)
        layout.addWidget(bottom_group)

    def set_active_page(self, page_id: str) -> None:
        for item in self.items:
            item.active = item.page_id == page_id
            item._apply_state()
