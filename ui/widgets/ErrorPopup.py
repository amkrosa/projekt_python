import dearpygui.dearpygui as dpg

class ErrorPopup:
    def __init__(self, itemTag, text):
        self.__tag = itemTag
        self.clear()
        buttonPos = dpg.get_item_pos(self.__tag)
        buttonPos[0]+=110
        with dpg.window(tag=f"error_{self.__tag}", popup=True, show=True, width=120, height=50,
                        min_size=(100,20), no_resize=True, no_move=True,
                        pos=buttonPos):
            dpg.add_text(text)

    def clear(self):
        if dpg.does_item_exist(f"error_{self.__tag}"):
            dpg.delete_item(f"error_{self.__tag}")