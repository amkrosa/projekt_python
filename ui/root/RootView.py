import tkinter

import tk
from dearpygui.dearpygui import window
import dearpygui.dearpygui as dpg

class RootView:
    def __init__(self):
        dpg.create_viewport(title='Klient bazy danych', width=self.width, height=self.height)
        with dpg.window(tag="root"):
            dpg.add_group(tag="rootGroup", horizontal=True)

    @property
    def width(self):
        return 800

    @property
    def height(self):
        return 600

    @property
    def center(self):
        return self.width / 2, self.height / 2

    def centerRelative(self, itemWidth, itemHeight):
        return (self.width-itemWidth)/2, (self.height-itemHeight)/2