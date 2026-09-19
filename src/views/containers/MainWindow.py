from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow

from configs import Settings, Themes
from services.settings_service import SettingsService
from views.containers.AppShell import AppShell


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        base_settings = Settings().items
        theme_name = SettingsService().get_theme(default=base_settings.get("theme", "default"))
        self.settings = {**base_settings, **Themes(theme=theme_name).items}
        self.setWindowTitle(self.settings.get("app_name", "App"))
        if self.settings.get("custom_title_bar", False):
            self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setMinimumSize(
            self.settings.get("size", {}).get("minimum", {}).get("width", 800),
            self.settings.get("size", {}).get("minimum", {}).get("height", 600),
        )
        self.resize(
            self.settings.get("size", {}).get("preferred", {}).get("width", 1024),
            self.settings.get("size", {}).get("preferred", {}).get("height", 768),
        )
        self.render()

    def render(self):
        shell = AppShell(name="appShell", settings=self.settings)
        self.setCentralWidget(shell)
