from dearpygui.dearpygui import window
import dearpygui.dearpygui as dpg

class RootView:
    """
    Root view which makes viewport, sets on exit callback to save data.
    """
    def __init__(self, onCloseHandler):
        dpg.create_viewport(title='Klient bazy danych', width=self.width, height=self.height)
        dpg.set_exit_callback(onCloseHandler)
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
        """
        Center element relative to it's position
        """
        return (self.width-itemWidth)/2, (self.height-itemHeight)/2