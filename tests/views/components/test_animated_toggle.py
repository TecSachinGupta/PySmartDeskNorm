from views.components.AnimatedToggle import AnimatedToggle


def test_animated_toggle_constructs(qtbot):
    widget = AnimatedToggle()
    qtbot.addWidget(widget)
    assert widget is not None
