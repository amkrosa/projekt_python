import tkinter

import tk

from ui.table.TableView import TableView


class RootView:
    def __init__(self, root):
        root.geometry('500x500')
        root['bg'] = '#AC99F2'
        frame = tkinter.Frame(root)
        frame.pack()
        TableView(frame)
