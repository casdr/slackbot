import os
import json
import tempfile


class DataManager:
    def __init__(self, bot, file, default=None):
        self.bot = bot
        self.file_name = file
        self.bot.log.info(f"setting up datamanager for '{self.file_name}'")
        self.file = os.path.join(self.bot.state_file_base, f'{self.file_name}.json')
        self.data = default or {}
        self._dirty = False

        if os.path.isfile(self.file):
            self.bot.log.info(f"loading data for '{self.file_name}'")
            with open(self.file) as f:
                self.data = {**self.data, **json.load(f)}

    def mark_dirty(self):
        self._dirty = True

    def save(self, force=False):
        if not force and not self._dirty:
            return
        self.bot.log.info(f"saving data file '{self.file_name}'")
        dir_name = os.path.dirname(self.file)
        fd, tmp_path = tempfile.mkstemp(dir=dir_name, suffix='.tmp')
        try:
            with os.fdopen(fd, 'w') as f:
                json.dump(self.data, f)
            os.replace(tmp_path, self.file)
        except BaseException:
            os.unlink(tmp_path)
            raise
        self._dirty = False

    def set(self, data):
        self.data = data
        self._dirty = True
        self.save(force=True)
