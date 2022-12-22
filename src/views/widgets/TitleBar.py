
from PySide6.QtWidgets import QWidget

class TitleBar(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__()
        if kwargs.get("name") is not None:
            self.setObjectName(kwargs.get("name"))
        
        self.setParent(kwargs.get("parent"))
        self.settings = kwargs.get("settings")
        
        pass