class Observable:
    def __init__(self, initialValue=None, uuid=None):
        self.uuid = uuid
        self.data = initialValue
        self.callbacks = {}

    def addCallback(self, func):
        self.callbacks[func] = 1

    def delCallback(self, func):
        del self.callbacks[func]

    def _docallbacks(self):
        for func in self.callbacks:
            if self.uuid is None:
                func(data=self.data)
            else:
                func(data=self.data, uuid=self.uuid)

    def set(self, data):
        self.data = data
        self._docallbacks()

    def get(self):
        return self.data

    def unset(self):
        self.data = None

    def __get__(self, instance, owner):
        return self.data

    def __set__(self, instance, value):
        self.data = value
        self._docallbacks()