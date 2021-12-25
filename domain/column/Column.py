import abc
from typing import Callable, Any, Dict, List, Tuple


class Column(metaclass=abc.ABCMeta):
    def __init__(self, name: str):
        self._row = 0
        if self._validateName(name):
            self.name = name.strip()

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'data') and
                callable(subclass.data) or
                NotImplemented)

    @property
    @abc.abstractmethod
    def data(self) -> dict[int, Any]:
        """Get dictionary containing data for specified column"""
        raise NotImplementedError

    @data.setter
    @abc.abstractmethod
    def data(self, data: List or Tuple):
        """Write dictionary containing data for specified column"""
        raise NotImplementedError

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def _validateName(self, name: str) -> bool:
        if not isinstance(name, str):
            raise ValueError("Name must be a string")
        if len(name.strip()) == 0:
            raise ValueError("Name cannot consist only of whitespaces")
        return True

    def nextRow(self):
        while True:
            self._row += 1
            yield self._row

    def executeQuery(self, query: Callable[[Any], bool]) -> dict[int, Any]:
        return {index: value for (index, value) in self.data.items() if query(value)}