import json
from typing import Type, TypeVar, Union, Dict, Any

from lib.BaseObservable import BaseObservable
from model.Row import Row
from lib.Observable import Observable

C = TypeVar("C", bound="Column")


class Table(BaseObservable):
    """
    Class encompassing Table in application. Inherits BaseObservable to more easily bind it to UI.
    """
    def __init__(self, name, tableId):
        super().__init__()
        if self.__validateName(name):
            self.__name = name.strip()
        self.__tableId = tableId
        self.__columnDictionary: Dict[str, C] = dict()
        self.__name = Observable(self.__name, tableId)
        self.__rows = []
        self.__rowCount = Observable(len(self.__rows), tableId)

    @property
    def id(self):
        return self.__tableId

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
        return self.__rowCount.get()

    @property
    def rows(self):
        return {i+1: val for i, val in enumerate(self.__rows)}

    @property
    def json(self):
        return json.dumps(self.__rows)

    def push(self, row: dict):
        self.__verifyRow(row)
        castedRow = { key: self.columns[key].cast(value) for key, value in row.items() }
        self.__rows.append(Observable(Row(castedRow)))
        self.__rowCount.set(self.rowCount+1)
        self._doCallbacks()

    def remove(self, rowIndex):
        try:
            self.__rows.pop(rowIndex)
            self.__rowCount.set(self.rowCount - 1)
            self._doCallbacks()
        except Exception:
            raise ValueError("Invalid index")

    def setNameCallback(self, callback):
        self.__name.addCallback(callback)

    def setRowsCountCallback(self, callback):
        self.__rowCount.addCallback(callback)

    def get(self, name: str) -> C:
        return self.__columnDictionary[name]

    def __getitem__(self, name: str) -> C:
        return self.__columnDictionary[name]

    def addColumn(self, column: C):
        for row in self.__rows:
            row.get().addValue(column.name, None)
        self.__columnDictionary[column.name] = column
        self._doCallbacks()

    def __str__(self):
        str=""
        for name, col in self.columns.items():
            str+=col.__str__()
        return str

    def __verifyRow(self, row: Dict[str, Any]):
        """
        Validates row by checking if argument has keys that matches table columns and by checking row types in each
        column.
        """
        for col in self.columns.keys():
            if col not in row.keys():
                raise ValueError(f"Row should contain all table columns, does not have {col}")
        for colName, rowValue in row.items():
            val = self.columns[colName].cast(rowValue)
            if not isinstance(val, self[colName].type):
                raise TypeError(f"Must input matching value types. {colName} needs {self[colName].type}")

    def __validateName(self, name):
        """
        Validates if name is a string and does not consists only of whitespaces
        """
        if not isinstance(name, str):
            raise ValueError("Name must be a string")
        if len(name.strip()) == 0:
            raise ValueError("Name cannot consist only of whitespaces")
        return True

    def _doCallbacks(self, data=None):
        """
        Overrides BaseObservable method to allow for more elastic callback use
        """
        for func in self._callbacks:
            if data is None:
                func(self)
            else:
                func(self, data)