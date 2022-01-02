import dearpygui.dearpygui as dpg


class TablesTable:
    def __init__(self):
        if not dpg.does_item_exist("tablesTableGroup"):
            dpg.add_group(parent="rootGroup", tag="tablesTableGroup", horizontal=False)
        with dpg.table(tag="tablesTable", header_row=True, width=250, parent="tablesTableGroup"):
            dpg.add_table_column(tag="tablesTableNameColumn", label="Name")
            dpg.add_table_column(tag="tablesTableRowsColumn", label="Rows")

    def clear(self):
        if dpg.does_item_exist("tablesTable"):
            dpg.delete_item("tablesTable", children_only=False)

    @property
    def tag(self):
        return "tablesTable"
