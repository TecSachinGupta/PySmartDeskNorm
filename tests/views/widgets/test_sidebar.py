from constants import (
    PAGE_ID_ABOUT,
    PAGE_ID_APPLICATIONS,
    PAGE_ID_DASHBOARD,
    PAGE_ID_SETTINGS,
    PAGE_ID_TOOLS,
)
from views.widgets.Sidebar import Sidebar


def test_sidebar_active_state_uses_theme_driven_property(qtbot):
    sidebar = Sidebar(name="sidebar", settings={})
    qtbot.addWidget(sidebar)

    sidebar.set_active_page("tools")

    for item in sidebar.items:
        assert item.property("active") is (item.page_id == "tools")


def test_sidebar_splits_nav_into_top_and_bottom_groups(qtbot):
    sidebar = Sidebar(name="sidebar", settings={})
    qtbot.addWidget(sidebar)

    assert [i.page_id for i in sidebar.top_items] == [
        PAGE_ID_DASHBOARD,
        PAGE_ID_APPLICATIONS,
        PAGE_ID_TOOLS,
    ]
    assert [i.page_id for i in sidebar.bottom_items] == [PAGE_ID_SETTINGS, PAGE_ID_ABOUT]
    # Every item still belongs to the flat list navigation iterates over.
    assert len(sidebar.items) == len(sidebar.top_items) + len(sidebar.bottom_items)


def test_sidebar_bottom_group_is_anchored_by_a_flexible_spacer(qtbot):
    """A stretch item, not fixed spacing, is what keeps the bottom group flush."""
    sidebar = Sidebar(name="sidebar", settings={})
    qtbot.addWidget(sidebar)

    layout = sidebar.layout()
    stretch_indexes = [
        i for i in range(layout.count()) if layout.itemAt(i).spacerItem() is not None
    ]
    assert stretch_indexes, "expected an expanding spacer between the two nav groups"

    widget_indexes = [i for i in range(layout.count()) if layout.itemAt(i).widget() is not None]
    assert widget_indexes[0] < stretch_indexes[0] < widget_indexes[-1]
