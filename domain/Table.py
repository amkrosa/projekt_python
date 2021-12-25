from typing import Type, TypeVar, Union, Dict

C = TypeVar("C", bound="Column")


class Table:
    def __init__(self, name):
        self.__columnDictionary: Dict[str, C] = dict()
        self.__name = name

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str):
        self.__name = name

    def __getitem__(self, item: str) -> C:
        return self.__columnDictionary[item]

    def addColumn(self, column: C):
        self.__columnDictionary[column.name] = column