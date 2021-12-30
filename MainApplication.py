import logging

import dearpygui.dearpygui as dpg

from ui.root.RootView import RootView
from ui.root.RootViewModel import RootViewModel

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
    dpg.create_context()
    RootViewModel()
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("root", True)
    dpg.start_dearpygui()
    dpg.destroy_context()