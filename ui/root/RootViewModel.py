from ui.root.RootView import RootView
from ui.table.TableViewModel import TableViewModel


class RootViewModel:
    def __init__(self):
        self._rootView = RootView()
        self._tableViewModel = TableViewModel(self._rootView)