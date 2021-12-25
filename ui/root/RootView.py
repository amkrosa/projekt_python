import tkinter

import tk


class RootView(tkinter.Toplevel):
    def __init__(self, root):
        tk.Toplevel.__init__(self, root)
        self.protocol('WM_DELETE_WINDOW', self.root.destroy)
        tk.Label(self, text='My Money').pack(side='left')