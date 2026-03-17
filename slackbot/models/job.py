import datetime

pid_count = 0

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

        self.next = datetime.datetime.now() + datetime.timedelta(seconds=start)

    def run(self):
        try:
            self.handler(*self.args, **self.kwargs)
        except Exception as e:
            raise

        self.run_count += 1
        if self.repeat != -1 and self.run_count >= self.repeat:
            return False
        self.next = datetime.datetime.now() + datetime.timedelta(seconds=self.interval)
        return True
