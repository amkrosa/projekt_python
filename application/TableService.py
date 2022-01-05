import uuid
from typing import Callable, Any, Dict

from model.Table import Table
from infrastructure.Repository import Repository
from model.column.Column import Column
from model.column.FloatColumn import FloatColumn
from model.column.IntegerColumn import IntegerColumn
from model.column.TextColumn import TextColumn


class TableService:
    def __init__(self, repository: Repository):
        self.__repository: Repository = repository

    def addTable(self, tableId, name, nameCallback=None, rowsCallback=None, refreshCallback=None, columns=None):
        table = Table(name, tableId)
        if nameCallback:
            table.setNameCallback(nameCallback)
        if rowsCallback is not None:
            table.setRowsCountCallback(rowsCallback)
        if columns is not None:
            [table.addColumn(TableService.createColumn(columnName, columnType)) for columnName, columnType in
             columns.items()]
        if refreshCallback is not None:
            table.addCallback(refreshCallback)
        self.__repository.add(table, tableId)

    def push(self, tableName, row):
        self.getTable(name=tableName).push(row)

    def pop(self, tableName, rowIndex):
        self.getTable(tableName).remove(rowIndex)

    def removeTable(self, tableId):
        self.__repository.remove(tableId)

    def getTables(self) -> Dict[Any, Table]:
        return self.__repository.repository

    def getTable(self, name) -> Table:
        for value in self.__repository.repository.values():
            if value.name == name:
                return value
        return None

    def getTableById(self, tableId):
        return self.__repository[tableId]

    def query(self, tableName, query: Callable[[Any], bool]) -> dict:
        return {i: row for i, row in self.getTable(tableName).rows.items() if query(row.get())}

    def getColumn(self, tableName, columnName) -> Column:
        return self.getTable(tableName)[columnName]

    def getColumns(self, tableName):
        return self.getTable(tableName).columns

    def addColumn(self, tableName, column):
        self.getTable(tableName).addColumn(column)

    def addColumns(self, tableName: str, columns: dict):
        table = self.getTable(tableName)
        [table.addColumn(TableService.createColumn(columnName, columnType)) for columnName, columnType in
         columns.items()]

    @classmethod
    def createColumn(cls, columnName, columnType):
        if columnType == "str":
            return TextColumn(columnName)
        elif columnType == "int":
            return IntegerColumn(columnName)
        elif columnType == "float":
            return FloatColumn(columnName)
        else:
            raise RuntimeError(f"Unexpected error has occured. Column type is: {columnType}")
