from constants import PAGE_ID_ABOUT
from views.pages.About import About


def test_page_constructs_without_error(qtbot, sample_settings):
    page = About(settings=sample_settings)
    qtbot.addWidget(page)
    assert page.page_id == PAGE_ID_ABOUT
