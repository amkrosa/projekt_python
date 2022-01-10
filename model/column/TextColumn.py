from typing import List, Tuple

from model.column.Column import Column
from lib.Observable import Observable
from model.column.ColumnTypeError import ColumnTypeError


class TextColumn(Column):
    def __init__(self, name):
        super().__init__(name)

    @property
    def type(self):
        return str

    def cast(self, value):
        try:
            if value != None:
                return str(value)
            else:
                return None
        except ValueError:
            raise ColumnTypeError("TextColumn may consists only of str")
