import tk as tk

from application.RootService import RootService

if __name__ == '__main__':
    root = tk.Tk()
    root.withdraw()
    app = RootService(root)
    root.mainloop()