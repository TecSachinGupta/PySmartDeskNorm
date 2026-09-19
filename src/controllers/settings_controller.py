from __future__ import annotations

from PySide6.QtWidgets import QApplication

from configs.Themes import Themes
from services.settings_service import SettingsService
from utils.resource import resource_path


class SettingsController:
    """Mediates between the Settings page's widgets and settings_service."""

    def __init__(self, settings_service: SettingsService | None = None):
        self.settings_service = settings_service or SettingsService()

    def available_themes(self) -> list[str]:
        themes_dir = resource_path("themes")
        return sorted(path.stem for path in themes_dir.glob("*.json"))

    def current_theme(self) -> str:
        return self.settings_service.get_theme()

    def select_theme(self, theme_name: str) -> None:
        self.settings_service.set_theme(theme_name)
        app = QApplication.instance()
        if app is not None:
            Themes(theme=theme_name).apply(app)

    def credits_bar_visible(self) -> bool:
        return self.settings_service.get_show_credits_bar()

    def set_credits_bar_visible(self, visible: bool) -> None:
        self.settings_service.set_show_credits_bar(visible)

    def credits_message(self) -> str:
        return self.settings_service.get_credits_message()

    def set_credits_message(self, message: str) -> None:
        self.settings_service.set_credits_message(message)
