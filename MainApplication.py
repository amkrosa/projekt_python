import tkinter

import tk as tk

from ui.root.RootViewModel import RootViewModel

if __name__ == '__main__':
    root = tkinter.Tk()
    app = RootViewModel(root)
    root.mainloop()