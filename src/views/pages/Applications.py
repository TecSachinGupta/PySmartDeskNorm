from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFileDialog, QGridLayout, QMessageBox, QVBoxLayout, QWidget

from constants import PAGE_ID_APPLICATIONS
from services.application_service import ApplicationService
from utils.logging_config import get_logger
from views.components.AppCard import AppCard
from views.components.Button import Button
from views.components.EmptyState import EmptyState
from views.components.PageHeader import PageHeader
from views.components.SearchInput import SearchInput
from views.components.Toast import Toast

logger = get_logger(__name__)

COLUMNS = 3


class Applications(QWidget):
    page_id = PAGE_ID_APPLICATIONS
    application_opened = Signal(str)

    def __init__(self, name=None, parent=None, settings=None, application_service=None):
        super().__init__(parent)
        self.setObjectName(name or "applicationsPage")
        self.settings = settings or {}
        self.service = application_service or ApplicationService(self)
        self.cards: list[AppCard] = []

        colors = self.settings.get("colors", {})
        self.add_button = Button(
            name="addApplicationButton",
            label="+ Add",
            tooltipLabel="Track a new application",
            width=80,
            height=28,
            radius=6,
            variant="primary",
            themeColors=colors,
        )
        self.add_button.clicked.connect(self.start_add_flow)

        header = PageHeader(
            title="Applications",
            subtitle="Apps you're tracking",
            actions=[self.add_button],
        )

        self.search_input = SearchInput(placeholder="Search applications...")
        self.search_input.textChanged.connect(lambda _text: self._render())

        self.grid_host = QWidget()
        self.grid_host.setObjectName("applicationsGrid")
        self.grid = QGridLayout(self.grid_host)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setSpacing(12)

        self.empty_state = EmptyState(title="", description="")
        self.toast = Toast(parent=self)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        layout.addWidget(header)
        layout.addWidget(self.search_input)
        layout.addWidget(self.grid_host)
        layout.addWidget(self.empty_state)
        layout.addWidget(self.toast)
        layout.addStretch(1)

        self.service.changed.connect(self._render)
        self._render()

    def visible_applications(self):
        query = self.search_input.text().strip().lower()
        applications = self.service.list()
        if not query:
            return applications
        return [a for a in applications if query in a.name.lower()]

    def _render(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
        self.cards = []

        applications = self.visible_applications()
        for index, application in enumerate(applications):
            card = AppCard(
                app_id=application.app_id,
                title=application.name,
                icon=application.icon,
                meta=application.added_label,
                themeColors=self.settings.get("colors", {}),
            )
            card.open_requested.connect(self._on_open_requested)
            card.remove_requested.connect(self._on_remove_requested)
            self.grid.addWidget(card, index // COLUMNS, index % COLUMNS)
            self.cards.append(card)

        self.grid_host.setVisible(bool(applications))
        self.empty_state.setVisible(not applications)
        if not applications:
            if self.service.count() > 0:
                self.empty_state.title_label.setText("No matching applications")
                self.empty_state.description_label.setText("Try a different search term.")
            else:
                self.empty_state.title_label.setText("No applications tracked yet")
                self.empty_state.description_label.setText("Add your first one to get started.")
            self.empty_state.description_label.setVisible(True)

    def start_add_flow(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select an application")
        if path:
            self.add_application_from_path(path)

    def add_application_from_path(self, path: str):
        application = self.service.add(name=Path(path).stem)
        self.toast.show_message(f"Now tracking {application.name}")
        return application

    def _on_open_requested(self, app_id: str):
        application = next((a for a in self.service.list() if a.app_id == app_id), None)
        if application is None:
            return
        # Launching a real process is deliberately out of scope for this pass.
        logger.info("Open requested for application: %s", application.name)
        self.toast.show_message(f"Opening {application.name}...")
        self.application_opened.emit(app_id)

    def _on_remove_requested(self, app_id: str):
        application = next((a for a in self.service.list() if a.app_id == app_id), None)
        if application is None:
            return
        answer = QMessageBox.question(
            self,
            "Stop tracking",
            f"Stop tracking {application.name}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if answer == QMessageBox.Yes:
            self.service.remove(app_id)
