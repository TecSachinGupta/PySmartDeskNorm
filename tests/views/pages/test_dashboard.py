from constants import PAGE_ID_DASHBOARD
from views.pages.Dashboard import Dashboard


def test_page_constructs_without_error(qtbot, sample_settings):
    page = Dashboard(settings=sample_settings)
    qtbot.addWidget(page)
    assert page.page_id == PAGE_ID_DASHBOARD


def test_dashboard_page_builds(qtbot):
    dashboard = Dashboard(settings={"app_name": "PySmartDeskNorm"})
    qtbot.addWidget(dashboard)
    assert dashboard.page_id == PAGE_ID_DASHBOARD
