from typing import List, Tuple

from domain.column.Column import Column
from lib.Observable import Observable


class IntegerColumn(Column):
    def __init__(self, name):
        super().__init__(name)
        #self.__data: dict[int, Observable] = dict()

    @property
    def type(self):
        return int

    def cast(self, value):
        try:
            if value != None:
                return int(value)
            else:
                return None
        except ValueError:
            raise TypeError("IntegerColumn may consists only of int")

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
    #             if handler is not None:
    #                 obs.addCallback(handler)
    #             self.__data[next] = obs
    #             print(self.data.__str__())
    #         else:
    #             raise TypeError("IntegerColumn may consists only of integers")