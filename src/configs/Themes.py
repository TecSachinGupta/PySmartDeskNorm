import errno
import json
from pathlib import Path

from .Settings import Settings


class Themes:
    def __init__(self, *args, **kwargs):
        theme_name = Settings().items["theme"]
        file_name = kwargs.get("theme", theme_name)
        root_dir = Path(__file__).resolve().parent.parent
        self.file_path = root_dir / "resources" / "themes" / f"{file_name}.json"
        if not self.file_path.is_file():
            raise FileNotFoundError(errno.ENOENT, "No such file or directory", str(self.file_path))
        super().__init__()
        self.items = {}
        self.deserialize()

    def serialize(self):
        with open(self.file_path, "w", encoding="utf-8") as write:
            json.dump(self.items, write, indent=4)

    def deserialize(self):
        with open(self.file_path, encoding="utf-8") as reader:
            settings = json.loads(reader.read())
            self.items = settings

    def apply(self, app):
        colors = self.items.get("colors", {})
        spacing = self.items.get("spacing", {})
        typography = self.items.get("typography", {})
        radius = self.items.get("radius", {})
        controls = self.items.get("controls", {})

        window_bg = colors.get("backgroundColor", "#1b1e23")
        bg = colors.get("primaryBackgroundColor", "#2c313c")
        bg_alt = colors.get("secondaryBackgroundColor", "#21252d")
        text = colors.get("textPrimaryColor", "#dce1ec")
        text_muted = colors.get("textSecondaryColor", "#8a95aa")
        text_active = colors.get("textActiveColor", "#f5f6f9")
        accent = colors.get("accentColor", "#6c99f4")
        surface = colors.get("surfaceColor", "#343b48")

        body_font = typography.get("font_family", "Segoe UI")
        body_size = typography.get("body_size", 10)
        title_size = typography.get("title_size", 12)
        subtitle_size = typography.get("subtitle_size", 10)
        caption_size = typography.get("caption_size", 9)
        heading_size = typography.get("heading_size", title_size + 6)
        value_size = typography.get("value_size", title_size + 5)

        control_height = controls.get("height", 32)
        icon_size = controls.get("icon_size", 18)
        radius_value = radius.get("md", 10)
        radius_sm = radius.get("sm", 6)
        pad_md = spacing.get("md", 12)
        pad_sm = spacing.get("sm", 8)

        # Segoe UI is Windows-only; fall back so macOS/Linux render a real UI font.
        font_stack = f'"{body_font}", "SF Pro Text", "Helvetica Neue", "Inter", Arial, sans-serif'

        stylesheet = f"""
        QWidget {{
            background-color: {bg};
            color: {text};
            font-family: {font_stack};
            font-size: {body_size}pt;
        }}
        QLabel {{
            background-color: transparent;
        }}
        QWidget#appshell {{
            background-color: {window_bg};
        }}

        /* ---- Title bar ---- */
        QLabel#logoSlot {{
            background-color: {bg_alt};
        }}
        QWidget#titleBarRow {{
            background-color: {bg_alt};
        }}
        QLabel#titleLabel {{
            color: {text};
            font-size: {subtitle_size}pt;
            font-weight: 600;
            padding-left: {pad_sm}px;
        }}

        /* ---- Sidebar ---- */
        QWidget#sidebar {{
            background-color: {bg_alt};
        }}
        QWidget#sidebarItem {{
            background-color: transparent;
            border: 1px solid transparent;
            border-radius: {radius_value}px;
            color: {text_muted};
        }}
        QWidget#sidebarItem:hover {{
            background-color: {surface};
        }}
        QWidget#sidebarItem:hover QLabel {{
            color: {text};
        }}
        QWidget#sidebarItem[active="true"] {{
            background-color: {accent};
            border: 1px solid {accent};
        }}
        QWidget#sidebarItem[active="true"] QLabel {{
            color: {text_active};
        }}
        QLabel#sidebarItemIcon {{
            font-size: {icon_size}px;
            color: {text_muted};
        }}
        QLabel#sidebarItemLabel {{
            font-size: {caption_size}pt;
            color: {text_muted};
        }}

        /* ---- Page header ---- */
        QLabel#pageHeaderTitle {{
            font-size: {heading_size}pt;
            font-weight: 700;
            color: {text};
        }}
        QLabel#pageHeaderSubtitle {{
            font-size: {subtitle_size}pt;
            color: {text_muted};
        }}

        /* ---- Cards ---- */
        QFrame#sectionCard, QFrame#statCard, QFrame#activityCard,
        QFrame#toolCard, QFrame#actionButton, QFrame#appCard {{
            background-color: {surface};
            border: 1px solid transparent;
            border-radius: {radius_value}px;
        }}
        QFrame#actionButton:hover, QFrame#toolCard:hover, QFrame#appCard:hover {{
            border: 1px solid {accent};
        }}
        QLabel#appCardTitle {{
            font-weight: 600;
            color: {text};
        }}
        QLabel#appCardMeta {{
            color: {text_muted};
            font-size: {caption_size}pt;
        }}
        QLabel#statCardTitle, QLabel#statCardDescription {{
            color: {text_muted};
            font-size: {caption_size}pt;
        }}
        QLabel#statCardValue {{
            font-size: {value_size}pt;
            font-weight: 700;
            color: {text};
        }}
        QLabel#sectionCardTitle, QLabel#activityCardTitle {{
            font-size: {subtitle_size}pt;
            font-weight: 600;
            color: {text};
        }}
        QLabel#activityCardTimestamp {{
            color: {text_muted};
            font-size: {caption_size}pt;
        }}
        QLabel#actionButtonTitle, QLabel#toolCardTitle {{
            font-weight: 600;
            color: {text};
        }}
        QLabel#actionButtonDescription, QLabel#toolCardDescription {{
            color: {text_muted};
            font-size: {caption_size}pt;
        }}
        QLabel#toolCardCategory {{
            color: {accent};
            font-size: {caption_size}pt;
        }}

        /* ---- Controls ---- */
        QLineEdit, QComboBox {{
            background-color: {surface};
            border: 1px solid {bg_alt};
            border-radius: {radius_sm}px;
            padding: {pad_sm}px {pad_md}px;
            color: {text};
            min-height: {control_height}px;
        }}
        QLineEdit:focus, QComboBox:focus {{
            border: 1px solid {accent};
        }}
        QComboBox QAbstractItemView {{
            background-color: {surface};
            color: {text};
            selection-background-color: {accent};
            selection-color: {text_active};
        }}

        /* ---- Feedback ---- */
        QLabel#emptyStateIcon, QLabel#emptyStateDescription {{
            color: {text_muted};
        }}
        QLabel#emptyStateTitle {{
            font-size: {subtitle_size}pt;
            font-weight: 600;
            color: {text};
        }}
        QLabel#toast {{
            background-color: {accent};
            color: {text_active};
            border-radius: {radius_sm}px;
            padding: {pad_sm}px {pad_md}px;
        }}

        /* ---- Credits bar ---- */
        QWidget#creditsBar {{
            background-color: {bg_alt};
        }}
        QWidget#creditsBar QLabel {{
            color: {text_muted};
            font-size: {caption_size}pt;
        }}
        """
        app.setStyleSheet(stylesheet)
        return stylesheet
