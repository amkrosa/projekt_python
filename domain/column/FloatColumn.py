from typing import List, Tuple

from domain.column.Column import Column


class FloatColumn(Column):
    def __init__(self, name):
        super().__init__(name)
        self.__data: dict[int, float] = dict()

    @property
    def data(self) -> dict:
        return self.__data

    @data.setter
    def data(self, data: List or Tuple):
        for element in data:
            if isinstance(element, float):
                self.__data[super().nextRow()] = element
            else:
                raise TypeError("FloatColumn may consists only of floats")