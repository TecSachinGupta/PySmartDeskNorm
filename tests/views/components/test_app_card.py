from __future__ import annotations

from views.components.AppCard import AppCard


def test_app_card_shows_name_and_metadata(qtbot):
    card = AppCard(
        app_id="vscode", title="Visual Studio Code", icon="component", meta="Added 2h ago"
    )
    qtbot.addWidget(card)

    assert card.title_label.text() == "Visual Studio Code"
    assert card.meta_label.text() == "Added 2h ago"
    assert not card.icon_label.pixmap().isNull()


def test_app_card_falls_back_to_a_generic_icon(qtbot):
    """A missing or unknown icon must still render something."""
    without_icon = AppCard(app_id="a", title="No Icon", icon=None)
    unknown_icon = AppCard(app_id="b", title="Unknown", icon="definitely-not-a-real-icon")
    qtbot.addWidget(without_icon)
    qtbot.addWidget(unknown_icon)

    assert not without_icon.icon_label.pixmap().isNull()
    assert not unknown_icon.icon_label.pixmap().isNull()


def test_app_card_emits_open_and_remove_with_its_app_id(qtbot):
    card = AppCard(app_id="vscode", title="Visual Studio Code")
    qtbot.addWidget(card)

    opened, removed = [], []
    card.open_requested.connect(opened.append)
    card.remove_requested.connect(removed.append)

    card.open_button.click()
    card.remove_button.click()

    assert opened == ["vscode"]
    assert removed == ["vscode"]
