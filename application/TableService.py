import uuid
from typing import Callable, Any, Dict

from domain.Table import Table
from infrastructure.Repository import Repository


class TableService:
    def __init__(self, repository: Repository):
        self.__repository: Repository = repository

    def addTable(self, tableId, name):
        self.__repository.add(Table(name, tableId))

    def push(self, tableName, row):
        self.getTable(name=tableName).push(row)

    def removeTable(self, name):
        self.__repository.remove(name)

    def getTables(self) -> Dict[Any, Table]:
        return self.__repository.repository

    def getTable(self, name) -> Table:
        for value in self.__repository.repository.values():
            if value.name == name:
                return value
        return None

    def query(self, tableName, query: Callable[[Any], bool]) -> dict:
        return {i: row for i, row in self.getTable(tableName).rows.items() if query(row.get())}
