from PySide6.QtWidgets import QMessageBox

from constants import PAGE_ID_ABOUT, PAGE_ID_APPLICATIONS, PAGE_ID_TOOLS
from models.application import Application
from services.application_service import ApplicationService
from views.pages.About import About
from views.pages.Applications import Applications
from views.pages.Tools import Tools


def _page(qtbot, applications):
    service = ApplicationService(applications=applications)
    page = Applications(settings={}, application_service=service)
    qtbot.addWidget(page)
    page.show()
    return page, service


def test_page_constructs_without_error(qtbot, sample_settings):
    page = Applications(settings=sample_settings)
    qtbot.addWidget(page)
    assert page.page_id == PAGE_ID_APPLICATIONS


def test_grid_shows_one_card_per_tracked_application(qtbot):
    page, _ = _page(qtbot, [Application("a", "Alpha"), Application("b", "Beta")])

    assert [card.title_text for card in page.cards] == ["Alpha", "Beta"]
    assert page.grid_host.isVisible() is True
    assert page.empty_state.isVisible() is False


def test_search_filters_the_grid_live(qtbot):
    page, _ = _page(qtbot, [Application("a", "Firefox"), Application("b", "Terminal")])

    page.search_input.setText("fire")
    assert [card.title_text for card in page.cards] == ["Firefox"]

    page.search_input.setText("")
    assert len(page.cards) == 2


def test_search_with_no_matches_shows_the_empty_state(qtbot):
    page, _ = _page(qtbot, [Application("a", "Firefox")])

    page.search_input.setText("nothing-matches")

    assert page.cards == []
    assert page.empty_state.isVisible() is True
    assert page.empty_state.title_label.text() == "No matching applications"


def test_nothing_tracked_prompts_to_add_the_first_app(qtbot):
    page, _ = _page(qtbot, [])

    assert page.cards == []
    assert page.empty_state.isVisible() is True
    assert page.empty_state.title_label.text() == "No applications tracked yet"


def test_removing_an_app_updates_the_grid_immediately(qtbot, monkeypatch):
    page, service = _page(qtbot, [Application("a", "Alpha"), Application("b", "Beta")])
    monkeypatch.setattr(QMessageBox, "question", lambda *a, **k: QMessageBox.Yes)

    page.cards[0].remove_button.click()

    assert service.count() == 1
    assert [card.title_text for card in page.cards] == ["Beta"]


def test_declining_the_confirmation_keeps_the_app(qtbot, monkeypatch):
    page, service = _page(qtbot, [Application("a", "Alpha")])
    monkeypatch.setattr(QMessageBox, "question", lambda *a, **k: QMessageBox.No)

    page.cards[0].remove_button.click()

    assert service.count() == 1
    assert [card.title_text for card in page.cards] == ["Alpha"]


def test_adding_from_a_path_tracks_it_and_refreshes_the_grid(qtbot):
    page, service = _page(qtbot, [])

    page.add_application_from_path("/Applications/Cool Editor.app")

    assert service.count() == 1
    assert [card.title_text for card in page.cards] == ["Cool Editor"]


# NOTE: also covers Tools and About; kept whole to preserve the original assertions.
def test_applications_tools_about_pages_build(qtbot):
    applications = Applications(settings={"app_name": "PySmartDeskNorm"})
    tools = Tools(settings={"app_name": "PySmartDeskNorm"})
    about = About(
        settings={
            "app_name": "PySmartDeskNorm",
            "version": "v1.0.0",
            "description": "Test description",
            "copyright": "Copyright",
            "year": 2026,
        }
    )

    for widget in (applications, tools, about):
        qtbot.addWidget(widget)

    assert applications.page_id == PAGE_ID_APPLICATIONS
    assert tools.page_id == PAGE_ID_TOOLS
    assert about.page_id == PAGE_ID_ABOUT
