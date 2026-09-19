import errno
import json
from pathlib import Path


class Settings:
    def __init__(self, *args, **kwargs):
        file_name = kwargs.get("settings", "default")
        root_dir = Path(__file__).resolve().parent.parent
        self.file_path = root_dir / "resources" / "settings" / f"{file_name}.json"
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
