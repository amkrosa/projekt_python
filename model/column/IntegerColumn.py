from typing import List, Tuple

from model.column.Column import Column
from lib.Observable import Observable
from model.column.ColumnTypeError import ColumnTypeError


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
            raise ColumnTypeError("IntegerColumn may consists only of int")