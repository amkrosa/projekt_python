from typing import Type, List, Tuple

from domain.column.Column import Column


class IntegerColumn(Column):
    def __init__(self, name):
        super().__init__(name)
        self.__data: dict[int, int] = dict()

    @property
    def data(self) -> dict:
        return self.__data

    @data.setter
    def data(self, data: List or Tuple):
        for element in data:
            if isinstance(element, int):
                next = super().nextRow().__next__()
                print(next)
                self.__data[next] = element
            else:
                raise TypeError("IntegerColumn may consists only of integers")