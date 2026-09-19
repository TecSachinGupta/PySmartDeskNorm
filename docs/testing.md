# Testing

## Where a test goes

**A test lives at the path mirroring its subject in `src/` — never in a file named after the
session, date, or phase that produced it.**

```
src/views/components/Button.py   ->  tests/views/components/test_button.py
src/services/settings_service.py ->  tests/services/test_settings_service.py
src/configs/Themes.py            ->  tests/configs/test_themes.py
```

Source modules use PascalCase (`Button.py`, `TitleBar.py`); test modules use snake_case
(`test_button.py`, `test_title_bar.py`).

Only create a test file when you actually have a test for that module — don't add empty
placeholders for untested source files.

## Running

```bash
pytest -q                                   # everything
pytest -q tests/views/components            # one area
pytest -q tests/views/components/test_button.py
```

`pythonpath = ["src"]` in `pyproject.toml` means tests import as `from views.components.Button
import Button`, with no `src.` prefix and no need to run from inside `src/`.

## Fixtures

Shared setup belongs in `tests/conftest.py`, not copy-pasted per file:

- `qtbot` / `qapp` — provided by `pytest-qt`; never construct a `QApplication` by hand.
- `sample_settings` — a representative settings dict for page construction.
- `ini_controller` — a `SettingsController` backed by a temp `.ini` file.

**Always use `ini_controller` rather than a bare `SettingsController()`.** A default
controller writes to the real OS-level `QSettings` store (a plist on macOS), which leaks
state between runs and can clobber your actual app preferences.

## Qt gotchas worth knowing

- `QWidget.isVisible()` reflects the whole ancestor chain. To assert on a child's
  visibility, call `.show()` on the top-level widget first, or it is always `False`.
- Probing rendered pixels: `QPixmap(size)` is uninitialised memory. `pm.fill(sentinel)`
  before `widget.render(pm)`, or unpainted regions return garbage colours.

## Naming caveat

Test file basenames must stay unique across the whole tree. Without `__init__.py` files,
pytest imports test modules by basename, so two files both called `test_settings.py` in
different folders would collide at import time. `tests/views/pages/test_settings.py`
already exists — if `src/configs/Settings.py` ever needs tests, name that file
`tests/configs/test_settings_config.py` (or add `__init__.py` files throughout `tests/`).
