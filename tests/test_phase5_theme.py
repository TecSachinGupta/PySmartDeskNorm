from PySide6.QtWidgets import QApplication

from configs.Themes import Themes


def test_theme_tokens_are_present_and_apply_sets_stylesheet():
    themes = Themes()

    assert "spacing" in themes.items
    assert "typography" in themes.items
    assert "radius" in themes.items

    app = QApplication.instance() or QApplication([])
    themes.apply(app)

    stylesheet = app.styleSheet()
    assert isinstance(stylesheet, str)
    assert stylesheet != ""
    assert "border-radius" in stylesheet.lower() or "font-family" in stylesheet.lower()
