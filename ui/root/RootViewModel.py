from ui.root.RootView import RootView
from ui.table.TableViewModel import TableViewModel


class RootViewModel:
    def __init__(self, root):
        self._rootView = RootView(root)
        self._tableViewModel = TableViewModel(root)