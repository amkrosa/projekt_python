import uuid
from typing import Dict, Any, TypeVar, Union

from domain.Table import Table
from domain.column.Column import Column

T = TypeVar("T", bound=Union[Table, Column])


class Repository:
    def __init__(self):
        self.__repository: Dict[uuid, T] = dict()

    @property
    def repository(self):
        return self.__repository

    def __getitem__(self, item):
        return self.__repository[item]

    def add(self, arg, id=uuid.uuid4()):
        self.repository[id] = arg

    def remove(self, arg: uuid):
        self.repository.pop(arg)

    def findByName(self, name):
        for value in self.repository.values():
            if value.name == name:
                return value
        return None