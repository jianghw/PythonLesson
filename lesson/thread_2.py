import threading
import time
from threading import Event, Thread


def countdown(count, event):
    while count > 0:
        count -= 1
        print('--- run {}'.format(threading.current_thread().getName()))
        time.sleep(1)
        # start_evt True
        if count == 2:
            event.set()


# 初始化的start_evt为False
start_evt = Event()
print('---> event {}'.format(threading.current_thread().getName()))
t = Thread(target=countdown, args=(5, start_evt,))
t.start()
print('---> start {}'.format(threading.current_thread().getName()))
start_evt.wait(1000)
print('---> wait {}'.format(threading.current_thread().getName()))
