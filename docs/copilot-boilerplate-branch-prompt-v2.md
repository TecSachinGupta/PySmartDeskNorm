# Copilot Prompt Pack v2 — PySmartDeskNorm `boilerplate` Branch

This **replaces** `copilot-boilerplate-branch-prompt.md`. It folds in the fuller dashboard/component-library scope from the ambitious spec you had reviewed, but mapped onto your **existing** `src/` structure instead of that spec's proposed `app/core/ui` reorganization, and corrected for your actual local environment.

**How to use it:** paste **Shared Context** once per Copilot session (or save as `.github/copilot-instructions.md`), then paste **one Phase at a time**. Run the app after each phase — several bugs here are only visible at runtime.

---

## Shared Context (paste first, every session)

You're building out the `boilerplate` branch of a PySide6 desktop app. Three decisions are final — don't revisit them:

1. **Folder structure stays as it is today.** Everything is organized under `src/`: `configs/` (Settings, Themes), `constants/`, `controllers/`, `models/`, `services/`, `utils/` (currently empty stubs, reserved), `resources/` (fonts, icons, images, `settings/default.json`, `themes/*.json`), and `views/{components, containers, pages, widgets}`. New work fills in these existing folders — do **not** introduce top-level `app/`, `core/`, or `ui/` folders.
2. **Documentation lives in `docs/` at the repo root** (new folder — create it in Phase 0). The root `README.md` stays short and points into `docs/` rather than growing into a long document itself.
3. **Environment: `venv` + `pyproject.toml`, Python 3.13, PySide6 6.11.2.** Not conda (`environment.yml` is being retired) and not Python 3.14 — 3.13 is what's actually installed locally (3.13.5), so that's the baseline to target and test against, regardless of what's newest upstream.

**Current real state of the code (verified by reading the files, not assumed):**

- `app.py` is a clean 16-line entry point — leave it that way.
- `MainWindow.render()` is a single `print(self.settings)` line — nothing is laid out yet.
- `TitleBar.__init__` sets its object name/parent and then just `pass`es.
- `AnimatedToggle` and `Tooltip` are correctly implemented — use them as the reference pattern, not things to change (except the one naming fix in Phase 1).
- `Row`, `Column`, `Button`, and `CreditsBar` each have a real bug (Phase 1).
- All four `views/*/__init__.py` files are empty.
- `resources/themes/default.json` currently defines only `colors` and a legacy `other_colors` hex palette (which is closer to genuine OneDark than the semantic `colors` block) — no spacing/typography/radius tokens exist yet.
- `resources/settings/default.json` already has `app_name`, `version`, `theme`, window `size`, `margins`, `paddings` — don't re-declare these elsewhere; read them once and expose what code needs.

**Constraints carried through every phase:**

- Components never import pages; pages listen to component signals, not the other way around.
- No database, auth, API backend, cloud integration, ORM, DI container, or microservices — this is a UI foundation only.
- No Redux-style global state — only share state where two or more components genuinely need the same value.
- Don't invent resolution logic for the `"auto"` placeholder color values.
- Prefer the smallest implementation that satisfies each phase; when a spec below suggests several near-identical classes (e.g. five button variants), a single component with a `variant` parameter is preferred over five subclasses, consistent with avoiding deep inheritance trees.

---

## Phase 0 — Environment migration, safety net, docs scaffold

- Delete `environment.yml`. Add `pyproject.toml` at repo root: `requires-python = ">=3.13"`, runtime dependency `PySide6==6.11.2`, a `dev` extra with `pytest`, `pytest-qt`, `ruff`. Configure `[tool.pytest.ini_options]` with `pythonpath = ["src"]` so tests can import `views`/`configs`/etc. without needing to run from inside `src/`. Given the current flat layout under `src/` has no top-level package namespace, don't restructure existing imports just to make an editable install nicer — a plain dependency manifest installed via `pip install -e ".[dev]"` (or `pip install ".[dev]"` if editable mode fights the layout) is enough.
- Update `README.md`'s setup section: `python -m venv .venv` → activate → `python -m pip install --upgrade pip` → `pip install -e ".[dev]"`. `.venv` is already covered by the existing `.gitignore` — no change needed there.
- Create `docs/` with a short `docs/README.md` explaining what will live there (architecture, per-feature guides added as later phases land).
- Add one smoke test per existing component/widget (`Row`, `Column`, `Button`, `Tooltip`, `AnimatedToggle`, `TitleBar`, `CreditsBar`), each constructing it inside a `qtbot` fixture and asserting no exception.

**Done when:** `pytest` runs under the new `.venv`. Expect `Row`, `Column`, `Button`, and `CreditsBar` to fail — that's the correct starting point.

---

## Phase 1 — Fix the four existing bugs

1. **`views/components/Tooltip.py`** — constructor parameter is spelled `toottipText`; `views/components/Button.py` calls it with the correctly-spelled `tooltipText=tooltipLabel`, so every `Button` construction throws `TypeError`. Rename the parameter to `tooltipText`.
2. **`views/components/Row.py`** and **`views/components/Column.py`** — identical bug in both: the `content_widgets` property's getter and setter each reference `self.content_widgets`, i.e. call themselves — infinite recursion on construction. Back both with a distinct `self._content_widgets` attribute, matching the pattern `AnimatedToggle._handle_position` already gets right. Fix the `__init__` line in each that currently reads `self.content_widgets` before anything is assigned.
3. **`views/components/Button.py`** — `isTabActive` and `isToggleActive` are both decorated `@isActive.setter` instead of their own property's setter. Fix each decorator.
4. **`views/widgets/CreditsBar.py`** — `__init__` builds `self.frameLayout` but never calls `self.setLayout(self.frameLayout)`, so nothing displays. `render()` references six `self._*` attributes (`_radius`, `_bg_two`, `_text_size`, `_font_family`, `_text_description_color`, `_padding`) that are never set anywhere — it will raise `AttributeError` if called. Decide whether the theme-driven styling belongs in `__init__` alongside the real `setLayout` call or stays a separate method that actually sets those attributes first; either way, remove the current broken body.

**Done when:** the Phase 0 smoke tests for these four go green.

---

## Phase 2 — Harden config path resolution

- `configs/Settings.py` and `configs/Themes.py` build their JSON path as a bare relative string (`"resources/settings/{file_name}.json"`), which only works because of the `cd src/` convention. Resolve both relative to the package's own file location (`Path(__file__).resolve().parent...`) instead.

**Done when:** `Settings()`/`Themes()` load correctly regardless of the process's working directory.

---

## Phase 3 — Core infra: constants, logging, resource resolution

- `constants/` gets symbolic, code-level constants that aren't already in `resources/settings/default.json` — page IDs, signal names, and similar — not a re-declaration of `app_name`/`version`/`size`, which already live in settings.
- `utils/` gets a `logging_config.py` (one-time `logging` setup, module-level loggers everywhere else — no `print()` in application code) and a small resource-resolution helper (e.g. `icon(name)`) that any component can call instead of building its own path, fixing the same CWD-fragility class as Phase 2 for icon/image lookups.

**Done when:** there's a single source for logging setup and a single function for resolving a resource path, and neither depends on the current working directory.

---

## Phase 4 — Chrome: `TitleBar`, `Sidebar`, `AppShell`

- Build out `TitleBar`: a title label reading `settings["app_name"]`, minimize/maximize/close buttons built from `Button`, and drag-to-move handling (`resources/settings/default.json` already has `"custom_title_bar": true`, implying a frameless main window). Compose its internal layout with `Row`/`Div`, not a raw `QHBoxLayout` directly on the class.
- Add `Sidebar` and `SidebarItem` to `views/widgets/` (alongside `TitleBar`/`CreditsBar` — this is where chrome/navigation elements already live). Each item: icon, label, active/hover state, a click signal, optional badge. `SidebarItem` must not import any page class — it only emits signals.
- Add `AppShell` to `views/containers/` (alongside `MainWindow`), composing `TitleBar` + `Sidebar` + a content area (a `QStackedWidget`, empty for now — pages arrive in Phase 6).
- `MainWindow` becomes thin: construct an `AppShell`, set it as the central widget, nothing else.

**Done when:** `python -B app.py` opens a real frameless window with a title bar and a sidebar, even though the content area is still empty.

---

## Phase 5 — Theme manager and design tokens

- `resources/themes/default.json` only has `colors` and `other_colors` today. Add `spacing`, `typography` (font family/sizes/weights), `radius`, and control-height tokens as new top-level keys — extend the schema, don't duplicate what's already in `resources/settings/default.json`'s `font`/`margins`/`paddings`.
- Add an `apply(app)` method to the existing `Themes` class (`configs/Themes.py`) that builds one global QSS stylesheet from the loaded tokens and calls `app.setStyleSheet(...)` once, from `app.py`. No component should call `setStyleSheet()` on itself once this lands — everything pulls from the applied theme.
- Add `docs/theming.md` documenting the token schema and how to add a new theme file.

**Done when:** swapping `resources/settings/default.json`'s `"theme"` value to a different theme file changes the whole app's appearance with no code changes.

---

## Phase 6 — Dashboard page and navigation

- Add to `views/components/`: `PageHeader` (title + subtitle + optional actions), `StatCard` (icon, title, value, description), `ActionButton` (icon, title, description, click signal), `ActivityCard` (a small activity list with timestamps), `SectionCard` (generic container for grouped content). If the component count here has gotten unwieldy, this is a reasonable point to split `views/components/` into subfolders (`cards/`, `buttons/`, `feedback/`) — that's still "the existing folder," just organized within it.
- Add `views/pages/Dashboard.py`, composed from the components above.
- Add `services/navigation_service.py`: Qt-signal-based, pages registered by id, a `navigate(page_id)` method that swaps the `AppShell`'s `QStackedWidget`. Avoid an `if/elif` chain — a small dict/list registry is enough for now.
- Wire `Sidebar` clicks → `navigation_service.navigate(...)` → visible page change.

**Done when:** `python -B app.py` opens the app directly into a working Dashboard page reachable from the sidebar.

---

## Phase 7 — Remaining pages

- **Applications** (`views/pages/Applications.py`): a few demonstration entries using `SectionCard`/`ActionButton` — these can be illustrative placeholders, not real functionality.
- **Tools** (`views/pages/Tools.py`): a `SearchInput` + a `ToolCard` component + a simple category filter, demonstrating the pattern for a future tool catalogue.
- **Settings** (`views/pages/Settings.py`) + `services/settings_service.py`: the page never touches persistence directly — it calls the service, which wraps `QSettings`. Cover at least theme selection and one other preference.
- **About** (`views/pages/About.py`): app name/version/description pulled from `constants`/`resources/settings/default.json`, not hard-coded again.
- Add a `controllers/` entry only where a page's own logic genuinely needs one (e.g. `controllers/settings_controller.py` mediating between the Settings page's widgets and `settings_service`) — not for pages simple enough to not need it.

**Done when:** all five pages (Dashboard, Applications, Tools, Settings, About) are reachable from the sidebar and Settings changes persist across a restart.

---

## Phase 8 — Round out the component library

- **Buttons:** rather than five separate button classes, extend the existing `Button` with a `variant` parameter (`primary`/`secondary`/`ghost`/`danger`) reading colors from the theme tokens — same visual outcomes, one class instead of five.
- **Inputs:** `TextInput`, `SearchInput`, `ComboBox` in `views/components/`. `Toggle` already exists as `AnimatedToggle` — reuse it, don't rebuild it.
- **Feedback:** add `Toast`, `LoadingState`, `ErrorState`, `EmptyState` only as the pages from Phase 7 actually need them (e.g. `EmptyState` when Applications/Tools has nothing to show) rather than building all four speculatively.

**Done when:** every input/feedback component added is actually used by at least one page — none exist purely for the sake of completeness.

---

## Phase 9 — Tests, docs, and optional tooling polish

- Expand tests: one per page (constructs without error), one per service (`navigation_service`, `settings_service` round-trips).
- Add `docs/adding-a-page.md` and `docs/adding-a-component.md`, written now that the patterns are proven, plus whatever `docs/theming.md` from Phase 5 still needs.
- Add `ruff` configuration to `pyproject.toml`; `ruff check .` and `ruff format .` clean.
- Optional, once the above is solid: a GitHub Actions workflow (checkout → set up Python 3.13 → install → ruff → pytest) and a VS Code `settings.json` pointing at `.venv`. Treat these as polish after the app itself works, not a blocker before it does.

**Done when:** a new contributor can read `docs/` and add a page or component without reading `AppShell`'s internals first.

---

## Guardrails for Copilot

- One phase per session; run the app and look at it after each — Qt failures are often silent (nothing crashes, a widget is just invisible or unstyled).
- Fix Phase 1's bugs using `AnimatedToggle`'s existing correct pattern; don't introduce a third convention for backing properties.
- Stay inside the existing `src/` folders. `docs/` at root is the one new top-level folder to create.
- If a phase seems to need touching a file outside its stated scope, stop and say so rather than quietly expanding the diff.
