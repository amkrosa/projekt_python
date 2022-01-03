import dearpygui.dearpygui as dpg


class ErrorPopup:
    def __init__(self, itemTag, text, modal=None):
        self.__tag = itemTag
        self.clear()
        buttonPos = dpg.get_item_pos(self.__tag)
        if modal is not None:
            windowPos = dpg.get_item_pos(modal)
            buttonPos[0] += windowPos[0] - 150
            buttonPos[1] += windowPos[1] - 60
        else:
            buttonPos[0] += 110
        print(buttonPos)
        with dpg.window(tag=f"error_{self.__tag}", popup=True, show=True, width=120, height=50,
                        min_size=(100, 20), no_resize=True, no_move=True,
                        pos=buttonPos, no_open_over_existing_popup=False):
            dpg.add_text(text)

    def clear(self):
        if dpg.does_item_exist(f"error_{self.__tag}"):
            dpg.delete_item(f"error_{self.__tag}")
