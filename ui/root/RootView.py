import tkinter

import tk
from dearpygui.dearpygui import window

from ui.table.TableView import TableView


class RootView:
    def __init__(self, root: window):
        self.__root = root
