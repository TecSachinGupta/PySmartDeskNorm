import errno
import json
import os

class Settings(object):
    def __init__(self, *args, **kwargs):
        file_name = kwargs.get('settings', 'default')
        self.file_path = "resources/settings/{file_name}.json".format(file_name = file_name)
        if not os.path.isfile(self.file_path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_name)
        super(Settings, self).__init__()
        self.items = {}
        self.deserialize()
    
    def serialize(self):
        with open(self.file_path, "w", encoding='utf-8') as write:
            json.dump(self.items, write, indent=4)
    
    def deserialize(self):
        with open(self.settings_path, "r", encoding='utf-8') as reader:
            settings = json.loads(reader.read())
            self.items = settings