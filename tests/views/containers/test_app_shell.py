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
from views.widgets.Sidebar import Sidebar


def test_logo_slot_matches_sidebar_width_and_title_bar_takes_the_rest(qtbot, ini_controller):
    """Top band is a logo slot the width of the sidebar plus the title bar beside it."""
    controller, _ = ini_controller()
    shell = AppShell(settings={"app_name": "PySmartDeskNorm"}, settings_controller=controller)
    qtbot.addWidget(shell)
    shell.resize(1024, 768)
    shell.show()

    assert shell.logo_slot.width() == Sidebar.WIDTH
    assert shell.logo_slot.mapTo(shell, shell.logo_slot.rect().topLeft()).x() == 0

    title_x = shell.title_bar.mapTo(shell, shell.title_bar.rect().topLeft()).x()
    assert title_x == Sidebar.WIDTH
    assert shell.title_bar.width() == shell.width() - Sidebar.WIDTH


def test_dashboard_and_applications_share_one_application_service(qtbot, ini_controller):
    """Both pages must read the same list, not two disconnected ones."""
    controller, _ = ini_controller()
    shell = AppShell(settings={}, settings_controller=controller)
    qtbot.addWidget(shell)

    dashboard = shell.navigation_service.widget_for(PAGE_ID_DASHBOARD)
    applications = shell.navigation_service.widget_for(PAGE_ID_APPLICATIONS)

    assert dashboard.service is shell.application_service
    assert applications.service is shell.application_service
    assert dashboard.apps_tracked_card.value_label.text() == str(len(applications.cards))


def test_add_application_navigates_then_starts_the_add_flow(qtbot, ini_controller, monkeypatch):
    controller, _ = ini_controller()
    shell = AppShell(settings={}, settings_controller=controller)
    qtbot.addWidget(shell)

    monkeypatch.setattr(
        "views.pages.Applications.QFileDialog.getOpenFileName",
        lambda *a, **k: ("/Applications/Brand New.app", ""),
    )

    before = shell.application_service.count()
    shell.navigation_service.widget_for(PAGE_ID_DASHBOARD).add_application_requested.emit()

    assert shell.navigation_service.current_page_id == PAGE_ID_APPLICATIONS
    assert shell.application_service.count() == before + 1
    assert any(a.name == "Brand New" for a in shell.application_service.list())


def test_credits_bar_sits_in_the_content_column_with_both_text_slots(qtbot, ini_controller):
    """The credits bar must not span the full width, and neither end may be blank."""
    controller, _ = ini_controller()
    shell = AppShell(
        settings={"app_name": "PySmartDeskNorm", "version": "v1.0.0", "year": 2022},
        settings_controller=controller,
    )
    qtbot.addWidget(shell)
    shell.resize(1024, 768)
    shell.show()

    credits_x = shell.credits_bar.mapTo(shell, shell.credits_bar.rect().topLeft()).x()
    assert credits_x == Sidebar.WIDTH
    assert shell.credits_bar.width() == shell.width() - Sidebar.WIDTH

    texts = [
        shell.credits_bar.frameLayout.itemAt(i).widget().text()
        for i in range(shell.credits_bar.frameLayout.count())
        if shell.credits_bar.frameLayout.itemAt(i).widget() is not None
    ]
    assert "v1.0.0" in texts
    assert any("2022" in t for t in texts)


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
