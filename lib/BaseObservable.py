import abc


class BaseObservable:
    """
    Base class for implementing easier binding between models and UI. Stores dictionary with functions as keys, which are
    then executed after specified actions (for example editing a dictionary).
    """
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
