
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QLabel, QGraphicsDropShadowEffect

class Tooltip(QLabel):
    style = """
                QLabel {{		
                    background-color: {backgroundColor};	
                    color: {textColor};
                    padding-left: 10px;
                    padding-right: 10px;
                    border-radius: 17px;
                    border: 0px solid transparent;
                    font: 800 9pt "Segoe UI";
                }}
            """
    def __init__(self,
                 name = None,
                 parent = None,
                 backgroundColor = None,
                 textColor = None,
                 toottipText = None 
                ):
        super().__init__()
        if name is not None:
            self.setObjectName(name)
        else:
            self.setObjectName(u"label_tooltip")
        if parent is not None:
            self.setParent(parent)
        
        style = self.style.format(
            backgroundColor = backgroundColor,
            textColor = textColor
        )
        self.setStyleSheet(style)
        self.setMinimumHeight(34)
        self.setText(toottipText)
        self.adjustSize()

        # SET DROP SHADOW
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(30)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(self.shadow)