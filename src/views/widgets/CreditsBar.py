
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QWidget, QSizePolicy, QSpacerItem

class CreditsBar(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
        if kwargs.get("name") is not None:
            self.setObjectName(kwargs.get("name"))
        
        self.setParent(kwargs.get("parent"))
        self.settings = kwargs.get("settings")
        
        custom_message = QLabel(kwargs.get("customMessage"))
        copyright = QLabel(args[0])
        version = QLabel(args[1])

        custom_message.setAlignment(Qt.AlignVCenter)
        copyright.setAlignment(Qt.AlignVCenter)
        version.setAlignment(Qt.AlignVCenter)

        hSpacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.frameLayout = QHBoxLayout()
        if kwargs.get("customMessage") is not None:
            self.frameLayout.addWidget(custom_message)
        
        self.frameLayout.addWidget(copyright)
        self.frameLayout.addSpacerItem(hSpacer)
        self.frameLayout.addWidget(version)

    def render(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        # BG STYLE
        style = f"""
            #creditsBarFrame {{
                border-radius: {self._radius}px;
                background-color: {self._bg_two};
            }}
            .QLabel {{
                font: {self._text_size}pt "{self._font_family}";
                color: {self._text_description_color};
                padding-left: {self._padding}px;
                padding-right: {self._padding}px;
            }}
        """

        frame = QFrame()
        frame.setObjectName("creditsBarFrame")
        

        
