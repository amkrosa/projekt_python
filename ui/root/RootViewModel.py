import json
from os.path import exists

from model.Repository import Repository
from infrastructure.Decoder import Decoder
from infrastructure.Encoder import Encoder
from ui.root.RootView import RootView
from ui.table.TableViewModel import TableViewModel

class RootViewModel:
    """
    Root handler class, loads data to Repository singleton from a file if it exists. Initializes table handler class.
    """
    def __init__(self):
        if exists("db.json"):
            with open("db.json", "r") as file:
                Repository(json.load(file, cls=Decoder))

        self._rootView = RootView(onCloseHandler=self.onCloseSaveHandler)
        self._tableViewModel = TableViewModel(self._rootView)

    def onCloseSaveHandler(self):
        """
        Handler executed when application is closed. Saves current data to json file.
        """
        tables = Repository()
        with open("db.json", "w") as file:
            json.dump(tables, file, cls=Encoder)