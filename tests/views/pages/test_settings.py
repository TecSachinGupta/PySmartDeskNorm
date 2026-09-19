from constants import PAGE_ID_SETTINGS
from views.pages.Settings import Settings as SettingsPage


def test_page_constructs_without_error(qtbot, sample_settings, ini_controller):
    controller, _ = ini_controller()
    page = SettingsPage(settings=sample_settings, controller=controller)
    qtbot.addWidget(page)
    assert page.page_id == PAGE_ID_SETTINGS


def test_settings_page_switches_theme_and_emits_credits_bar_signal(qtbot, ini_controller):
    controller, _ = ini_controller()
    page = SettingsPage(settings={"app_name": "PySmartDeskNorm"}, controller=controller)
    qtbot.addWidget(page)

    received = []
    page.credits_bar_visibility_changed.connect(received.append)

    page.theme_combo.setCurrentText("Dracula")
    assert controller.current_theme() == "dracula"

    page.credits_bar_toggle.setChecked(not page.credits_bar_toggle.isChecked())
    assert received
