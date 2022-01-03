from typing import List, Tuple

from model.column.Column import Column
from lib.Observable import Observable


class IntegerColumn(Column):
    def __init__(self, name):
        super().__init__(name)

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