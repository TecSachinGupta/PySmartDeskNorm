from PySide6.QtCore import Property
from PySide6.QtWidgets import QFrame, QHBoxLayout


class Row(QFrame):
    def __init__(self, name=None, parent=None, widgets=None):
        super().__init__()
        if name is not None:
            self.setObjectName(name)
        if parent is not None:
            self.setParent(parent)

        self._content_widgets = [] if widgets is None else list(widgets)
        layout = QHBoxLayout()

        for content in self._content_widgets:
            layout.addWidget(content)

        self.setLayout(layout)

    @Property(list)
    def content_widgets(self):
        return self._content_widgets

    @content_widgets.setter
    def content_widgets(self, cw: list):
        self._content_widgets = list(cw) if cw is not None else []
        layout = self.layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
        for content in self._content_widgets:
            layout.addWidget(content)
        self.update()
