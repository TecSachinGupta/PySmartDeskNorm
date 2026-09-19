from PySide6.QtCore import QSettings

from constants import (
    PAGE_ID_ABOUT,
    PAGE_ID_APPLICATIONS,
    PAGE_ID_DASHBOARD,
    PAGE_ID_SETTINGS,
    PAGE_ID_TOOLS,
)
from controllers.settings_controller import SettingsController
from services.settings_service import SettingsService
from views.containers.AppShell import AppShell
from views.pages.About import About
from views.pages.Applications import Applications
from views.pages.Settings import Settings as SettingsPage
from views.pages.Tools import Tools


def _ini_backed_controller(tmp_path):
    ini_path = tmp_path / "settings.ini"
    qsettings = QSettings(str(ini_path), QSettings.IniFormat)
    return SettingsController(settings_service=SettingsService(settings=qsettings)), ini_path


def test_settings_persist_across_service_restarts(tmp_path):
    controller, ini_path = _ini_backed_controller(tmp_path)
    controller.select_theme("dracula")
    controller.set_credits_bar_visible(False)

    # simulate an app restart: a brand-new service/controller against the same store
    restarted_qsettings = QSettings(str(ini_path), QSettings.IniFormat)
    restarted_controller = SettingsController(
        settings_service=SettingsService(settings=restarted_qsettings)
    )

    assert restarted_controller.current_theme() == "dracula"
    assert restarted_controller.credits_bar_visible() is False


def test_settings_controller_lists_available_themes(tmp_path):
    controller, _ = _ini_backed_controller(tmp_path)
    themes = controller.available_themes()

    assert themes == sorted(themes)
    assert {"default", "bright", "dracula"}.issubset(set(themes))


def test_applications_tools_about_pages_build(qtbot):
    applications = Applications(settings={"app_name": "PySmartDeskNorm"})
    tools = Tools(settings={"app_name": "PySmartDeskNorm"})
    about = About(
        settings={
            "app_name": "PySmartDeskNorm",
            "version": "v1.0.0",
            "description": "Test description",
            "copyright": "Copyright",
            "year": 2026,
        }
    )

    for widget in (applications, tools, about):
        qtbot.addWidget(widget)

    assert applications.page_id == PAGE_ID_APPLICATIONS
    assert tools.page_id == PAGE_ID_TOOLS
    assert about.page_id == PAGE_ID_ABOUT


def test_tools_page_filters_by_search_text(qtbot):
    tools = Tools(settings={})
    qtbot.addWidget(tools)
    tools.show()

    tools.search_input.setText("format")
    visible_titles = [card.title_text for card in tools.cards if card.isVisible()]

    assert visible_titles == ["Formatter"]


def test_tools_page_filters_by_category(qtbot):
    tools = Tools(settings={})
    qtbot.addWidget(tools)
    tools.show()

    tools._select_category("Files")
    visible_titles = [card.title_text for card in tools.cards if card.isVisible()]

    assert visible_titles == ["Converter"]
    assert tools.category_buttons["Files"].isActive is True
    assert tools.category_buttons["All"].isActive is False


def test_settings_page_switches_theme_and_emits_credits_bar_signal(qtbot, tmp_path):
    controller, _ = _ini_backed_controller(tmp_path)
    page = SettingsPage(settings={"app_name": "PySmartDeskNorm"}, controller=controller)
    qtbot.addWidget(page)

    received = []
    page.credits_bar_visibility_changed.connect(received.append)

    page.theme_combo.setCurrentText("Dracula")
    assert controller.current_theme() == "dracula"

    page.credits_bar_toggle.setChecked(not page.credits_bar_toggle.isChecked())
    assert received


def test_appshell_registers_all_five_pages(qtbot, tmp_path):
    controller, _ = _ini_backed_controller(tmp_path)
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
