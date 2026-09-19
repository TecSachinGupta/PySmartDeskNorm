from __future__ import annotations

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QHBoxLayout, QLabel, QStackedWidget, QVBoxLayout, QWidget

from constants import (
    PAGE_ID_ABOUT,
    PAGE_ID_APPLICATIONS,
    PAGE_ID_DASHBOARD,
    PAGE_ID_SETTINGS,
    PAGE_ID_TOOLS,
)
from services.application_service import ApplicationService
from services.navigation_service import NavigationService
from utils.resource import icon
from views.pages.About import About
from views.pages.Applications import Applications
from views.pages.Dashboard import Dashboard
from views.pages.Settings import Settings as SettingsPage
from views.pages.Tools import Tools
from views.widgets.CreditsBar import CreditsBar
from views.widgets.Sidebar import Sidebar
from views.widgets.TitleBar import TitleBar


class AppShell(QWidget):
    def __init__(
        self,
        name=None,
        parent=None,
        settings=None,
        settings_controller=None,
        application_service=None,
    ):
        super().__init__(parent)
        self.setObjectName(name or "appshell")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.settings = settings or {}
        self._settings_controller = settings_controller
        self.application_service = application_service or ApplicationService(self)

        self.title_bar = TitleBar(name="titleBar", parent=self, settings=self.settings)
        self.sidebar = Sidebar(name="sidebar", parent=self, settings=self.settings)
        self.logo_slot = self._build_logo_slot()
        self.stacked_widget = QStackedWidget(self)
        self.credits_bar = CreditsBar(
            copyright=self._copyright_text(),
            version=str(self.settings.get("version", "")),
            name="creditsBar",
            parent=self,
            settings=self.settings,
        )
        self.navigation_service = NavigationService(self)

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        top_band = QHBoxLayout()
        top_band.setContentsMargins(0, 0, 0, 0)
        top_band.setSpacing(0)
        top_band.addWidget(self.logo_slot)
        top_band.addWidget(self.title_bar, 1)
        outer_layout.addLayout(top_band)

        content_column = QVBoxLayout()
        content_column.setContentsMargins(0, 0, 0, 0)
        content_column.setSpacing(0)
        content_column.addWidget(self.stacked_widget, 1)
        content_column.addWidget(self.credits_bar)

        body_layout = QHBoxLayout()
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)
        body_layout.addWidget(self.sidebar)
        body_layout.addLayout(content_column, 1)
        outer_layout.addLayout(body_layout)

        self._register_pages()
        self.navigation_service.page_changed.connect(self._show_page)
        self.navigation_service.page_changed.connect(self.sidebar.set_active_page)

        for item in self.sidebar.items:
            item.clicked.connect(self.navigation_service.navigate)

        self.navigation_service.navigate(PAGE_ID_DASHBOARD)

    def _build_logo_slot(self) -> QLabel:
        slot = QLabel()
        slot.setObjectName("logoSlot")
        slot.setAttribute(Qt.WA_StyledBackground, True)
        slot.setFixedSize(Sidebar.WIDTH, TitleBar.HEIGHT)
        slot.setAlignment(Qt.AlignCenter)

        logo_path = icon("logo")
        if logo_path.is_file():
            size = self.settings.get("controls", {}).get("logo_size", 24)
            slot.setPixmap(QIcon(str(logo_path)).pixmap(QSize(size, size)))
        else:
            slot.setText(self.settings.get("app_name", "")[:1])
        return slot

    def _copyright_text(self) -> str:
        """Fall back to year + app name so the credits bar's left slot is never blank."""
        declared = self.settings.get("copyright", "")
        if declared:
            return declared
        year = self.settings.get("year", "")
        app_name = self.settings.get("app_name", "")
        return f"\u00a9 {year} {app_name}".strip()

    def _register_pages(self):
        settings_page = SettingsPage(
            name="settingsPage", settings=self.settings, controller=self._settings_controller
        )
        settings_page.credits_bar_visibility_changed.connect(self.credits_bar.setVisible)
        settings_page.credits_message_changed.connect(self.credits_bar.set_custom_message)
        self.credits_bar.setVisible(settings_page.controller.credits_bar_visible())
        self.credits_bar.set_custom_message(settings_page.controller.credits_message())

        pages = [
            (
                PAGE_ID_DASHBOARD,
                Dashboard(
                    name="dashboardPage",
                    settings=self.settings,
                    application_service=self.application_service,
                ),
            ),
            (
                PAGE_ID_APPLICATIONS,
                Applications(
                    name="applicationsPage",
                    settings=self.settings,
                    application_service=self.application_service,
                ),
            ),
            (PAGE_ID_TOOLS, Tools(name="toolsPage", settings=self.settings)),
            (PAGE_ID_SETTINGS, settings_page),
            (PAGE_ID_ABOUT, About(name="aboutPage", settings=self.settings)),
        ]
        for page_id, widget in pages:
            self.stacked_widget.addWidget(widget)
            self.navigation_service.register_page(page_id, widget)

        dashboard = self.navigation_service.widget_for(PAGE_ID_DASHBOARD)
        dashboard.add_application_requested.connect(self._start_add_application)

    def _start_add_application(self):
        self.navigation_service.navigate(PAGE_ID_APPLICATIONS)
        self.navigation_service.widget_for(PAGE_ID_APPLICATIONS).start_add_flow()

    def _show_page(self, page_id: str):
        widget = self.navigation_service.widget_for(page_id)
        if widget is not None:
            self.stacked_widget.setCurrentWidget(widget)
