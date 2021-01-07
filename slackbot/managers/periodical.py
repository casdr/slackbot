import datetime
import threading
import types
import re
import time

pid_count = 0

class PeriodicalManager:
    def __init__(self, bot):
        self.bot = bot
        self.jobs = []
    
    def add_job(self, job):
        pass

class PeriodicalThread(threading.Thread):
    def __init__(self, bot, pm):
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
                        pass
                except:
                    pass
            time.sleep(1)
        self.bot.log.info('stopped periodical loop')
    
    def kill(self):
        self.bot.log.info('stopping periodical loop')
        self.killed = True

    


class Job:
    def __init__(self, start, interval, repeat, handler, *args, **kwargs):
        global pid_count
        pid_count += 1
        self.pid = pid_count
        self.run_count = 0

        self.handler = handler
        self.args = args
        self.kwargs = kwargs

        self.repeat = repeat
        self.interval = interval

        self.next = datetime.timedelta(seconds=start)
    
    def id(self):
        return self.pid
    
    def run(self):
        try:
            self.handler(*self.args, **self.kwargs)
        except:
            pass
    
        self.run_count += 1
        if self.repeat != -1 and self.run_count >= self.repeat:
            return False
        self.next = datetime.timedelta(seconds=self.interval)
        return True