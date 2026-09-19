from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QSpacerItem, QWidget


class CreditsBar(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
        if kwargs.get("name") is not None:
            self.setObjectName(kwargs.get("name"))

        if kwargs.get("parent") is not None:
            self.setParent(kwargs.get("parent"))
        self.settings = kwargs.get("settings")

        self._radius = 8
        self._bg_two = "#343b48"
        self._text_size = 9
        self._font_family = "Segoe UI"
        self._text_description_color = "#8a95aa"
        self._padding = 10

        self._custom_message_label = QLabel(kwargs.get("customMessage") or "")
        self._custom_message_label.setAlignment(Qt.AlignVCenter)
        self._custom_message_label.setVisible(bool(kwargs.get("customMessage")))

        copyright = QLabel(args[0] if args else kwargs.get("copyright", ""))
        version = QLabel(args[1] if len(args) > 1 else kwargs.get("version", ""))

        copyright.setAlignment(Qt.AlignVCenter)
        version.setAlignment(Qt.AlignVCenter)

        spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.frameLayout = QHBoxLayout(self)
        self.frameLayout.setContentsMargins(8, 4, 8, 4)
        self.setLayout(self.frameLayout)

        self.frameLayout.addWidget(self._custom_message_label)
        self.frameLayout.addWidget(copyright)
        self.frameLayout.addSpacerItem(spacer)
        self.frameLayout.addWidget(version)

    def render(self):
        return self.frameLayout

    def set_custom_message(self, message: str) -> None:
        self._custom_message_label.setText(message or "")
        self._custom_message_label.setVisible(bool(message))
