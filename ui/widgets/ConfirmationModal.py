from typing import Tuple

import dearpygui.dearpygui as dpg


class ConfirmationModal:
    def __init__(self, text, callback, afterCallback, afterData, width, height, center: Tuple):
        if dpg.does_item_exist("confirmation_modal"):
            dpg.delete_item("confirmation_modal")

        with dpg.window(modal=True, tag="confirmation_modal", pos=center, width=width, height=height):
            dpg.add_text(text)
            with dpg.group(horizontal=True):
                dpg.add_button(label="OK", callback=callback, user_data={"confirmation": True, "after": afterCallback,
                                                                         "data": afterData, "modal": self})
                dpg.add_button(label="Wroc", callback=callback, user_data={"confirmation": False, "modal": self})

    def close(self):
        dpg.configure_item("confirmation_modal", show=False)
