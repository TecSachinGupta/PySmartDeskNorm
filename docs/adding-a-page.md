# Adding a page

Pages live in `views/pages/` and are wired into the app through `AppShell` — a page never
manages its own navigation or persistence directly.

## Steps

1. **Add a page id.** Open `constants/__init__.py` and add `PAGE_ID_<NAME> = "<name>"` to
   the list of page ids (and to `__all__`).
2. **Create the page class** in `views/pages/<Name>.py`:
   ```python
   from __future__ import annotations

   from PySide6.QtWidgets import QVBoxLayout, QWidget

   from constants import PAGE_ID_<NAME>
   from views.components.PageHeader import PageHeader


   class <Name>(QWidget):
       page_id = PAGE_ID_<NAME>

       def __init__(self, name=None, parent=None, settings=None):
           super().__init__(parent)
           self.setObjectName(name or "<name>Page")
           self.settings = settings or {}

           header = PageHeader(title="<Name>", subtitle="...")

           layout = QVBoxLayout(self)
           layout.setContentsMargins(24, 24, 24, 24)
           layout.setSpacing(16)
           layout.addWidget(header)
           layout.addStretch(1)
   ```
   Compose the body from existing `views/components/` pieces (`SectionCard`, `StatCard`,
   `ActionButton`, etc.) before reaching for a new component — see
   [adding-a-component.md](adding-a-component.md) if nothing fits.
3. **Register it in `AppShell`** (`views/containers/AppShell.py`): import the class and add
   `(PAGE_ID_<NAME>, <Name>(name="<name>Page", settings=self.settings))` to the `pages`
   list in `_register_pages()`. `NavigationService` and the `QStackedWidget` handle the
   rest.
4. **Add a sidebar entry** in `views/widgets/Sidebar.py`'s `self.items` list if the page
   should be reachable from navigation: `SidebarItem(PAGE_ID_<NAME>, "<Label>", icon_text="...")`.
   `SidebarItem` only emits a `clicked(page_id)` signal — it never imports a page class.
5. **If the page needs persistence or non-trivial logic**, add a `services/<x>_service.py`
   (wrapping the actual persistence/IO) and, only if the page's own widget logic needs
   mediation beyond simple service calls, a `controllers/<x>_controller.py` — see
   `services/settings_service.py` + `controllers/settings_controller.py` for the pattern.
   Pages should call a controller/service, never touch `QSettings` or files directly.
6. **Add a smoke test** in `tests/test_pages_smoke.py`: construct the page inside a
   `qtbot` fixture and assert `page.page_id == PAGE_ID_<NAME>`.

## Conventions to keep

- Pages accept `name=None, parent=None, settings=None` and store `self.settings`.
- Pages listen to component signals (e.g. a card's `clicked`); components never import
  pages.
- No global/singleton state — if two pieces need the same value, pass it down explicitly
  (see how `AppShell` threads `settings` and a `SettingsController` into pages).
