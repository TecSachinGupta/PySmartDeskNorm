from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QStackedWidget, QVBoxLayout, QWidget

from constants import (
    PAGE_ID_ABOUT,
    PAGE_ID_APPLICATIONS,
    PAGE_ID_DASHBOARD,
    PAGE_ID_SETTINGS,
    PAGE_ID_TOOLS,
)
from services.navigation_service import NavigationService
from views.pages.About import About
from views.pages.Applications import Applications
from views.pages.Dashboard import Dashboard
from views.pages.Settings import Settings as SettingsPage
from views.pages.Tools import Tools
from views.widgets.CreditsBar import CreditsBar
from views.widgets.Sidebar import Sidebar
from views.widgets.TitleBar import TitleBar


class AppShell(QWidget):
    def __init__(self, name=None, parent=None, settings=None, settings_controller=None):
        super().__init__(parent)
        self.setObjectName(name or "appshell")
        self.settings = settings or {}
        self._settings_controller = settings_controller

        self.title_bar = TitleBar(name="titleBar", parent=self, settings=self.settings)
        self.sidebar = Sidebar(name="sidebar", parent=self, settings=self.settings)
        self.stacked_widget = QStackedWidget(self)
        self.credits_bar = CreditsBar(
            copyright=self.settings.get("copyright", ""),
            version=str(self.settings.get("version", "")),
            name="creditsBar",
            parent=self,
            settings=self.settings,
        )
        self.navigation_service = NavigationService(self)

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)
        outer_layout.addWidget(self.title_bar)

        body_layout = QHBoxLayout()
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)
        body_layout.addWidget(self.sidebar)
        body_layout.addWidget(self.stacked_widget, 1)
        outer_layout.addLayout(body_layout)
        outer_layout.addWidget(self.credits_bar)

        self._register_pages()
        self.navigation_service.page_changed.connect(self._show_page)
        self.navigation_service.page_changed.connect(self.sidebar.set_active_page)

        for item in self.sidebar.items:
            item.clicked.connect(self.navigation_service.navigate)

        self.navigation_service.navigate(PAGE_ID_DASHBOARD)

    def _register_pages(self):
        settings_page = SettingsPage(
            name="settingsPage", settings=self.settings, controller=self._settings_controller
        )
        settings_page.credits_bar_visibility_changed.connect(self.credits_bar.setVisible)
        settings_page.credits_message_changed.connect(self.credits_bar.set_custom_message)
        self.credits_bar.setVisible(settings_page.controller.credits_bar_visible())
        self.credits_bar.set_custom_message(settings_page.controller.credits_message())

        pages = [
            (PAGE_ID_DASHBOARD, Dashboard(name="dashboardPage", settings=self.settings)),
            (PAGE_ID_APPLICATIONS, Applications(name="applicationsPage", settings=self.settings)),
            (PAGE_ID_TOOLS, Tools(name="toolsPage", settings=self.settings)),
            (PAGE_ID_SETTINGS, settings_page),
            (PAGE_ID_ABOUT, About(name="aboutPage", settings=self.settings)),
        ]
        for page_id, widget in pages:
            self.stacked_widget.addWidget(widget)
            self.navigation_service.register_page(page_id, widget)

    def _show_page(self, page_id: str):
        widget = self.navigation_service.widget_for(page_id)
        if widget is not None:
            self.stacked_widget.setCurrentWidget(widget)
