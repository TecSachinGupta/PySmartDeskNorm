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

        bg = colors.get("primaryBackgroundColor", "#2c313c")
        bg_alt = colors.get("secondaryBackgroundColor", "#21252d")
        text = colors.get("textPrimaryColor", "#dce1ec")
        accent = colors.get("accentColor", "#6c99f4")
        surface = colors.get("surfaceColor", "#343b48")
        body_font = typography.get("font_family", "Segoe UI")
        body_size = typography.get("body_size", 10)
        title_size = typography.get("title_size", 12)
        control_height = controls.get("height", 32)
        radius_value = radius.get("md", 10)
        padding_x = spacing.get("md", 12)
        padding_y = spacing.get("sm", 8)

        stylesheet = f"""
        QWidget {{
            background-color: {bg};
            color: {text};
            font-family: "{body_font}";
            font-size: {body_size}pt;
        }}
        QWidget#sidebar {{
            background-color: {bg_alt};
        }}
        QWidget#sidebarItem {{
            border-radius: {radius_value}px;
            padding: {padding_y}px {padding_x}px;
        }}
        QWidget#titleBarRow {{
            background-color: {bg_alt};
        }}
        QLabel#titleLabel {{
            font-size: {title_size}pt;
            font-weight: 600;
        }}
        QPushButton {{
            min-height: {control_height}px;
            border-radius: {radius_value}px;
        }}
        QFrame#sectionCard, QFrame#statCard, QFrame#activityCard, QFrame#toolCard, QFrame#actionButton {{
            background-color: {surface};
            border-radius: {radius_value}px;
        }}
        QFrame#actionButton:hover, QFrame#toolCard:hover {{
            border: 1px solid {accent};
        }}
        """
        app.setStyleSheet(stylesheet)
        return stylesheet
