from views.widgets.TitleBar import TitleBar


def test_title_bar_constructs(qtbot):
    widget = TitleBar(name="titlebar", parent=None, settings={"app_name": "PySmartDeskNorm"})
    qtbot.addWidget(widget)
    assert widget is not None
