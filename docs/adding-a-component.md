# Adding a component

`views/components/` holds small, reusable UI primitives (buttons, cards, inputs,
feedback). `views/widgets/` holds larger composed chrome pieces (`TitleBar`, `Sidebar`,
`CreditsBar`) that are typically only used once, by `AppShell`. Start in `components/`
unless you're building something like a new piece of app chrome.

## Before adding a new component

Check whether an existing component already does the job with different content:
`SectionCard`, `StatCard`, `ActionButton`, `ActivityCard`, `PageHeader` cover most
"card with text" needs. A `variant` parameter on an existing component (see `Button`) is
preferred over a near-duplicate class.

## Steps

1. **Create `views/components/<Name>.py`:**
   ```python
   from __future__ import annotations

   from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


   class <Name>(QWidget):
       def __init__(self, name=None, parent=None, ...):
           super().__init__(parent)
           self.setObjectName(name or "<name>")
           ...
   ```
   - Constructor kwargs: `name=None, parent=None`, then whatever content the component
     needs. Set `self.setObjectName(name or "<default>")` so QSS in `Themes.apply()` can
     target it by object name.
   - If the component emits events, use a Qt `Signal` (e.g. `clicked = Signal(str)`) —
     don't accept callback functions.
2. **Make it theme-aware, not self-styled.** Don't call `self.setStyleSheet(...)` with
   hardcoded colors. Either:
   - Rely on the global stylesheet from `Themes.apply()` by using a recognizable
     `objectName()` and adding a rule for it in `configs/Themes.py`, or
   - Accept a `themeColors: dict | None` param and resolve colors from it with a sensible
     fallback, the way `Button`'s `variant`/`themeColors` does (see
     `views/components/Button.py`'s `_resolve_variant_colors`).
3. **Add a smoke test** in `tests/test_smoke_components.py` (or a dedicated test file for
   anything with real logic — see `tests/test_phase8_components.py` for examples):
   construct it inside a `qtbot` fixture and assert no exception.
4. **Only add it if a page actually uses it.** Don't build input/feedback components
   speculatively — wire the component into the page that needs it in the same change.

## Testing pattern

```python
def test_<name>_smoke(qtbot):
    widget = <Name>(...)
    qtbot.addWidget(widget)
    assert widget is not None
```

For components with visible state changes (filters, toggles, active/selected styling),
call `widget.show()` before asserting on `isVisible()` — `QWidget.isVisible()` reflects
the whole ancestor chain, not just the widget's own `setVisible()` call.
