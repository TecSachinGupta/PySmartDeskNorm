from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget

from views.components.Button import Button
from views.components.Row import Row


class TitleBar(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.settings = kwargs.get("settings") or {}
        if kwargs.get("name") is not None:
            self.setObjectName(kwargs.get("name"))
        if kwargs.get("parent") is not None:
            self.setParent(kwargs.get("parent"))

        self.title_label = QLabel(self.settings.get("app_name", "App"))
        self.title_label.setObjectName("titleLabel")
        self.title_label.setStyleSheet("color: #dce1ec; font-weight: 700;")

        self._build_window_controls()
        self._build_layout()

    def _build_window_controls(self):
        colors = self.settings.get("colors", {})
        self.minimize_button = Button(
            name="minimizeButton",
            label="—",
            width=32,
            height=24,
            variant="ghost",
            themeColors=colors,
        )
        self.maximize_button = Button(
            name="maximizeButton",
            label="□",
            width=32,
            height=24,
            variant="ghost",
            themeColors=colors,
        )
        self.close_button = Button(
            name="closeButton", label="✕", width=32, height=24, variant="danger", themeColors=colors
        )

    def _build_layout(self):
        row = Row(
            name="titleBarRow",
            widgets=[
                self.title_label,
                self.minimize_button,
                self.maximize_button,
                self.close_button,
            ],
        )
        row.setStyleSheet("QWidget#titleBarRow { background: #21252d; border: none; }")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(8)
        layout.addWidget(row)

        self.setFixedHeight(48)

        self.minimize_button.clicked.connect(lambda: self.window().showMinimized())
        self.maximize_button.clicked.connect(self._toggle_maximize)
        self.close_button.clicked.connect(lambda: self.window().close())

    def _toggle_maximize(self):
        window = self.window()
        if window.isMaximized():
            window.showNormal()
        else:
            window.showMaximized()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            window_handle = self.window().windowHandle()
            if window_handle is not None:
                window_handle.startSystemMove()
        super().mousePressEvent(event)
