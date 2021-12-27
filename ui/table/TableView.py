from uuid import uuid4

from dearpygui.dearpygui import window
import dearpygui.dearpygui as dpg


class TableView:
    def __init__(self, root: window):
        self.__root = root
        self.__addTableButton = "addTableButton"
        self.__tablesTable = "tablesTable"
        self.__tablesTableRowCount = 0
        self.__databaseTables()
        self.__createAddTableButton()

    @property
    def addTableButton(self):
        return self.__addTableButton

    @property
    def tablesTable(self):
        return self.__tablesTable

    def __createAddTableButton(self):
        dpg.add_button(tag="addTableButton", label="Dodaj tabele", parent="root")

    def __databaseTables(self):
        with self.__root:
            with dpg.table(tag="tablesTable", header_row=True):
                dpg.add_table_column(tag="tablesTableNameColumn", label="Name")
                dpg.add_table_column(tag="tablesTableRowsColumn", label="Rows")

    def addRow(self, data):
        uuid = uuid4
        with dpg.table_row(parent=self.tablesTable):
            dpg.add_text(data, tag=uuid.__str__())
        return uuid

    def changeRow(self, tag, data):
        dpg.set_value(tag, data)

    def setAddTableRegistry(self, handler):
        with dpg.item_handler_registry(tag="addTableButtonHandler"):
            dpg.add_item_clicked_handler(callback=handler)
        dpg.bind_item_handler_registry(self.addTableButton, "addTableButtonHandler")