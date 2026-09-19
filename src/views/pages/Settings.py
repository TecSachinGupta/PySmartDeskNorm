from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QVBoxLayout, QWidget

from constants import PAGE_ID_SETTINGS
from controllers.settings_controller import SettingsController
from views.components.AnimatedToggle import AnimatedToggle
from views.components.ComboBox import ComboBox
from views.components.PageHeader import PageHeader
from views.components.SectionCard import SectionCard
from views.components.TextInput import TextInput
from views.components.Toast import Toast


class Settings(QWidget):
    page_id = PAGE_ID_SETTINGS
    credits_bar_visibility_changed = Signal(bool)
    credits_message_changed = Signal(str)

    def __init__(self, name=None, parent=None, settings=None, controller=None):
        super().__init__(parent)
        self.setObjectName(name or "settingsPage")
        self.settings = settings or {}
        self.controller = controller or SettingsController()

        header = PageHeader(title="Settings", subtitle="Appearance and preferences")

        self.theme_combo = ComboBox(
            name="themeComboBox",
            items=[theme_name.title() for theme_name in self.controller.available_themes()],
            current=self.controller.current_theme().title(),
        )
        self.theme_combo.currentTextChanged.connect(self._on_theme_selected)
        theme_section = SectionCard(title="Theme", content_widgets=[self.theme_combo])

        self.credits_bar_toggle = AnimatedToggle()
        self.credits_bar_toggle.setChecked(self.controller.credits_bar_visible())
        self.credits_bar_toggle.stateChanged.connect(self._toggle_credits_bar)
        credits_toggle_section = SectionCard(
            title="Show Credits Bar", content_widgets=[self.credits_bar_toggle]
        )

        self.credits_message_input = TextInput(
            name="creditsMessageInput",
            placeholder="Optional custom credits message",
            text=self.controller.credits_message(),
        )
        self.credits_message_input.textChanged.connect(self._on_credits_message_changed)
        credits_message_section = SectionCard(
            title="Credits Message", content_widgets=[self.credits_message_input]
        )

        self.toast = Toast(parent=self)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        layout.addWidget(header)
        layout.addWidget(theme_section)
        layout.addWidget(credits_toggle_section)
        layout.addWidget(credits_message_section)
        layout.addWidget(self.toast)
        layout.addStretch(1)

    def _on_theme_selected(self, theme_label: str) -> None:
        if not theme_label:
            return
        theme_name = theme_label.lower()
        self.controller.select_theme(theme_name)
        self.toast.show_message(f"Theme changed to {theme_label}")

    def _toggle_credits_bar(self, state: int) -> None:
        visible = bool(state)
        self.controller.set_credits_bar_visible(visible)
        self.credits_bar_visibility_changed.emit(visible)

    def _on_credits_message_changed(self, message: str) -> None:
        self.controller.set_credits_message(message)
        self.credits_message_changed.emit(message)
