# Component library

A catalog of every generic, reusable UI piece in `views/components/` — what each one is,
its actual constructor signature, and any signals it emits. For the *conventions* behind
these (theming, testing, where a new one belongs), see
[adding-a-component.md](adding-a-component.md).

Chrome widgets that are only ever used once by `AppShell` (`TitleBar`, `Sidebar`,
`CreditsBar`) live in `views/widgets/` instead and aren't covered here.

All components accept `name=None, parent=None` and set `objectName(name or "<default>")`
unless noted otherwise.

## Layout primitives

### `Row` / `Column`
`QFrame`s that lay out a fixed list of child widgets horizontally (`Row`) or vertically
(`Column`).
```python
Row(name=None, parent=None, widgets=None)      # QHBoxLayout
Column(name=None, parent=None, widgets=None)   # QVBoxLayout
```
- `widgets` is a plain list, added once at construction.
- `content_widgets` is a settable `Property(list)` — reassigning it clears and rebuilds
  the layout with the new widgets (not just bookkeeping).

### `Div`
Generic wrapper that turns an existing `QLayout` into a styleable `QFrame`.
```python
Div(content: QLayout, name=None, parent=None, color=None)
```
- `content` is positional and required — this is not a container you add children to
  later, you hand it a fully-built layout.
- `color`, if given, sets a flat inline background (one of the few components that still
  self-styles; see [theming.md](theming.md)).

## Buttons

### `Button`
The base clickable control, used directly or as the basis for window/category/theme
controls. Paints its own background/text/icon — no native `QPushButton` chrome.
```python
Button(
    name=None, parent=None, appParent=None,
    label=None, tooltipLabel=None,
    width=50, height=50, radius=8,
    variant=None, themeColors=None,          # theme-driven color resolution
    textColor="", backgroundColor="", backgroundHoverColor="", backgroundPressedColor="",
    leftIconPath=None, rightIconPath=None,
    iconColor="", iconHoverColor="", iconPressedColor="", iconActiveColor="",
    margin=None, isActive=False, isTabActive=False, isToggleActive=False,
)
```
- `variant`: `"primary"` / `"secondary"` / `"ghost"` / `"danger"`. When set, colors are
  resolved from `themeColors` (the theme's `colors` dict) via `_resolve_variant_colors`,
  with built-in fallbacks if a token is missing. Explicit color kwargs always win over
  the variant. A square `width`/`height` with `radius = width // 2` renders as a circle
  (see the title bar's window controls).
- `isActive=True` renders using the pressed color, for a persistent "selected" look
  (theme pickers, category filters).
- Builds a `Tooltip` lazily on first hover, only if `tooltipLabel` is set — a button with
  no tooltip text never creates one.
- Inherits `clicked`/`released` from `QPushButton`.

### `ActionButton`
A clickable card (icon + title + description) — the "quick action" tile pattern used on
the Dashboard.
```python
ActionButton(name=None, parent=None, icon_text="\u25cf", title="", description=None)
```
- Signal: `clicked()`.

## Toggles and tooltips

### `AnimatedToggle`
A `QCheckBox` subclass that paints and animates itself as an iOS-style sliding switch.
```python
AnimatedToggle(
    parent=None, bar_color=Qt.gray, checked_color="#00B0FF",
    handle_color=Qt.white, pulse_unchecked_color="#44999999", pulse_checked_color="#4400B0EE",
)
```
- Standard `QCheckBox` API (`isChecked()`, `setChecked()`, `stateChanged`). Reuse this —
  don't build a second toggle component.

### `Tooltip`
A drop-shadowed floating label. Normally you don't construct this directly — `Button`
manages its own.
```python
Tooltip(name=None, parent=None, backgroundColor=None, textColor=None, tooltipText=None)
```

## Cards

### `StatCard`
Icon + title + big value + optional description, for dashboard-style metrics.
```python
StatCard(name=None, parent=None, icon_text="\u25cf", title="", value="", description=None)
```
- `value_label` is exposed so callers can update the number later
  (`card.value_label.setText(...)`).

### `ActivityCard`
A titled list of `{"text": ..., "timestamp": ...}` rows.
```python
ActivityCard(name=None, parent=None, title="Recent Activity", entries=None)
```
- `entries` is rendered once at construction; re-construct the card to show new entries.

### `SectionCard`
Generic titled container — the "put this group of widgets in a card" primitive used to
wrap other components (e.g. a `Row` of buttons) with a heading.
```python
SectionCard(name=None, parent=None, title=None, content_widgets=None)
```

### `ToolCard`
A clickable card for a catalog entry (title + category + description).
```python
ToolCard(name=None, parent=None, tool_id="", title="", category="", description=None)
```
- Signal: `clicked(str)` — emits `tool_id`.
- Exposes `title_text` / `category` as plain attributes for client-side filtering (see
  the Tools page's search/category filter).

### `AppCard`
A tracked-application card: icon, name, one line of metadata, an Open action, and a
remove ("✕") action.
```python
AppCard(
    name=None, parent=None, app_id="", title="", icon=None, meta="",
    icon_size=28, themeColors=None,
)
```
- Signals: `open_requested(str)`, `remove_requested(str)` — both emit `app_id`.
- `icon` is a name resolved via `utils.resource.icon()`; falls back to a generic icon
  (`GENERIC_ICON = "component"`) if missing, so a card never renders with a blank icon.

## Inputs

### `SearchInput`
A `QLineEdit` preconfigured for search: placeholder text and a built-in clear button.
```python
SearchInput(name=None, parent=None, placeholder="Search...")
```
- Plain `QLineEdit` API (`text()`, `textChanged`) — wire `textChanged` to your own filter
  logic; there's no built-in search service.

### `TextInput`
A plain single-line `QLineEdit` for anything that isn't a search box.
```python
TextInput(name=None, parent=None, placeholder="", text="")
```

### `ComboBox`
A `QComboBox` preloaded with a flat list of string items.
```python
ComboBox(name=None, parent=None, items=None, current=None)
```
- `current`, if given, is matched by exact text (`findText`) and selected.

## Feedback

### `Toast`
A transient, self-hiding status label.
```python
Toast(name=None, parent=None, duration_ms=2000)
```
- Not shown at construction. Call `toast.show_message("...")` to display it; it hides
  itself automatically after `duration_ms`.

### `EmptyState`
Centered icon + title + optional description, for "nothing here yet" placeholders.
```python
EmptyState(name=None, parent=None, icon_text="\u2205", title="Nothing here", description=None)
```
- `icon_label` / `title_label` / `description_label` are exposed so callers can update
  the copy for different empty conditions (e.g. "no results" vs "nothing added yet" —
  see the Applications and Tools pages).

## Headers

### `PageHeader`
A page's title + optional subtitle + optional trailing action widgets, right-aligned.
```python
PageHeader(name=None, parent=None, title="", subtitle=None, actions=None)
```
- `actions` is a list of pre-built widgets (e.g. a `Button`) appended after a stretch.
