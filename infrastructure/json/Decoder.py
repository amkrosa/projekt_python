import logging
from json import JSONDecoder
from typing import Any, Callable

from domain.Row import Row
from domain.Table import Table
from domain.column.FloatColumn import FloatColumn
from domain.column.IntegerColumn import IntegerColumn
from domain.column.TextColumn import TextColumn

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
            print(obj["rows"])
            [tab.addColumn(column) for column in obj["columns"].values()]
            for row in obj["rows"].values():
                tab.push(row.values)
            #[tab.push(row.values) for index, row in obj["rows"].items()]
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
