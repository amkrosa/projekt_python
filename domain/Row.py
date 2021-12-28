class Row:
    def __init__(self, data):
        self.__data = data

    def __getitem__(self, columnName: str):
        return self.__data[columnName]