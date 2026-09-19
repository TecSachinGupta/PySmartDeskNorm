from PySide6.QtCore import QEvent

from views.components.Button import Button, _resolve_variant_colors

THEME_COLORS = {
    "primaryColor": "#111111",
    "accentColor": "#222222",
    "contextHoverColor": "#333333",
    "surfaceColor": "#444444",
    "textPrimaryColor": "#555555",
    "textActiveColor": "#666666",
    "errorColor": "#777777",
}


def test_button_constructs(qtbot):
    widget = Button(name="button", label="Test", tooltipLabel="Test tooltip")
    qtbot.addWidget(widget)
    assert widget is not None


def test_resolve_variant_colors_reads_theme_tokens():
    primary = _resolve_variant_colors("primary", THEME_COLORS)
    assert primary["background"] == "#111111"
    assert primary["text"] == "#666666"

    ghost = _resolve_variant_colors("ghost", THEME_COLORS)
    assert ghost["background"] == ""  # transparent until hovered/pressed
    assert ghost["backgroundHover"] == "#444444"

    danger = _resolve_variant_colors("danger", THEME_COLORS)
    assert danger["background"] == ""
    assert danger["backgroundHover"] == "#777777"


def test_resolve_variant_colors_falls_back_without_theme():
    resolved = _resolve_variant_colors("primary", {})
    assert resolved["background"] == "#568af2"
    assert resolved["text"] == "#f5f6f9"


def test_button_variant_is_actually_applied_to_instance(qtbot):
    """The variant kwarg must reach the instance, not just the helper."""
    button = Button(name="b", label="Go", variant="primary", themeColors=THEME_COLORS)
    qtbot.addWidget(button)

    assert button._backgroundColor == THEME_COLORS["primaryColor"]
    assert button._backgroundHoverColor == THEME_COLORS["accentColor"]
    assert button._textColor == THEME_COLORS["textActiveColor"]

    danger = Button(name="d", label="X", variant="danger", themeColors=THEME_COLORS)
    qtbot.addWidget(danger)
    assert danger._backgroundHoverColor == THEME_COLORS["errorColor"]


def test_button_without_tooltip_label_never_creates_a_tooltip(qtbot):
    """A tooltip-less button must not spawn a stray floating window on hover."""
    button = Button(name="noTip", label="—")
    qtbot.addWidget(button)
    button.show()

    assert button._tooltip is None

    button.enterEvent(QEvent(QEvent.Enter))
    assert button._tooltip is None

    button.leaveEvent(QEvent(QEvent.Leave))
    assert button._tooltip is None


def test_button_with_tooltip_label_builds_tooltip_parented_to_window(qtbot):
    button = Button(name="tip", label="Go", tooltipLabel="Helpful text")
    qtbot.addWidget(button)
    button.show()

    button.enterEvent(QEvent(QEvent.Enter))

    assert button._tooltip is not None
    assert button._tooltip.text() == "Helpful text"
    # Parented to a real widget, so it is not a stray top-level window.
    assert button._tooltip.parent() is not None
