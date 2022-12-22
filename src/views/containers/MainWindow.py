
from PySide6.QtWidgets import QMainWindow

from configs import Settings, Themes

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = {**Settings().items, **Themes().items}
        
        self.render()

    def render(self):
        print(self.settings)