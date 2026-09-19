from constants import PAGE_ID_DASHBOARD
from models.application import Application
from services.application_service import ApplicationService
from views.pages.Dashboard import Dashboard


def test_page_constructs_without_error(qtbot, sample_settings):
    page = Dashboard(settings=sample_settings)
    qtbot.addWidget(page)
    assert page.page_id == PAGE_ID_DASHBOARD


def test_dashboard_page_builds(qtbot):
    dashboard = Dashboard(settings={"app_name": "PySmartDeskNorm"})
    qtbot.addWidget(dashboard)
    assert dashboard.page_id == PAGE_ID_DASHBOARD


def test_apps_tracked_stat_reads_from_the_service_and_updates(qtbot):
    """The stat must reflect the shared service, not a hardcoded number."""
    service = ApplicationService(applications=[Application("a", "Alpha")])
    dashboard = Dashboard(settings={}, application_service=service)
    qtbot.addWidget(dashboard)

    assert dashboard.apps_tracked_card.value_label.text() == "1"

    service.add(name="Beta")
    assert dashboard.apps_tracked_card.value_label.text() == "2"

    service.remove("a")
    assert dashboard.apps_tracked_card.value_label.text() == "1"


def test_add_application_action_emits_a_request(qtbot):
    dashboard = Dashboard(settings={})
    qtbot.addWidget(dashboard)

    seen = []
    dashboard.add_application_requested.connect(lambda: seen.append(True))

    dashboard.add_application_button.clicked.emit()

    assert seen == [True]
