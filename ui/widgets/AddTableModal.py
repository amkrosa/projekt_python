import dearpygui.dearpygui as dpg


class AddTableModal:

    def __init__(self, center, width, height, callback, afterCallback):
        if dpg.does_item_exist("createTable_modal"):
            dpg.delete_item("createTable_modal")
        with dpg.window(tag="createTable_modal", label="Dodaj tabele", modal=True,
                        pos=center,
                        width=width, height=height):
            dpg.add_input_text(tag="addTableInput_modal", hint="nazwa", label="Tabela", width=100)
            dpg.add_input_text(tag="addColumnInput_modal", hint="nazwa", label="Kolumna", width=100)
            dpg.add_radio_button(tag="addColumnRadio_modal", default_value="str", items=["str", "int", "float"],
                                 horizontal=True)
            dpg.add_button(tag="addColumnButton_modal", label="Dodaj kolumne",
                           callback=self.__addColumn)
            with dpg.table(tag="addColumnTable", header_row=True):
                dpg.add_table_column(label="Kolumna")
                dpg.add_table_column(label="Typ")

            with dpg.group(horizontal=True):
                dpg.add_button(label="Stworz", callback=callback,
                               user_data={"confirmation": True, "after": afterCallback, "modal": self})
                dpg.add_button(label="Wroc", callback=callback, user_data={"confirmation": False})

    @property
    def form(self):
        names = {int(item.split("_")[2]): item for item in dpg.get_aliases() if item.startswith("addColumn_name_")}
        types = {int(item.split("_")[2]): item for item in dpg.get_aliases() if item.startswith("addColumn_type_")}
        return {
            "name": dpg.get_value("addTableInput_modal"),
            "columns": {dpg.get_value(names[index]): dpg.get_value(types[index]) for index in range(1, len(names)+1)}
        }

    def __addColumn(self):
        with dpg.table_row(parent="addColumnTable"):
            count = len(dpg.get_item_children("addColumnTable", 1)) #get rows of element addColumnTable
            dpg.add_text(dpg.get_value("addColumnInput_modal"), tag=f"addColumn_name_{count}")
            dpg.add_text(dpg.get_value("addColumnRadio_modal"), tag=f"addColumn_type_{count}")

    def close(self):
        dpg.configure_item("createTable_modal", show=False)
