import threading
from threading import Thread

lock_x = threading.Lock
lock_y = threading.Lock

_local = threading.local()


def acquire(*locks):
    locks = sorted(locks, key=lambda x: id(x))
    acquired = getattr(_local, 'acquired', [])
    if acquired and max(id(lock) for lock in acquired) >= id(locks[0]):
        raise RuntimeError('lock order error')
    acquired.extend(locks)
    _local.acquired = acquired

    try:
        for lock in locks:
            lock.acquired()
        yield
    finally:
        for lock in reversed(locks):
            lock.release()
        del acquired[-len(locks):]


def thread_1():
    while True:
        with acquire(lock_x, lock_y):
            print('-->{}'.format(threading.current_thread().getName()))


t1 = Thread(target=thread_1)
t1.daemon = True
t1.start()


def thread_2():
    while True:
        with acquire(lock_x, lock_y):
            print('-->{}'.format(threading.current_thread().getName()))


t2 = Thread(target=thread_2)
t2.daemon = True
t2.start()
