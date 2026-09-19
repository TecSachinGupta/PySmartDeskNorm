from PySide6.QtCore import Property, QEvent, QPoint, QRect, Qt
from PySide6.QtGui import QBrush, QColor, QPainter, QPixmap
from PySide6.QtWidgets import QPushButton

from .Tooltip import Tooltip

_VARIANT_TOKENS = {
    "primary": {
        "background": "primaryColor",
        "hover": "accentColor",
        "pressed": "contextHoverColor",
        "text": "textActiveColor",
    },
    "secondary": {
        "background": "surfaceColor",
        "hover": "accentColor",
        "pressed": "contextHoverColor",
        "text": "textPrimaryColor",
    },
    "ghost": {
        "background": None,
        "hover": "surfaceColor",
        "pressed": "accentColor",
        "text": "textPrimaryColor",
    },
    "danger": {
        "background": None,
        "hover": "errorColor",
        "pressed": "errorColor",
        "text": "textActiveColor",
    },
}

_VARIANT_FALLBACK_COLORS = {
    "primaryColor": "#568af2",
    "accentColor": "#6c99f4",
    "contextHoverColor": "#6c99f4",
    "surfaceColor": "#343b48",
    "textPrimaryColor": "#dce1ec",
    "textActiveColor": "#f5f6f9",
    "errorColor": "#ff5555",
}


def _resolve_variant_colors(variant: str, theme_colors: dict) -> dict:
    """Look up a button variant's colors from theme tokens, falling back to defaults."""
    tokens = _VARIANT_TOKENS.get(variant, _VARIANT_TOKENS["primary"])

    def lookup(key):
        token_name = tokens.get(key)
        if token_name is None:
            return ""
        return theme_colors.get(token_name) or _VARIANT_FALLBACK_COLORS.get(token_name, "")

    return {
        "background": lookup("background"),
        "backgroundHover": lookup("hover"),
        "backgroundPressed": lookup("pressed"),
        "text": lookup("text"),
    }


class Button(QPushButton):
    def __init__(
        self,
        name=None,
        parent=None,
        appParent=None,
        label=None,
        tooltipLabel=None,
        width=50,
        height=50,
        radius=8,
        variant=None,
        themeColors=None,
        textColor="",
        contextColor="",
        backgroundColor="",
        backgroundHoverColor="",
        backgroundPressedColor="",
        leftIconPath=None,
        rightIconPath=None,
        iconColor="",
        iconHoverColor="",
        iconPressedColor="",
        iconActiveColor="",
        margin=None,
        isActive=False,
        isTabActive=False,
        isToggleActive=False,
    ):
        super().__init__()
        if name is not None:
            self.setObjectName(name)
        if parent is not None:
            self.setParent(parent)

        if variant:
            resolved = _resolve_variant_colors(variant, themeColors or {})
            backgroundColor = backgroundColor or resolved["background"]
            backgroundHoverColor = backgroundHoverColor or resolved["backgroundHover"]
            backgroundPressedColor = backgroundPressedColor or resolved["backgroundPressed"]
            textColor = textColor or resolved["text"]

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
        self._margin = margin or {}
        self._isActive = isActive
        self._isTabActive = isTabActive
        self._isToggleActive = isToggleActive

        self._defaultBackgroundColor = backgroundColor
        self._defaultIconColor = iconColor
        self._defaultRadius = radius

        self._parent = appParent

        self.setText(label)
        self.setFixedSize(width, height)
        self.setCursor(Qt.PointingHandCursor)

        # Built lazily on first hover so buttons without tooltip text never spawn a window.
        self._tooltipLabel = tooltipLabel
        self._tooltip = None

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

    @isTabActive.setter
    def isTabActive(self, isTabActive):
        self._isTabActive = isTabActive
        self.update()

    @Property(bool)
    def isToggleActive(self):
        return self._isToggleActive

    @isToggleActive.setter
    def isToggleActive(self, isToggleActive):
        self._isToggleActive = isToggleActive
        self.update()

    def _ensure_tooltip(self):
        if self._tooltip is None and self._tooltipLabel:
            self._tooltip = Tooltip(
                parent=self._parent or self.window(),
                backgroundColor=self._backgroundHoverColor or "#343b48",
                textColor=self._textColor or "#f5f6f9",
                tooltipText=self._tooltipLabel,
            )
            self._tooltip.hide()
        return self._tooltip

    def moveTooltip(self):
        if self._tooltip is None:
            return
        reference = self._parent or self.window()
        if reference is None:
            return
        gp = self.mapToGlobal(QPoint(0, 0))
        pos = reference.mapFromGlobal(gp)

        pos_x = (pos.x() - (self._tooltip.width() // 2)) + (self.width() // 2)
        pos_y = pos.y() - self._margin.get("top", self._tooltip.height() + 6)

        self._tooltip.move(pos_x, pos_y)

    def paintIcon(self, qp, image, rect):
        icon = QPixmap(image)
        painter = QPainter(icon)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        if self._isActive:
            painter.fillRect(icon.rect(), self._iconActiveColor)
        else:
            painter.fillRect(icon.rect(), self._iconColor)
        qp.drawPixmap((rect.width() - icon.width()) / 2, (rect.height() - icon.height()) / 2, icon)
        painter.end()

    def paintEvent(self, event):
        # PAINTER
        p = QPainter()
        p.begin(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setPen(Qt.NoPen)
        p.setFont(self.font())

        rect = QRect(0, 0, self.width(), self.height())
        fill_color = self._backgroundPressedColor if self._isActive else self._backgroundColor

        if fill_color:
            p.setBrush(QBrush(QColor(fill_color)))
            p.drawRoundedRect(rect, self._defaultRadius, self._defaultRadius)

        icon_width = min(50, self.width())
        if self._leftIconPath:
            self.paintIcon(p, self._leftIconPath, QRect(0, 0, icon_width, self.height()))
        if self._rightIconPath:
            self.paintIcon(
                p,
                self._rightIconPath,
                QRect(self.width() - icon_width, 0, icon_width, self.height()),
            )

        if self._label:
            p.setPen(QColor(self._textColor or "#dce1ec"))
            p.drawText(rect, Qt.AlignCenter, self._label)

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
        if self._ensure_tooltip() is not None:
            self.moveTooltip()
            self._tooltip.show()

    def leaveEvent(self, event):
        self.changeStyle(QEvent.Leave)
        if self._tooltip is not None:
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
