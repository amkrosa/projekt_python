from typing import List, Tuple, Callable, Any

from application.TableService import TableService
from domain.column.Column import Column
from infrastructure.Repository import Repository


class ColumnService:
    def __init__(self, repository: Repository, tableService: TableService):
        self.__repository = repository
        self.__tableService = tableService

    def getColumn(self, tableName, columnName) -> Column:
        return self.__tableService.getTable(tableName)[columnName]

    def addColumn(self, tableName, columnName):
        self.__tableService.getTable(tableName).addColumn(columnName)

    def push(self, tableName, columnName, data: List or Tuple):
        self.__tableService.getTable(tableName)[columnName].data = data
