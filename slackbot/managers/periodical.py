import datetime
import threading
import time
from ..models.job import Job


class PeriodicalManager:
    def __init__(self, bot):
        self.bot = bot
        self.jobs = []

    def add_job(self, job):
        self.jobs.append(job)


class PeriodicalThread(threading.Thread):
    def __init__(self, bot, pm):
        super().__init__()
        self.pm = pm
        self.bot = bot
        self.killed = False

    def run(self):
        self.bot.log.info('starting periodical loop')
        while not self.killed:
            now = datetime.datetime.now()
            for job in self.pm.jobs:
                if job.next > now:
                    continue
                try:
                    keep = job.run()
                    if not keep:
                        self.pm.jobs.remove(job)
                except Exception as e:
                    self.bot.log.error(f"job {job.pid} failed: {e}")
            time.sleep(1)
        self.bot.log.info('stopped periodical loop')

    def kill(self):
        self.bot.log.info('stopping periodical loop')
        self.killed = True
