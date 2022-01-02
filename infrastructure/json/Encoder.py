from json import JSONEncoder
from typing import Any

from model.Row import Row
from model.Table import Table
from model.column.Column import Column
from infrastructure.Repository import Repository
from lib.Observable import Observable


class Encoder(JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, Table):
            return {
                "_type": "Table",
                "_id": o.id,
                "name": o.name,
                "columns": o.columns,
                "rows": o.rows
            }
        if isinstance(o, Row):
            d = {name: value for name, value in o.values.items()}
            d["_type"] = "Row"
            return d
        if isinstance(o, Column):
            return {
                "_type": "Column",
                "name": o.name,
                "type": o.type
            }
        if isinstance(o, type):
            return o.__name__
        if isinstance(o, Repository):
            rep = o.repository
            rep["_type"] = "Repository"
            return rep
        if isinstance(o, Observable):
            return o.get()
        return super().default(o)
