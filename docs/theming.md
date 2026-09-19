# Theming

The app's look is driven entirely by JSON token files under `resources/themes/` — no
component hardcodes colors, fonts, or spacing that should vary by theme.

## Choosing the active theme

`resources/settings/default.json` has a `"theme"` key (e.g. `"default"`) that names the
theme file to load. This can be overridden at runtime — see below.

## Token schema

Every file in `resources/themes/` (`default.json`, `bright.json`, `dracula.json`) follows
the same schema:

- `colors` — semantic color roles: `primaryBackgroundColor`, `secondaryBackgroundColor`,
  `surfaceColor` (card backgrounds), `textPrimaryColor`, `textSecondaryColor`,
  `accentColor`, `errorColor`, and related hover/pressed/active variants.
- `spacing` — a `xs`/`sm`/`md`/`lg`/`xl` scale (in px) for margins and padding.
- `typography` — `font_family`, and `title_size`/`subtitle_size`/`body_size`/`caption_size`.
- `radius` — corner radius scale (`sm`/`md`/`lg`/`xl`) for cards, buttons, and controls.
- `controls` — shared control sizing (`height`, `compact_height`, `icon_size`).
- `other_colors` — the original legacy hex palette kept for reference; not read by code.

`spacing`/`typography`/`radius`/`controls` are structural and intentionally identical
across all three theme files — a theme swap should only change the color palette, not
the layout rhythm.

## How a theme becomes a stylesheet

`configs/Themes.py`'s `Themes.apply(app)` reads the loaded theme's tokens and builds one
QSS stylesheet, then calls `app.setStyleSheet(...)` once. `app.py` calls this exactly once
at startup. No component should ever call `self.setStyleSheet(...)` on itself outside of
that — everything should be themeable through this single stylesheet, plus the
`Button` `variant`/`themeColors` pattern described in
[adding-a-component.md](adding-a-component.md) for widgets that need per-instance colors
(e.g. a `danger` vs `primary` button).

## Switching themes at runtime

The Settings page lets a user pick a theme from a `ComboBox`. That choice is persisted via
`SettingsService` (a thin wrapper over `QSettings`) so it survives an app restart —
`MainWindow` resolves `SettingsService().get_theme(default=...)` at startup, falling back
to the JSON default only if nothing has been persisted yet.

## Adding a new theme

1. Copy `resources/themes/default.json` to `resources/themes/<name>.json`.
2. Update `theme_name` and the `colors` block's hex values. Keep `spacing`/`typography`/
   `radius`/`controls` unless you specifically want different structural sizing.
3. That's it — `SettingsController.available_themes()` discovers theme files by scanning
   `resources/themes/*.json`, so the new theme automatically shows up in the Settings
   page's theme picker with no code changes.
