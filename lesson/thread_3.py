import threading
import time
from threading import Thread


class PeriodicTimer(Thread):

    def __init__(self, interval):
        self._interval = interval
        self._flag = 0
        self._cd = threading.Condition()

    def start(self):
        t = threading.Thread(target=self.run)
        t.daemon = True
        t.start()

    def run(self):
        while True:
            time.sleep(self._interval)
            print('run --> {} {}'.format(self._flag, threading.current_thread().getName()))
            with self._cd:
                self._flag ^= 1
                self._cd.notify_all()

    def wait_tick(self):
        with self._cd:
            last_flag = self._flag

            while last_flag == self._flag:
                self._cd.wait()


def countdown(args):
    while args > 0:
        ptimer.wait_tick()
        print('down --> {} {}'.format(args, threading.current_thread().getName()))
        args -= 1


def coundup(args):
    n = 0
    while n < args:
        ptimer.wait_tick()
        print('up --> {} {}'.format(n, threading.current_thread().getName()))
        n += 1


ptimer = PeriodicTimer(5)
ptimer.start()

Thread(target=countdown, args=(6,)).start()
Thread(target=coundup, args=(3,)).start()
