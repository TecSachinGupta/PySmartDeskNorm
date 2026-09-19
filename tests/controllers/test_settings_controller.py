from __future__ import annotations

from PySide6.QtCore import QSettings

from controllers.settings_controller import SettingsController
from services.settings_service import SettingsService


def test_settings_persist_across_service_restarts(ini_controller):
    controller, ini_path = ini_controller()
    controller.select_theme("dracula")
    controller.set_credits_bar_visible(False)

    # simulate an app restart: a brand-new service/controller against the same store
    restarted_qsettings = QSettings(str(ini_path), QSettings.IniFormat)
    restarted_controller = SettingsController(
        settings_service=SettingsService(settings=restarted_qsettings)
    )

    assert restarted_controller.current_theme() == "dracula"
    assert restarted_controller.credits_bar_visible() is False


def test_settings_controller_lists_available_themes(ini_controller):
    controller, _ = ini_controller()
    themes = controller.available_themes()

    assert themes == sorted(themes)
    assert {"default", "bright", "dracula"}.issubset(set(themes))
