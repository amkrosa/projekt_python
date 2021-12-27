from typing import Type, TypeVar, Union, Dict

from lib.Observable import Observable

C = TypeVar("C", bound="Column")


class Table:
    def __init__(self, name, nameUuid):
        self.__columnDictionary: Dict[str, C] = dict()
        self.__name = Observable(name, nameUuid)

    @property
    def name(self) -> str:
        return self.__name.get()

    @name.setter
    def name(self, name: str):
        self.__name.set(name)

    def setNameCallback(self, callback):
        self.__name.addCallback(callback)

    def get(self, name: str) -> C:
        return self.__columnDictionary[name]

    def __getitem__(self, name: str) -> C:
        return self.__columnDictionary[name]

    def addColumn(self, column: C):
        self.__columnDictionary[column.name] = column