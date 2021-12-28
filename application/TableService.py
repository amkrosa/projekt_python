from typing import Callable, Any

from application.ColumnService import ColumnService
from domain.Table import Table
from infrastructure.Repository import Repository


class TableService:
    def __init__(self, repository: Repository):
        self.__repository: Repository = repository

    def push(self, name):
        self.__repository.add(Table(name))

    def removeTable(self, name):
        self.__repository.remove(name)

    def getTable(self, name):
        for value in self.__repository.repository.values():
            if value.name == name:
                return value
        return None

    def query(self, tableName, query: Callable[[Any], bool]) -> list:
        return [row for row in self.getTable(tableName).rows if query(row)]
