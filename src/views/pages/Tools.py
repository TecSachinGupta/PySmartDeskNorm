from __future__ import annotations

from typing import ClassVar

from PySide6.QtWidgets import QVBoxLayout, QWidget

from constants import PAGE_ID_TOOLS
from views.components.Button import Button
from views.components.EmptyState import EmptyState
from views.components.PageHeader import PageHeader
from views.components.Row import Row
from views.components.SearchInput import SearchInput
from views.components.ToolCard import ToolCard


class Tools(QWidget):
    page_id = PAGE_ID_TOOLS

    # Demonstrates the catalogue pattern; not a real tool registry yet.
    CATALOGUE: ClassVar[list[dict[str, str]]] = [
        {
            "id": "formatter",
            "title": "Formatter",
            "category": "Text",
            "description": "Reformat text and code snippets.",
        },
        {
            "id": "converter",
            "title": "Converter",
            "category": "Files",
            "description": "Convert between common file formats.",
        },
        {
            "id": "inspector",
            "title": "Inspector",
            "category": "Debug",
            "description": "Inspect app settings and themes.",
        },
    ]

    def __init__(self, name=None, parent=None, settings=None):
        super().__init__(parent)
        self.setObjectName(name or "toolsPage")
        self.settings = settings or {}
        self._active_category = "All"

        header = PageHeader(title="Tools", subtitle="Browse the tool catalogue")

        self.search_input = SearchInput(placeholder="Search tools...")
        self.search_input.textChanged.connect(lambda _text: self._apply_filters())

        categories = ["All", *sorted({entry["category"] for entry in self.CATALOGUE})]
        self.category_buttons = {}
        category_widgets = []
        colors = self.settings.get("colors", {})
        for category in categories:
            button = Button(
                name=f"category_{category}_button",
                label=category,
                tooltipLabel=f"Filter by {category}",
                width=90,
                height=28,
                variant="secondary",
                themeColors=colors,
                isActive=(category == "All"),
            )
            button.clicked.connect(lambda checked=False, c=category: self._select_category(c))
            self.category_buttons[category] = button
            category_widgets.append(button)
        category_row = Row(name="toolsCategoryRow", widgets=category_widgets)

        self.cards = [
            ToolCard(
                tool_id=entry["id"],
                title=entry["title"],
                category=entry["category"],
                description=entry["description"],
            )
            for entry in self.CATALOGUE
        ]
        self.cards_row = Row(name="toolsCardsRow", widgets=self.cards)
        self.empty_state = EmptyState(
            title="No tools found",
            description="Try a different search term or category.",
        )
        self.empty_state.setVisible(False)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        layout.addWidget(header)
        layout.addWidget(self.search_input)
        layout.addWidget(category_row)
        layout.addWidget(self.cards_row)
        layout.addWidget(self.empty_state)
        layout.addStretch(1)

    def _select_category(self, category: str) -> None:
        self._active_category = category
        for name, button in self.category_buttons.items():
            button.isActive = name == category
        self._apply_filters()

    def _apply_filters(self) -> None:
        query = self.search_input.text().strip().lower()
        any_visible = False
        for card in self.cards:
            category_match = (
                self._active_category == "All" or card.category == self._active_category
            )
            text_match = (
                not query or query in card.title_text.lower() or query in card.category.lower()
            )
            visible = category_match and text_match
            card.setVisible(visible)
            any_visible = any_visible or visible
        self.cards_row.setVisible(any_visible)
        self.empty_state.setVisible(not any_visible)
