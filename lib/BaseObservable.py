import abc


class BaseObservable:
    def __init__(self):
        self._callbacks = {}

    def addCallback(self, callback):
        self._callbacks[callback] = 1

    def _doCallbacks(self, data=None):
        for func in self._callbacks:
            if data is None:
                func()
            else:
                func(data)
