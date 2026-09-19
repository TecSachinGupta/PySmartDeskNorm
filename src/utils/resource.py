from __future__ import annotations

from pathlib import Path


def resource_path(*parts: str) -> Path:
    project_root = Path(__file__).resolve().parent.parent
    return project_root / "resources" / Path(*parts)


def icon(name: str) -> Path:
    return resource_path("icons", f"{name}.svg" if not name.endswith(".svg") else name)
