import os

from PySide6.QtCore import Property, QEvent, QPoint, QRect, Qt
from PySide6.QtGui import QBrush, QColor, QPainter, QPixmap
from PySide6.QtWidgets import QPushButton

from .Tooltip import Tooltip

class Button(QPushButton):
    def __init__(self,
                 name = None,
                 parent = None,
                 appParent = None,
                 label = None,
                 tooltipLabel = None,
                 width = 50,
                 height = 50,
                 radius = 8,
                 textColor = '',
                 contextColor = '',
                 backgroundColor = '',
                 backgroundHoverColor = '',
                 backgroundPressedColor = '',
                 leftIconPath = None,
                 rightIconPath = None,
                 iconColor = '',
                 iconHoverColor = '',
                 iconPressedColor = '',
                 iconActiveColor = '',
                 margin = {},
                 isActive = False,
                 isTabActive = False,
                 isToggleActive= False
                ):
        super().__init__()
        if name is not None:
            self.setObjectName(name)
        if parent is not None:
            self.setParent(parent)
        
        self._label = label
        self._textColor = textColor
        self._contextColor = contextColor
        self._backgroundColor = backgroundColor
        self._backgroundHoverColor = backgroundHoverColor
        self._backgroundPressedColor = backgroundPressedColor
        self._leftIconPath = leftIconPath
        self._rightIconPath = rightIconPath
        self._iconColor = iconColor
        self._iconHoverColor = iconHoverColor
        self._iconPressedColor = iconPressedColor
        self._iconActiveColor = iconActiveColor
        self._margin = margin
        self._isActive = isActive
        self._isTabActive = isTabActive
        self._isToggleActive = isToggleActive

        self._defaultBackgroundColor = backgroundColor
        self._defaultIconColor = iconColor
        self._defaultRadius = radius

        self.setText(label)
        self.setFixedSize(width, height)
        self.setCursor(Qt.PointingHandCursor)

        self._tooltip = Tooltip(
                                parent = appParent,
                                backgroundColor = backgroundColor,
                                textColor = textColor,
                                tooltipText = tooltipLabel
                               )
        self._tooltip.hide()
    
    @Property(bool)
    def isActive(self):
        return self._isActive
    
    @isActive.setter
    def isActive(self, isActive):
        self._isActive = isActive
        self.update()
    
    @Property(bool)
    def isTabActive(self):
        return self._isTabActive
    
    @isActive.setter
    def isTabActive(self, isTabActive):
        self._isTabActive = isTabActive
        self.update()

    @Property(bool)
    def isToggleActive(self):
        return self._isToggleActive
    
    @isActive.setter
    def isToggleActive(self, isToggleActive):
        self._isToggleActive = isToggleActive
        self.update()

    def moveTooltip(self):
        # GET MAIN WINDOW PARENT
        gp = self.mapToGlobal(QPoint(0, 0))

        # SET WIDGET TO GET POSTION
        # Return absolute position of widget inside app
        pos = self._parent.mapFromGlobal(gp)

        # FORMAT POSITION
        # Adjust tooltip position with offset
        pos_x = (pos.x() - (self._tooltip.width() // 2)) + (self.width() // 2)
        pos_y = pos.y() - self._margin["top"]

        # SET POSITION TO WIDGET
        # Move tooltip position
        self._tooltip.move(pos_x, pos_y)
    
    def paintIcon(self, qp, image, rect):
        icon = QPixmap(image)
        painter = QPainter(icon)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        if self._isActive:
            painter.fillRect(icon.rect(), self._iconActiveColor)
        else:
            painter.fillRect(icon.rect(), self._iconColor)
        qp.drawPixmap(
            (rect.width() - icon.width()) / 2, 
            (rect.height() - icon.height()) / 2,
            icon
        )        
        painter.end()
    
    def paintEvent(self, event):
        # PAINTER
        p = QPainter()
        p.begin(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.NoPen)
        p.setFont(self.font())

        # RECTANGLES
        rect = QRect(4, 5, self.width(), self.height() - 10)
        rect_inside = QRect(4, 5, self.width() - 8, self.height() - 10)
        rect_left_icon = QRect(0, 0, 50, self.height())
        rect_right_icon = QRect(0, 0, 50, self.height())
        rect_blue = QRect(4, 5, 20, self.height() - 10)
        rect_inside_active = QRect(7, 5, self.width(), self.height() - 10)
        rect_text = QRect(45, 0, self.width() - 50, self.height())
        # code to create the button component
        
        p.end()

    
    def changeStyle(self, event):
        if not self._isActive:
            if event == QEvent.Enter:
                self._backgroundColor = self._backgroundHoverColor
                self._iconColor = self._iconHoverColor        
            elif event == QEvent.Leave:
                self._backgroundColor = self._defaultBackgroundColor
                self._iconColor = self._defaultIconColor
            elif event == QEvent.MouseButtonPress:            
                self._backgroundColor = self._backgroundPressedColor
                self._iconColor = self._iconPressedColor
            elif event == QEvent.MouseButtonRelease:
                self._backgroundColor = self._backgroundHoverColor
                self._iconColor = self._iconHoverColor
        self.repaint()
    
    def enterEvent(self, event):
        self.changeStyle(QEvent.Enter)
        self.moveTooltip()
        self._tooltip.show()
    
    def leaveEvent(self, event):
        self.changeStyle(QEvent.Leave)
        self.moveTooltip()
        self._tooltip.hide()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.changeStyle(QEvent.MouseButtonPress)
            # SET FOCUS
            self.setFocus()
            # EMIT SIGNAL
            return self.clicked.emit()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.changeStyle(QEvent.MouseButtonRelease)
            # EMIT SIGNAL
            return self.released.emit()
