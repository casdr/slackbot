import os
import json

class DataManager:
    def __init__(self, bot, file, default={}):
        self.bot = bot
        self.file_name = file
        self.bot.log.info("setting up datamanager for '%s'" % self.file_name)
        self.file = os.path.join(self.bot.state_file_base, '%s.json' % self.file_name)
        self.data = default

        self.bot.log.info("loading data file '%s'" % self.file_name)
        if os.path.isfile(self.file):
            with open(self.file) as f:
                self.bot.log.info("loading data for '%s'" % self.file_name)
                self.data = {**self.data, **json.load(f)}

    def set(self, data):
        self.data = data
        self.save()

    def save(self):
        self.bot.log.info("saving data file '%s'" % self.file_name)
        with open(self.file, 'w') as f:
            json.dump(self.data, f)