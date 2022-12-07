
from PySide6.QtWidgets import QFrame, QVBoxLayout

class Column(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__()
        if kwargs.get("name") is not None:
            self.setObjectName(kwargs.get("name"))
        if kwargs.get("parent") is not None:
            self.setParent(kwargs.get("parent"))
        
        layout = QVBoxLayout()

        for content in args:
            layout.addWidget(content)

        self.setLayout(layout)

