from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QStackedWidget

from constants import PAGE_ID_APPLICATIONS, PAGE_ID_DASHBOARD
from controllers.settings_controller import SettingsController
from services.navigation_service import NavigationService
from services.settings_service import SettingsService
from views.containers.AppShell import AppShell
from views.pages.Dashboard import Dashboard


def test_navigation_service_navigates_between_registered_pages():
    service = NavigationService()
    seen = []
    service.page_changed.connect(seen.append)

    service.register_page(PAGE_ID_DASHBOARD, object())
    service.navigate(PAGE_ID_DASHBOARD)
    service.navigate(PAGE_ID_DASHBOARD)  # same page again: no duplicate emit
    service.navigate(PAGE_ID_APPLICATIONS)  # unregistered: no-op

    assert seen == [PAGE_ID_DASHBOARD]
    assert service.current_page_id == PAGE_ID_DASHBOARD


def test_dashboard_page_builds(qtbot):
    dashboard = Dashboard(settings={"app_name": "PySmartDeskNorm"})
    qtbot.addWidget(dashboard)
    assert dashboard.page_id == PAGE_ID_DASHBOARD


def test_appshell_shows_dashboard_and_tracks_active_sidebar_item(qtbot, tmp_path):
    ini_settings = QSettings(str(tmp_path / "settings.ini"), QSettings.IniFormat)
    controller = SettingsController(settings_service=SettingsService(settings=ini_settings))
    shell = AppShell(
        name="appshell", settings={"app_name": "PySmartDeskNorm"}, settings_controller=controller
    )
    qtbot.addWidget(shell)

    dashboard_widget = shell.navigation_service.widget_for(PAGE_ID_DASHBOARD)
    assert isinstance(shell.stacked_widget, QStackedWidget)
    assert isinstance(dashboard_widget, Dashboard)
    assert shell.stacked_widget.currentWidget() is dashboard_widget

    dashboard_item = next(item for item in shell.sidebar.items if item.page_id == PAGE_ID_DASHBOARD)
    assert dashboard_item.active is True
