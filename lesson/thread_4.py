import threading


class SharedCounter:
    def __init__(self, init_value=0):
        self._value = init_value
        self._value_lock = threading.Lock()

    def incr(self, delta=1):
        with self._value_lock:
            self._value += delta

    def decr(self, delta=1):
        with self._value_lock:
            self._value -= delta
