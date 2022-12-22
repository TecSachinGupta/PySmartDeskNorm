
from PySide6.QtCore import Property
from PySide6.QtWidgets import QFrame, QVBoxLayout

class Column(QFrame):
    def __init__(self, name = None, parent = None, widgets = []):
        super().__init__()
        if name is not None:
            self.setObjectName(name)
        if parent is not None:
            self.setParent(parent)
        
        layout = QVBoxLayout()

        self.content_widgets = widgets if self.content_widgets is None else self.content_widgets

        for content in self.content_widgets:
            layout.addWidget(content)

        self.setLayout(layout)
    
    @Property(list)
    def content_widgets(self):
        return self.content_widgets
    
    @content_widgets.setter
    def content_widgets(self, cw: list):
        self.content_widgets = cw
        self.update()
