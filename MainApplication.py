import tk as tk

from ui.RootViewModel import RootViewModel

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    app = RootViewModel(root)
    root.mainloop()