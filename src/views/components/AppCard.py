from __future__ import annotations

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout

from utils.resource import icon as icon_path
from views.components.Button import Button

GENERIC_ICON = "component"


class AppCard(QFrame):
    open_requested = Signal(str)
    remove_requested = Signal(str)

    def __init__(
        self,
        name=None,
        parent=None,
        app_id="",
        title="",
        icon=None,
        meta="",
        icon_size=28,
        themeColors=None,
    ):
        super().__init__(parent)
        self.setObjectName(name or "appCard")
        self.app_id = app_id
        self.title_text = title

        colors = themeColors or {}

        self.icon_label = QLabel()
        self.icon_label.setObjectName("appCardIcon")
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setFixedSize(icon_size + 8, icon_size + 8)
        self.icon_label.setPixmap(self._load_pixmap(icon, icon_size))

        self.title_label = QLabel(title)
        self.title_label.setObjectName("appCardTitle")

        self.meta_label = QLabel(meta)
        self.meta_label.setObjectName("appCardMeta")

        self.open_button = Button(
            name="appCardOpenButton",
            label="Open",
            tooltipLabel=f"Open {title}" if title else "Open",
            width=64,
            height=26,
            radius=6,
            variant="secondary",
            themeColors=colors,
        )
        self.remove_button = Button(
            name="appCardRemoveButton",
            label="\u2715",
            tooltipLabel=f"Stop tracking {title}" if title else "Stop tracking",
            width=26,
            height=26,
            radius=13,
            variant="ghost",
            themeColors=colors,
        )

        self.open_button.clicked.connect(lambda: self.open_requested.emit(self.app_id))
        self.remove_button.clicked.connect(lambda: self.remove_requested.emit(self.app_id))

        text_column = QVBoxLayout()
        text_column.setContentsMargins(0, 0, 0, 0)
        text_column.setSpacing(2)
        text_column.addWidget(self.title_label)
        text_column.addWidget(self.meta_label)

        top_row = QHBoxLayout()
        top_row.setContentsMargins(0, 0, 0, 0)
        top_row.setSpacing(10)
        top_row.addWidget(self.icon_label)
        top_row.addLayout(text_column, 1)
        top_row.addWidget(self.remove_button, 0, Qt.AlignTop)

        actions_row = QHBoxLayout()
        actions_row.setContentsMargins(0, 0, 0, 0)
        actions_row.addStretch(1)
        actions_row.addWidget(self.open_button)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(10)
        layout.addLayout(top_row)
        layout.addLayout(actions_row)

    def _load_pixmap(self, icon: str | None, size: int):
        path = icon_path(icon) if icon else None
        if path is None or not path.is_file():
            path = icon_path(GENERIC_ICON)
        return QIcon(str(path)).pixmap(QSize(size, size))
