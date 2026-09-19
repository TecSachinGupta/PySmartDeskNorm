from __future__ import annotations

from datetime import datetime, timedelta
from uuid import uuid4

from PySide6.QtCore import QObject, Signal

from models.application import Application
from utils.logging_config import get_logger

logger = get_logger(__name__)


def _seed_applications() -> list[Application]:
    """Mock data stands in for real app detection, which is out of scope for now."""
    now = datetime.now()
    return [
        Application("vscode", "Visual Studio Code", "component", now - timedelta(hours=2)),
        Application("terminal", "Terminal", "menu2", now - timedelta(days=1)),
        Application("firefox", "Firefox", "signal", now - timedelta(days=3)),
        Application("figma", "Figma", "drawing-compass", now - timedelta(days=5)),
        Application("obsidian", "Obsidian", "library", now - timedelta(days=9)),
        Application("scratch", "Scratchpad", None, now - timedelta(days=12)),
    ]


class ApplicationService(QObject):
    """Single source of truth for tracked applications, shared by Dashboard and Applications."""

    changed = Signal()

    def __init__(self, parent=None, applications: list[Application] | None = None):
        super().__init__(parent)
        self._applications = list(_seed_applications() if applications is None else applications)

    def list(self) -> list[Application]:
        return list(self._applications)

    def count(self) -> int:
        return len(self._applications)

    def add(self, name: str, icon: str | None = None) -> Application:
        application = Application(app_id=uuid4().hex, name=name, icon=icon)
        self._applications.insert(0, application)
        logger.info("Tracking application: %s", name)
        self.changed.emit()
        return application

    def remove(self, app_id: str) -> None:
        remaining = [a for a in self._applications if a.app_id != app_id]
        if len(remaining) == len(self._applications):
            return
        self._applications = remaining
        logger.info("Stopped tracking application: %s", app_id)
        self.changed.emit()
