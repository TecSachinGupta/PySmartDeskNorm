from __future__ import annotations

from PySide6.QtCore import QSettings

ORGANIZATION_NAME = "PySmartDeskNorm"
APPLICATION_NAME = "PySmartDeskNorm"

THEME_KEY = "appearance/theme"
CREDITS_BAR_KEY = "appearance/show_credits_bar"
CREDITS_MESSAGE_KEY = "appearance/credits_message"


class SettingsService:
    """Wraps QSettings so pages never touch persistence directly."""

    def __init__(self, settings: QSettings | None = None):
        self._settings = settings or QSettings(ORGANIZATION_NAME, APPLICATION_NAME)

    def get_theme(self, default: str = "default") -> str:
        return str(self._settings.value(THEME_KEY, default))

    def set_theme(self, theme_name: str) -> None:
        self._settings.setValue(THEME_KEY, theme_name)
        self._settings.sync()

    def get_show_credits_bar(self, default: bool = True) -> bool:
        value = self._settings.value(CREDITS_BAR_KEY, default)
        if isinstance(value, str):
            return value.lower() in ("1", "true", "yes")
        return bool(value)

    def set_show_credits_bar(self, enabled: bool) -> None:
        self._settings.setValue(CREDITS_BAR_KEY, enabled)
        self._settings.sync()

    def get_credits_message(self, default: str = "") -> str:
        return str(self._settings.value(CREDITS_MESSAGE_KEY, default))

    def set_credits_message(self, message: str) -> None:
        self._settings.setValue(CREDITS_MESSAGE_KEY, message)
        self._settings.sync()
