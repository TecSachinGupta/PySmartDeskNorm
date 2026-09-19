from views.components.Tooltip import Tooltip


def test_tooltip_constructs(qtbot):
    widget = Tooltip(
        name="tooltip",
        parent=None,
        backgroundColor="#000000",
        textColor="#ffffff",
        tooltipText="Hello",
    )
    qtbot.addWidget(widget)
    assert widget is not None
