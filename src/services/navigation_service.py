from __future__ import annotations

from PySide6.QtCore import QObject, Signal

from utils.logging_config import get_logger

logger = get_logger(__name__)


class NavigationService(QObject):
    """Signal-based registry mapping page ids to page widgets for AppShell."""

    page_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._pages = {}
        self._current_page_id = None

    def register_page(self, page_id: str, widget) -> None:
        self._pages[page_id] = widget

    @property
    def current_page_id(self):
        return self._current_page_id

    def widget_for(self, page_id: str):
        return self._pages.get(page_id)

    def navigate(self, page_id: str) -> None:
        if page_id not in self._pages:
            logger.warning("Ignoring navigation to unregistered page id: %s", page_id)
            return
        if page_id == self._current_page_id:
            return
        self._current_page_id = page_id
        logger.debug("Navigating to page: %s", page_id)
        self.page_changed.emit(page_id)
