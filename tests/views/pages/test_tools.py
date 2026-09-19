from constants import PAGE_ID_TOOLS
from views.pages.Tools import Tools


def test_page_constructs_without_error(qtbot, sample_settings):
    page = Tools(settings=sample_settings)
    qtbot.addWidget(page)
    assert page.page_id == PAGE_ID_TOOLS


def test_tools_page_filters_by_search_text(qtbot):
    tools = Tools(settings={})
    qtbot.addWidget(tools)
    tools.show()

    tools.search_input.setText("format")
    visible_titles = [card.title_text for card in tools.cards if card.isVisible()]

    assert visible_titles == ["Formatter"]


def test_tools_page_filters_by_category(qtbot):
    tools = Tools(settings={})
    qtbot.addWidget(tools)
    tools.show()

    tools._select_category("Files")
    visible_titles = [card.title_text for card in tools.cards if card.isVisible()]

    assert visible_titles == ["Converter"]
    assert tools.category_buttons["Files"].isActive is True
    assert tools.category_buttons["All"].isActive is False


def test_tools_page_shows_empty_state_when_no_matches(qtbot):
    tools = Tools(settings={})
    qtbot.addWidget(tools)
    tools.show()

    tools.search_input.setText("does-not-exist")

    assert tools.empty_state.isVisible() is True
    assert tools.cards_row.isVisible() is False

    tools.search_input.setText("")
    assert tools.empty_state.isVisible() is False
    assert tools.cards_row.isVisible() is True
