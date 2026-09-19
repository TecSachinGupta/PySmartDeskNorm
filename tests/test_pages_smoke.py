from __future__ import annotations

import pytest
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
from views.pages.About import About
from views.pages.Applications import Applications
from views.pages.Dashboard import Dashboard
from views.pages.Settings import Settings as SettingsPage
from views.pages.Tools import Tools

SAMPLE_SETTINGS = {
    "app_name": "PySmartDeskNorm",
    "version": "v1.0.0",
    "description": "Test description",
    "copyright": "Copyright",
    "year": 2026,
}


def _isolated_controller(tmp_path):
    qsettings = QSettings(str(tmp_path / "settings.ini"), QSettings.IniFormat)
    return SettingsController(settings_service=SettingsService(settings=qsettings))


def _dashboard(tmp_path):
    return Dashboard(settings=SAMPLE_SETTINGS)


def _applications(tmp_path):
    return Applications(settings=SAMPLE_SETTINGS)


def _tools(tmp_path):
    return Tools(settings=SAMPLE_SETTINGS)


def _settings(tmp_path):
    return SettingsPage(settings=SAMPLE_SETTINGS, controller=_isolated_controller(tmp_path))


def _about(tmp_path):
    return About(settings=SAMPLE_SETTINGS)


@pytest.mark.parametrize(
    "factory,expected_page_id",
    [
        (_dashboard, PAGE_ID_DASHBOARD),
        (_applications, PAGE_ID_APPLICATIONS),
        (_tools, PAGE_ID_TOOLS),
        (_settings, PAGE_ID_SETTINGS),
        (_about, PAGE_ID_ABOUT),
    ],
)
def test_page_constructs_without_error(qtbot, tmp_path, factory, expected_page_id):
    page = factory(tmp_path)
    qtbot.addWidget(page)
    assert page.page_id == expected_page_id
