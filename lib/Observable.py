class Observable:
    def __init__(self, initialValue=None, uuid=None):
        self.uuid = uuid
        self.data = initialValue
        self.callbacks = {}

    def addCallback(self, func):
        self.callbacks[func] = 1

    def delCallback(self, func):
        del self.callback[func]

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