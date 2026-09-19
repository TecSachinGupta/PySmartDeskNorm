from views.widgets.CreditsBar import CreditsBar


def test_credits_bar_constructs(qtbot):
    widget = CreditsBar(
        name="credits", customMessage="Built with PySide6", parent=None, settings={}
    )
    qtbot.addWidget(widget)
    assert widget is not None


def test_credits_bar_custom_message_toggles_visibility(qtbot):
    credits_bar = CreditsBar(copyright="Copyright", version="v1.0.0", settings={})
    qtbot.addWidget(credits_bar)
    credits_bar.show()

    assert credits_bar._custom_message_label.isVisible() is False

    credits_bar.set_custom_message("Hello there")
    assert credits_bar._custom_message_label.text() == "Hello there"
    assert credits_bar._custom_message_label.isVisible() is True

    credits_bar.set_custom_message("")
    assert credits_bar._custom_message_label.isVisible() is False
