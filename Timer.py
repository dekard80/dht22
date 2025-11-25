# create a timer

from time import time, sleep


class Timer:
    state = False
    time_interval = 0
    initial_time = 0
    cpu_save = False

    def __init__(self, ti, cpus=False):
        self.cpu_save = cpus
        self.time_interval = ti

    def start(self):
        self.initial_time = time()
        self.state = False

    def get_state(self):
        return self.state

    def run(self):
        if (self.initial_time + self.time_interval) < time():
            self.state = True
        # reduces CPU load
        if self.cpu_save:
            sleep(0.01)
