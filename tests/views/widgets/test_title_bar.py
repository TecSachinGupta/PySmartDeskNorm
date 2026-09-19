from views.widgets.TitleBar import TitleBar


def test_title_bar_constructs(qtbot):
    widget = TitleBar(name="titlebar", parent=None, settings={"app_name": "PySmartDeskNorm"})
    qtbot.addWidget(widget)
    assert widget is not None


def test_window_controls_are_circular_and_theme_sized(qtbot):
    """Square buttons with a half-side radius are what render as circles."""
    settings = {
        "app_name": "PySmartDeskNorm",
        "controls": {"window_control_size": 30},
        "colors": {"surfaceColor": "#343b48", "errorColor": "#ff5555"},
    }
    bar = TitleBar(name="titlebar", settings=settings)
    qtbot.addWidget(bar)

    for button in (bar.minimize_button, bar.maximize_button, bar.close_button):
        assert button.width() == button.height() == 30
        assert button._defaultRadius * 2 == button.width()
        # A resting background is required, or the control renders as a bare glyph.
        assert button._backgroundColor != ""

    assert bar.close_button._backgroundColor == "#ff5555"
