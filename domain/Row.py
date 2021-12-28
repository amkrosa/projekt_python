class Row:
    def __init__(self, data):
        self.__data = data

    def __iter__(self):
        return iter(self.__data)

    @property
    def values(self):
        return self.__data.items()

    def __getitem__(self, columnName: str):
        return self.__data[columnName]