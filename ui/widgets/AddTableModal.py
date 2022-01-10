import dearpygui.dearpygui as dpg

from ui.widgets.ErrorPopup import ErrorPopup


class AddTableModal:
    def __init__(self, center, width, height, callback, afterCallback):
        """
        Creates add table modal and displays it
        """
        if dpg.does_item_exist("createTable_modal"):
            dpg.delete_item("createTable_modal")
        with dpg.window(tag="createTable_modal", label="Dodaj tabele",
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
                dpg.add_button(label="Stworz", tag="createTableButton_modal", callback=callback,
                               user_data={"confirmation": True, "after": afterCallback, "modal": self})
                dpg.add_button(label="Wroc", callback=callback, user_data={"confirmation": False, "modal": self})

    @property
    def form(self):
        """
        Used to read values from add table modal, which are: table name and columns dictionary with names and types
        """
        names = {int(item.split("_")[2]): item for item in dpg.get_aliases() if item.startswith("addColumn_name_")}
        types = {int(item.split("_")[2]): item for item in dpg.get_aliases() if item.startswith("addColumn_type_")}
        return {
            "name": dpg.get_value("addTableInput_modal"),
            "columns": {dpg.get_value(names[index]): dpg.get_value(types[index]) for index in range(1, len(names)+1)}
        }

    def __addColumn(self):
        """
        Adds column to add table modal and unfortunately validates, displaying ErrorPopup on error.
        """
        name = dpg.get_value("addColumnInput_modal")

        if not isinstance(name, str):
            ErrorPopup(itemTag="addColumnButton_modal", text="Nazwa kolumny musi byc tekstem", modal="createTable_modal")
            return

        if len(name.strip()) == 0:
            ErrorPopup(itemTag="createTable_modal", text="Nazwa musi kolumny zawierac znaki drukowalne", modal="createTable_modal")
            return

        with dpg.table_row(parent="addColumnTable"):
            count = len(dpg.get_item_children("addColumnTable", 1))  # get rows of element addColumnTable
            dpg.add_text(dpg.get_value("addColumnInput_modal"), tag=f"addColumn_name_{count}")
            dpg.add_text(dpg.get_value("addColumnRadio_modal"), tag=f"addColumn_type_{count}")

    def close(self):
        dpg.configure_item("createTable_modal", show=False)
