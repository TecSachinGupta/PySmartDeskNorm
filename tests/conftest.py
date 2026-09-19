from __future__ import annotations

import pytest
from PySide6.QtCore import QSettings

from controllers.settings_controller import SettingsController
from services.settings_service import SettingsService

# `qtbot` / `qapp` come from pytest-qt and do not need to be redefined here.

SAMPLE_SETTINGS = {
    "app_name": "PySmartDeskNorm",
    "version": "v1.0.0",
    "description": "Test description",
    "copyright": "Copyright",
    "year": 2026,
}


@pytest.fixture
def sample_settings():
    return dict(SAMPLE_SETTINGS)


@pytest.fixture
def ini_controller(tmp_path):
    """SettingsController backed by a temp ini file so tests never touch the real OS store."""

    def _make(filename: str = "settings.ini"):
        ini_path = tmp_path / filename
        qsettings = QSettings(str(ini_path), QSettings.IniFormat)
        controller = SettingsController(settings_service=SettingsService(settings=qsettings))
        return controller, ini_path

    return _make
