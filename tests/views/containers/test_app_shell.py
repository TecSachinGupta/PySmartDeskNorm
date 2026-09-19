from PySide6.QtWidgets import QStackedWidget

from constants import (
    PAGE_ID_ABOUT,
    PAGE_ID_APPLICATIONS,
    PAGE_ID_DASHBOARD,
    PAGE_ID_SETTINGS,
    PAGE_ID_TOOLS,
)
from views.containers.AppShell import AppShell
from views.pages.Dashboard import Dashboard


def test_appshell_shows_dashboard_and_tracks_active_sidebar_item(qtbot, ini_controller):
    controller, _ = ini_controller()
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


def test_appshell_registers_all_five_pages(qtbot, ini_controller):
    controller, _ = ini_controller()
    shell = AppShell(
        name="appshell", settings={"app_name": "PySmartDeskNorm"}, settings_controller=controller
    )
    qtbot.addWidget(shell)

    for page_id in (
        PAGE_ID_DASHBOARD,
        PAGE_ID_APPLICATIONS,
        PAGE_ID_TOOLS,
        PAGE_ID_SETTINGS,
        PAGE_ID_ABOUT,
    ):
        assert shell.navigation_service.widget_for(page_id) is not None


def test_settings_page_credits_message_flows_to_credits_bar(qtbot, ini_controller):
    controller, _ = ini_controller()
    shell = AppShell(
        name="appshell", settings={"app_name": "PySmartDeskNorm"}, settings_controller=controller
    )
    qtbot.addWidget(shell)
    shell.show()

    settings_page = shell.navigation_service.widget_for("settings")
    settings_page.credits_message_input.setText("Made with love")

    assert shell.credits_bar._custom_message_label.text() == "Made with love"
    assert shell.credits_bar._custom_message_label.isVisible() is True
