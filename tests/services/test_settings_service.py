from __future__ import annotations

from PySide6.QtCore import QSettings

from services.settings_service import SettingsService


def test_settings_service_roundtrips_theme_credits_and_message(tmp_path):
    ini_path = tmp_path / "settings.ini"
    service = SettingsService(settings=QSettings(str(ini_path), QSettings.IniFormat))

    service.set_theme("dracula")
    service.set_show_credits_bar(False)
    service.set_credits_message("Hello")

    # Re-open the same store to confirm persistence independent of this instance.
    reopened = SettingsService(settings=QSettings(str(ini_path), QSettings.IniFormat))
    assert reopened.get_theme() == "dracula"
    assert reopened.get_show_credits_bar() is False
    assert reopened.get_credits_message() == "Hello"


def test_settings_service_defaults_when_nothing_persisted(tmp_path):
    ini_path = tmp_path / "empty.ini"
    service = SettingsService(settings=QSettings(str(ini_path), QSettings.IniFormat))

    assert service.get_theme(default="default") == "default"
    assert service.get_show_credits_bar(default=True) is True
    assert service.get_credits_message(default="") == ""
