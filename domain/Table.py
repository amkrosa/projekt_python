from typing import Type, TypeVar, Union, Dict, Any

from domain.Row import Row
from lib.Observable import Observable

C = TypeVar("C", bound="Column")


class Table:
    def __init__(self, name, nameUuid):
        self.__columnDictionary: Dict[str, C] = dict()
        self.__name = Observable(name, nameUuid)
        self.__rows = []
        self.__rowCount = 0

    @property
    def name(self) -> str:
        return self.__name.get()

    @name.setter
    def name(self, name: str):
        self.__name.set(name)

    @property
    def columns(self):
        return self.__columnDictionary

    @property
    def rowCount(self):
        return len(self.__rows)

    @property
    def rows(self):
        return {i+1: val for i, val in enumerate(self.__rows)}

    def push(self, row: dict):
        self.__verifyRow(row)
        self.__rows.append(Observable(Row(row)))

    def setNameCallback(self, callback):
        self.__name.addCallback(callback)

    def get(self, name: str) -> C:
        return self.__columnDictionary[name]

    def __getitem__(self, name: str) -> C:
        return self.__columnDictionary[name]

    def addColumn(self, column: C):
        for row in self.__rows:
            row.get().addValue(column.name, None)
        self.__columnDictionary[column.name] = column

    def __str__(self):
        str=""
        for name, col in self.columns.items():
            str+=col.__str__()
        return str

    def __verifyRow(self, row: Dict[str, Any]):
        for col in self.columns.keys():
            if col not in row.keys():
                raise ValueError(f"Row should contain all table columns, does not have {col}")
        for colName, rowValue in row.items():
            if rowValue != None and not isinstance(rowValue, self[colName].type):
                raise TypeError(f"Must input matching value types. {colName} needs {self[colName].type}")