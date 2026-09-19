from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QVBoxLayout, QWidget

from constants import PAGE_ID_DASHBOARD
from services.application_service import ApplicationService
from views.components.ActionButton import ActionButton
from views.components.ActivityCard import ActivityCard
from views.components.PageHeader import PageHeader
from views.components.Row import Row
from views.components.SectionCard import SectionCard
from views.components.StatCard import StatCard


class Dashboard(QWidget):
    page_id = PAGE_ID_DASHBOARD
    add_application_requested = Signal()

    def __init__(self, name=None, parent=None, settings=None, application_service=None):
        super().__init__(parent)
        self.setObjectName(name or "dashboardPage")
        self.settings = settings or {}
        self.service = application_service or ApplicationService(self)

        header = PageHeader(title="Dashboard", subtitle="Overview of your workspace")

        self.apps_tracked_card = StatCard(
            icon_text="\u25a0",
            title="Apps Tracked",
            value=str(self.service.count()),
            description="Across your workspace",
        )
        stats = Row(
            name="dashboardStatsRow",
            widgets=[
                self.apps_tracked_card,
                StatCard(icon_text="\u25b2", title="Tools Used", value="8", description="Active"),
                StatCard(icon_text="\u2699", title="Automations", value="3", description="Running"),
            ],
        )

        self.add_application_button = ActionButton(
            icon_text="+", title="Add Application", description="Track a new app"
        )
        self.add_application_button.clicked.connect(self.add_application_requested.emit)
        self.action_buttons = [
            self.add_application_button,
            ActionButton(
                icon_text="\u2318", title="Open Tools", description="Browse the tool catalogue"
            ),
        ]
        actions = Row(name="dashboardActionsRow", widgets=self.action_buttons)
        quick_actions = SectionCard(title="Quick Actions", content_widgets=[actions])

        self.activity_card = ActivityCard(title="Recent Activity", entries=self._recent_activity())

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        layout.addWidget(header)
        layout.addWidget(stats)
        layout.addWidget(quick_actions)
        layout.addWidget(self.activity_card)
        layout.addStretch(1)

        self.service.changed.connect(self._refresh_stats)

    def _recent_activity(self):
        return [
            {"text": f"Added {a.name}", "timestamp": a.added_label.replace("Added ", "")}
            for a in self.service.list()[:3]
        ]

    def _refresh_stats(self):
        self.apps_tracked_card.value_label.setText(str(self.service.count()))
