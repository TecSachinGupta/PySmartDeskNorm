from typing import Self

from PySide6.QtWidgets import QFrame, QLayout

class Div(QFrame):
    def __init__(self: Self, content: QLayout, **kwargs):
        super().__init__()
        self.setLayout(content)

        if kwargs.get("name") is not None:
            self.setObjectName(kwargs.get("name"))
        if kwargs.get("parent") is not None:
            self.setParent(kwargs.get("parent"))
        if kwargs.get("color") is not None:
            self.setStyleSheet("background: {color};".format(color=kwargs.get("color")))
        
        self.setLayout(content)