import json
import uuid
from json import JSONEncoder
from typing import Dict, Any, TypeVar, Union

from lib.BaseObservable import BaseObservable
from model.Table import Table
from model.column.Column import Column
from lib.SingletonMeta import SingletonMeta

T = TypeVar("T", bound=Union[Table, Column])


class Repository(BaseObservable, metaclass=SingletonMeta):
    def __init__(self, data=None):
        super().__init__()
        if data is not None:
            self.__repository = data
        else:
            self.__repository = {}

    @property
    def repository(self):
        return self.__repository

    @repository.setter
    def repository(self, repository):
        self.__repository = {tableId: table for tableId, table in repository.items()}

    def __getitem__(self, item):
        return self.__repository[item]

    def __len__(self):
        return len(self.repository)

    def add(self, arg, id=uuid.uuid4().__str__()):
        self.repository[id] = arg
        self._doCallbacks()

    def remove(self, tableId: uuid):
        self.repository.pop(tableId)
        self._doCallbacks()

    def findByName(self, name):
        for value in self.repository.values():
            if value.name == name:
                return value
        return None
