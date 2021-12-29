import tkinter

import tk
from dearpygui.dearpygui import window
import dearpygui.dearpygui as dpg


from ui.table.TableView import TableView


class RootView:
    def __init__(self, root: window):
        self.__root = root
        with root:
            dpg.add_group(tag="rootGroup", horizontal=True)
