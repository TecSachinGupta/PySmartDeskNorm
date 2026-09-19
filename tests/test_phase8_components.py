from PySide6.QtCore import QSettings

from controllers.settings_controller import SettingsController
from services.settings_service import SettingsService
from views.components.Button import _resolve_variant_colors
from views.components.ComboBox import ComboBox
from views.components.EmptyState import EmptyState
from views.components.TextInput import TextInput
from views.components.Toast import Toast
from views.containers.AppShell import AppShell
from views.pages.Tools import Tools
from views.widgets.CreditsBar import CreditsBar

THEME_COLORS = {
    "primaryColor": "#111111",
    "accentColor": "#222222",
    "contextHoverColor": "#333333",
    "surfaceColor": "#444444",
    "textPrimaryColor": "#555555",
    "textActiveColor": "#666666",
    "errorColor": "#777777",
}


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


def test_credits_bar_custom_message_toggles_visibility(qtbot):
    credits_bar = CreditsBar(copyright="Copyright", version="v1.0.0", settings={})
    qtbot.addWidget(credits_bar)
    credits_bar.show()

    assert credits_bar._custom_message_label.isVisible() is False

    credits_bar.set_custom_message("Hello there")
    assert credits_bar._custom_message_label.text() == "Hello there"
    assert credits_bar._custom_message_label.isVisible() is True

    credits_bar.set_custom_message("")
    assert credits_bar._custom_message_label.isVisible() is False


def test_combo_box_and_text_input_build(qtbot):
    combo = ComboBox(items=["Default", "Dracula"], current="Dracula")
    qtbot.addWidget(combo)
    assert combo.currentText() == "Dracula"

    text_input = TextInput(placeholder="Type here", text="hello")
    qtbot.addWidget(text_input)
    assert text_input.text() == "hello"
    assert text_input.placeholderText() == "Type here"


def test_toast_shows_and_schedules_hide(qtbot):
    toast = Toast(duration_ms=50)
    qtbot.addWidget(toast)

    toast.show_message("Saved")
    assert toast.text() == "Saved"
    assert toast.isVisible() is True

    qtbot.waitUntil(lambda: not toast.isVisible(), timeout=1000)


def test_empty_state_builds(qtbot):
    empty_state = EmptyState(title="Nothing", description="Try again")
    qtbot.addWidget(empty_state)
    assert empty_state.objectName() == "emptyState"


def test_tools_page_shows_empty_state_when_no_matches(qtbot):
    tools = Tools(settings={})
    qtbot.addWidget(tools)
    tools.show()

    tools.search_input.setText("does-not-exist")

    assert tools.empty_state.isVisible() is True
    assert tools.cards_row.isVisible() is False

    tools.search_input.setText("")
    assert tools.empty_state.isVisible() is False
    assert tools.cards_row.isVisible() is True


def test_settings_page_credits_message_flows_to_credits_bar(qtbot, tmp_path):
    ini_settings = QSettings(str(tmp_path / "settings.ini"), QSettings.IniFormat)
    controller = SettingsController(settings_service=SettingsService(settings=ini_settings))
    shell = AppShell(
        name="appshell", settings={"app_name": "PySmartDeskNorm"}, settings_controller=controller
    )
    qtbot.addWidget(shell)
    shell.show()

    settings_page = shell.navigation_service.widget_for("settings")
    settings_page.credits_message_input.setText("Made with love")

    assert shell.credits_bar._custom_message_label.text() == "Made with love"
    assert shell.credits_bar._custom_message_label.isVisible() is True
