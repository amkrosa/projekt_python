from typing import List, Tuple

from model.column.Column import Column
from lib.Observable import Observable


class FloatColumn(Column):
    def __init__(self, name):
        super().__init__(name)
        #self.__data: dict[int, float] = dict()

    @property
    def type(self):
        return float

    def cast(self, value):
        try:
            return float(value)
        except ValueError:
            raise TypeError("FloatColumn may consists only of floats")

    # @property
    # def data(self) -> dict:
    #     return self.__data
    #
    # def set(self, key: int, data: int):
    #     if isinstance(data, int):
    #         self.__data[key].set(data)
    #     else:
    #         raise TypeError("IntegerColumn may consists only of integers")
    #
    # def delete(self, key: int):
    #     self.__data.pop(key)
    #
    # def push(self, data: List or Tuple, handler):
    #     for element in data:
    #         if isinstance(element, int):
    #             next = super().nextRow().__next__()
    #             obs = Observable(element)
    #             obs.addCallback(handler)
    #             self.__data[next] = obs
    #         else:
    #             raise TypeError("IntegerColumn may consists only of integers")