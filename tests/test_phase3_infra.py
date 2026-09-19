from pathlib import Path

from constants import PAGE_ID_DASHBOARD, SIGNAL_NAVIGATE
from utils.logging_config import configure_logging, get_logger
from utils.resource import icon, resource_path


def test_resource_path_is_cwd_safe(monkeypatch):
    monkeypatch.chdir(Path("/tmp"))
    resolved = resource_path("icons/home.svg")
    assert resolved.is_file()
    assert resolved.name == "home.svg"
    assert icon("home").is_file()


def test_logging_helpers_are_available():
    configure_logging()
    logger = get_logger("phase3.test")
    assert logger.name == "phase3.test"
    assert SIGNAL_NAVIGATE == "navigate"
    assert PAGE_ID_DASHBOARD == "dashboard"
