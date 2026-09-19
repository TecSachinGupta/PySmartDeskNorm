from PySide6.QtWidgets import QApplication

from configs.Themes import Themes
from views.containers.AppShell import AppShell
from views.widgets.Sidebar import Sidebar
from views.widgets.TitleBar import TitleBar


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


def test_swapping_theme_changes_appearance_without_code_changes():
    """Phase 5 'Done when': a different theme file restyles the app with no code change."""
    app = QApplication.instance() or QApplication([])

    default_qss = Themes(theme="default").apply(app)
    dracula_qss = Themes(theme="dracula").apply(app)
    bright_qss = Themes(theme="bright").apply(app)

    assert default_qss != dracula_qss != bright_qss
    assert app.styleSheet() == bright_qss

    # Each theme's own palette must actually reach the stylesheet.
    assert Themes(theme="dracula").items["colors"]["accentColor"] in dracula_qss
    assert Themes(theme="bright").items["colors"]["primaryBackgroundColor"] in bright_qss


def test_chrome_widgets_carry_no_inline_stylesheet(qtbot):
    """Chrome must pull from the applied theme rather than styling itself."""
    settings = Themes().items | {"app_name": "PySmartDeskNorm"}

    title_bar = TitleBar(name="titleBar", settings=settings)
    sidebar = Sidebar(name="sidebar", settings=settings)
    shell = AppShell(settings=settings)
    for widget in (title_bar, sidebar, shell):
        qtbot.addWidget(widget)

    assert shell.styleSheet() == ""
    assert shell.objectName() == "appshell"
    assert sidebar.styleSheet() == ""
    assert title_bar.title_label.styleSheet() == ""
    assert all(item.styleSheet() == "" for item in sidebar.items)


def test_sidebar_active_state_uses_theme_driven_property(qtbot):
    sidebar = Sidebar(name="sidebar", settings={})
    qtbot.addWidget(sidebar)

    sidebar.set_active_page("tools")

    for item in sidebar.items:
        assert item.property("active") is (item.page_id == "tools")
