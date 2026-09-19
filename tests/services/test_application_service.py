from __future__ import annotations

from models.application import Application
from services.application_service import ApplicationService


def test_service_seeds_mock_applications():
    service = ApplicationService()
    assert service.count() > 0
    assert service.count() == len(service.list())


def test_add_prepends_and_emits_changed():
    service = ApplicationService(applications=[])
    seen = []
    service.changed.connect(lambda: seen.append(service.count()))

    added = service.add(name="Zed", icon="component")

    assert service.count() == 1
    assert service.list()[0].name == "Zed"
    assert added.app_id
    assert seen == [1]


def test_remove_drops_the_application_and_emits_changed():
    existing = [Application("keep", "Keep"), Application("drop", "Drop")]
    service = ApplicationService(applications=existing)
    seen = []
    service.changed.connect(lambda: seen.append(service.count()))

    service.remove("drop")

    assert [a.app_id for a in service.list()] == ["keep"]
    assert seen == [1]


def test_remove_unknown_id_is_a_no_op():
    service = ApplicationService(applications=[Application("keep", "Keep")])
    seen = []
    service.changed.connect(lambda: seen.append(1))

    service.remove("missing")

    assert service.count() == 1
    assert seen == []


def test_list_returns_a_copy_so_callers_cannot_mutate_the_store():
    service = ApplicationService(applications=[Application("a", "A")])
    service.list().clear()
    assert service.count() == 1
