import logging
from json import JSONDecoder
from typing import Any, Callable

from model.Row import Row
from model.Table import Table
from model.column.FloatColumn import FloatColumn
from model.column.IntegerColumn import IntegerColumn
from model.column.TextColumn import TextColumn

logger = logging.getLogger(__name__)

class Decoder(JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj: dict):
        if '_type' not in obj:
            return obj
        type = obj['_type']

        if type == 'Table':
            logging.debug(obj["rows"])
            tab = Table(name=obj["name"], tableId=obj["_id"])
            [tab.addColumn(column) for column in obj["columns"].values()]
            for row in obj["rows"].values():
                tab.push(row.values)
            return tab

        if type == 'Column':
            t = obj['type']
            if t == 'str':
                return TextColumn(obj['name'])
            elif t == 'int':
                return IntegerColumn(obj['name'])
            elif t == 'float':
                return FloatColumn(obj['name'])

        if type == 'Row':
            dict = {colName: value for colName, value in obj.items() if colName != '_type'}
            logging.debug(f"Loaded Row: {dict}")
            return Row(dict)

        if type == 'Repository':
            return {tableId: table for tableId, table in obj.items() if tableId != '_type'}

        return obj
