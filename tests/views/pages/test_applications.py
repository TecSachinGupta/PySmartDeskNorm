from constants import PAGE_ID_ABOUT, PAGE_ID_APPLICATIONS, PAGE_ID_TOOLS
from views.pages.About import About
from views.pages.Applications import Applications
from views.pages.Tools import Tools


def test_page_constructs_without_error(qtbot, sample_settings):
    page = Applications(settings=sample_settings)
    qtbot.addWidget(page)
    assert page.page_id == PAGE_ID_APPLICATIONS


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
