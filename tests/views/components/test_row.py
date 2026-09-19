from PySide6.QtWidgets import QWidget

from views.components.Row import Row


def test_row_constructs(qtbot):
    widget = Row(name="row", widgets=[QWidget()])
    qtbot.addWidget(widget)
    assert widget is not None
