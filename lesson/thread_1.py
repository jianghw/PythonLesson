import random
import time
from queue import Queue
from threading import Thread

q = Queue()
_sentinel = object()


def consumer(q_in):
    while True:
        data = q_in.get()
        print('consume --> {}'.format(data))
        if data is _sentinel:
            q_in.put(_sentinel)
            break


t1 = Thread(target=consumer, args=(q,))


def producer(q_out):
    n = 10
    while n:
        time.sleep(1)
        data = random.randint(0, 10)
        print('produce --> {}'.format(data))
        q_out.put(data)
        n -= 1
    q_out.put(_sentinel)
    pass


t2 = Thread(target=producer, args=(q,))
t1.start()
t2.start()
