# PySmartDeskNorm: A Python PySide Boilerplate
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
![GitHub repo size]

# Description
PySmartDeskNorm is a PySide6 boilerplate for building a themeable Python desktop
application: a frameless custom title bar, sidebar navigation, a small reusable
component library, and a working set of pages (Dashboard, Applications, Tools,
Settings, About).

# Features
 - Frameless window with a custom title bar and sidebar navigation
 - Live theming — switch themes from the Settings page, no restart required
 - Preferences persisted via `QSettings` (theme, credits message, credits bar visibility)
 - A small app-tracking Dashboard/Applications pair sharing one data source
 - A reusable component library: button variants, cards, inputs, and feedback components

# Screenshots

Not committed to the repo yet — run the app locally (see Getting Started below) to see
the current UI.

# Built With
 - Python >= 3.13 ![Python](https://img.shields.io/badge/-Python-1e415e?logo=python&style=flat-square)
 - PySide6 == 6.11.2 ![Python](https://img.shields.io/badge/-PySide6-1e415e?logo=PySide&style=flat-square)

# Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Installing
1. Clone this PySmartDeskNorm repository.
   ```bash
   git clone https://github.com/TecSachinGupta/PySmartDeskNorm
   ```
2. Create and activate a virtual environment.
   ```bash
   cd PySmartDeskNorm
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Install the project and dev dependencies.
   ```bash
   python -m pip install --upgrade pip
   pip install -e '.[dev]'
   ```
4. Run the app from the project root.
   ```bash
   python -B src/app.py
   ```

## Testing and linting
```bash
pytest -q
ruff check .
ruff format .
```

## Structure
```
.
│
├─── docs                 # architecture notes and contributor guides — start here
├─── src
│    ├─── configs         # Settings/Themes loaders
│    ├─── constants       # page ids, signal names
│    ├─── controllers     # mediates between a page's widgets and its service
│    ├─── models          # plain data classes (e.g. Application)
│    ├─── resources       # fonts, icons, images, settings/themes json
│    ├─── services        # navigation, settings, and application tracking
│    ├─── utils           # logging setup, resource-path resolution
│    └─── views
│         ├─── components # reusable UI primitives (Button, Row, StatCard, ...)
│         ├─── containers # MainWindow, AppShell
│         ├─── pages      # Dashboard, Applications, Tools, Settings, About
│         └─── widgets    # app chrome: TitleBar, Sidebar, CreditsBar
└─── tests                # mirrors src/, one test module per source module
```

## Process Flow

![Layout](src/resources/others/layout.svg)


## Documentation

See [docs/](docs/README.md) for the full set of guides:
 - [docs/theming.md](docs/theming.md) — the token schema and how to add a new theme
 - [docs/components.md](docs/components.md) — catalog of every generic UI component
 - [docs/adding-a-page.md](docs/adding-a-page.md) — wiring a new page into the app
 - [docs/adding-a-component.md](docs/adding-a-component.md) — component conventions
 - [docs/testing.md](docs/testing.md) — where tests live and shared fixtures


# Credits
 - [PyOneDark](https://github.com/Wanderson-Magalhaes/PyOneDark_Qt_Widgets_Modern_GUI/) by WANDERSON M.PIMENTA: Repository for QT Modern UI.
 - [Animating custom widgets with QPropertyAnimation](https://www.pythonguis.com/tutorials/pyside6-animated-widgets/) by Salem Al Bream: Blog on creting the Animated Toggle Button



[contributors-shield]: https://img.shields.io/github/contributors/TecSachinGupta/PySmartDeskNorm.svg?style=for-the-badge
[contributors-url]: https://github.com/TecSachinGupta/PySmartDeskNorm/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/TecSachinGupta/PySmartDeskNorm.svg?style=for-the-badge
[forks-url]: https://github.com/TecSachinGupta/PySmartDeskNorm/network/members
[stars-shield]: https://img.shields.io/github/stars/TecSachinGupta/PySmartDeskNorm.svg?style=for-the-badge
[stars-url]: https://github.com/TecSachinGupta/PySmartDeskNorm/stargazers
[issues-shield]: https://img.shields.io/github/issues/TecSachinGupta/PySmartDeskNorm.svg?style=for-the-badge
[issues-url]: https://github.com/TecSachinGupta/PySmartDeskNorm/issues
[license-shield]: https://img.shields.io/github/license/TecSachinGupta/PySmartDeskNorm.svg?style=for-the-badge
[license-url]: https://github.com/TecSachinGupta/PySmartDeskNorm/blob/master/LICENSE
[GitHub repo size]: https://img.shields.io/github/repo-size/TecSachinGupta/PySmartDeskNorm?style=for-the-badge