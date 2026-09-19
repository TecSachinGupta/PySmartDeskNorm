from __future__ import annotations

from PySide6.QtWidgets import QVBoxLayout, QWidget

from constants import PAGE_ID_DASHBOARD
from views.components.ActionButton import ActionButton
from views.components.ActivityCard import ActivityCard
from views.components.PageHeader import PageHeader
from views.components.Row import Row
from views.components.SectionCard import SectionCard
from views.components.StatCard import StatCard


class Dashboard(QWidget):
    page_id = PAGE_ID_DASHBOARD

    def __init__(self, name=None, parent=None, settings=None):
        super().__init__(parent)
        self.setObjectName(name or "dashboardPage")
        self.settings = settings or {}

        header = PageHeader(title="Dashboard", subtitle="Overview of your workspace")

        stats = Row(
            name="dashboardStatsRow",
            widgets=[
                StatCard(
                    icon_text="\u25a0", title="Apps Tracked", value="12", description="+2 this week"
                ),
                StatCard(icon_text="\u25b2", title="Tools Used", value="8", description="Active"),
                StatCard(icon_text="\u2699", title="Automations", value="3", description="Running"),
            ],
        )

        self.action_buttons = [
            ActionButton(icon_text="+", title="Add Application", description="Track a new app"),
            ActionButton(
                icon_text="\u2318", title="Open Tools", description="Browse the tool catalogue"
            ),
        ]
        actions = Row(name="dashboardActionsRow", widgets=self.action_buttons)
        quick_actions = SectionCard(title="Quick Actions", content_widgets=[actions])

        activity = ActivityCard(
            title="Recent Activity",
            entries=[
                {"text": "Added Visual Studio Code", "timestamp": "2h ago"},
                {"text": "Updated theme to Dracula", "timestamp": "1d ago"},
            ],
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        layout.addWidget(header)
        layout.addWidget(stats)
        layout.addWidget(quick_actions)
        layout.addWidget(activity)
        layout.addStretch(1)
