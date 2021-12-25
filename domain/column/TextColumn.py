from typing import List, Tuple

from domain.column.Column import Column


class TextColumn(Column):
    def __init__(self, name):
        super().__init__(name)
        self.__data: dict[int, str] = dict()

    @property
    def data(self) -> dict:
        return self.__data

    def data(self, data: List or Tuple):
        for element in data:
            if isinstance(element, str):
                self.__data[super().nextRow()] = element
            else:
                raise TypeError("TextColumn may consists only of strings")

