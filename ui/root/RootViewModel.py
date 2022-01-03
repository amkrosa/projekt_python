import json
from os.path import exists

from infrastructure.Repository import Repository
from infrastructure.json.Decoder import Decoder
from infrastructure.json.Encoder import Encoder
from ui.root.RootView import RootView
from ui.table.TableViewModel import TableViewModel

class RootViewModel:
    def __init__(self):
        if exists("db.json"):
            with open("db.json", "r") as file:
                Repository(json.load(file, cls=Decoder))

        self._rootView = RootView(onCloseHandler=self.onCloseSaveHandler)
        self._tableViewModel = TableViewModel(self._rootView)

    def onCloseSaveHandler(self):
        tables = Repository()
        with open("db.json", "w") as file:
            json.dump(tables, file, cls=Encoder)