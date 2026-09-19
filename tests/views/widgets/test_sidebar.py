from views.widgets.Sidebar import Sidebar


def test_sidebar_active_state_uses_theme_driven_property(qtbot):
    sidebar = Sidebar(name="sidebar", settings={})
    qtbot.addWidget(sidebar)

    sidebar.set_active_page("tools")

    for item in sidebar.items:
        assert item.property("active") is (item.page_id == "tools")
