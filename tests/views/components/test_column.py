from PySide6.QtWidgets import QWidget

from views.components.Column import Column


def test_column_constructs(qtbot):
    widget = Column(name="column", widgets=[QWidget()])
    qtbot.addWidget(widget)
    assert widget is not None
