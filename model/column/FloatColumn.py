from typing import List, Tuple

from model.column.Column import Column
from lib.Observable import Observable
from model.column.ColumnTypeError import ColumnTypeError


class FloatColumn(Column):
    def __init__(self, name):
        super().__init__(name)

    @property
    def type(self):
        return float

    def cast(self, value):
        try:
            if value != None:
                return float(value)
            else:
                return None
        except ValueError:
            raise ColumnTypeError("FloatColumn may consists only of floats")