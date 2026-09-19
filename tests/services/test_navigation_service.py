from constants import PAGE_ID_APPLICATIONS, PAGE_ID_DASHBOARD
from services.navigation_service import NavigationService


def test_navigation_service_navigates_between_registered_pages():
    service = NavigationService()
    seen = []
    service.page_changed.connect(seen.append)

    service.register_page(PAGE_ID_DASHBOARD, object())
    service.navigate(PAGE_ID_DASHBOARD)
    service.navigate(PAGE_ID_DASHBOARD)  # same page again: no duplicate emit
    service.navigate(PAGE_ID_APPLICATIONS)  # unregistered: no-op

    assert seen == [PAGE_ID_DASHBOARD]
    assert service.current_page_id == PAGE_ID_DASHBOARD


def test_navigation_service_registers_and_reports_widgets():
    service = NavigationService()
    widget = object()
    service.register_page("home", widget)

    assert service.widget_for("home") is widget
    assert service.widget_for("missing") is None
    assert service.current_page_id is None

    service.navigate("home")
    assert service.current_page_id == "home"


def test_navigation_service_ignores_unregistered_and_duplicate_navigation():
    service = NavigationService()
    seen = []
    service.page_changed.connect(seen.append)
    service.register_page("home", object())

    service.navigate("unregistered")
    service.navigate("home")
    service.navigate("home")

    assert seen == ["home"]
