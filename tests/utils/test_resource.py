from pathlib import Path

from utils.resource import icon, resource_path


def test_resource_path_is_cwd_safe(monkeypatch):
    monkeypatch.chdir(Path("/tmp"))
    resolved = resource_path("icons/home.svg")
    assert resolved.is_file()
    assert resolved.name == "home.svg"
    assert icon("home").is_file()
