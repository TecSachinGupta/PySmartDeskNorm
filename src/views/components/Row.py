
from PySide6.QtWidgets import QFrame, QHBoxLayout

class Row(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__()
        if kwargs.get("name") is not None:
            self.setObjectName(kwargs.get("name"))
        if kwargs.get("parent") is not None:
            self.setParent(kwargs.get("parent"))
        
        layout = QHBoxLayout()

        for content in args:
            layout.addWidget(content)

        self.setLayout(layout)