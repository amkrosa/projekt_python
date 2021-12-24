import Column

class Table:
    def __init__(self, name):
        self.__columnDictionary: dict[str, Column] = dict()
        self.__name = name

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name

    def __getitem__(self, item: str):
        return self.__columnDictionary[item].getData()