from typing import Any
from uuid import uuid4

from dearpygui.dearpygui import window
import dearpygui.dearpygui as dpg

from domain.column.Column import Column


class TableView:
    def __init__(self, root: window):
        self.__root = root
        self.__addTableButton = "addTableButton"
        self.__tablesTable = "tablesTable"
        self.__addTableInput = "addTableInput"
        self.__columnsTable = "columnsTable"
        self.__tablesTableRowCount = 0
        self.__databaseTables()
        self.__createAddTableInput()
        self.__createAddTableButton()
        self.__createColumnsTable()

    @property
    def addTableButton(self):
        return self.__addTableButton

    def addTableInputValue(self):
        return dpg.get_value(self.addTableInput)

    @property
    def tablesTable(self):
        return self.__tablesTable

    @property
    def addTableInput(self):
        return self.__addTableInput

    @property
    def columnsTable(self):
        return self.__columnsTable

    def errorPopup(self, text):
        self.clearErrorPopup()
        buttonPos = dpg.get_item_pos(self.addTableButton)
        buttonPos[0]+=110
        with dpg.window(tag="error_addTableButton", popup=True, show=True, width=120, height=50,
                        min_size=(100,20), no_resize=True, no_move=True,
                        pos=buttonPos):
            dpg.add_text(text)

    def clearErrorPopup(self):
        if dpg.does_item_exist("error_addTableButton"):
            dpg.delete_item("error_addTableButton")

    def __createAddTableInput(self):
        dpg.add_input_text(tag="addTableInput", before=self.tablesTable, label="Nazwa", parent="root", width=100)

    def __createAddTableButton(self):
        dpg.add_button(tag="addTableButton", before=self.tablesTable, label="Dodaj tabele", parent="root")

    def __databaseTables(self):
        with self.__root:
            with dpg.table(tag="tablesTable", header_row=True, width=250):
                dpg.add_table_column(tag="tablesTableNameColumn", label="Name")
                dpg.add_table_column(tag="tablesTableRowsColumn", label="Rows")

    def __createColumnsTable(self):
        dpg.add_table(parent="root", tag="columnsTable", header_row=True, width=250, show=False)

    def __clearColumnsTable(self):
        if dpg.does_item_exist("columnsTable"):
            dpg.delete_item(self.columnsTable, children_only=True)

    def addRow(self):
        self.clearErrorPopup()
        id = uuid4()
        print(id)
        data = dpg.get_value(self.addTableInput)
        with dpg.table_row(parent=self.tablesTable):
            dpg.add_text(data, tag=id.__str__())
            dpg.add_text("0", tag=f"count_{id.__str__()}")
        return id.__str__(), data

    def changeRow(self, tag, data):
        dpg.set_value(tag, data)

    def setRegistry(self, handlerTag, itemTag, handler):
        with dpg.item_handler_registry(tag=handlerTag):
            dpg.add_item_clicked_handler(callback=handler)
        dpg.bind_item_handler_registry(itemTag, handlerTag)

    def setColumns(self, rows: int, columns, data: list):
        self.__clearColumnsTable()
        dpg.add_table_column(parent=self.columnsTable, label="Wiersz", tag="rowCount")

        ##jeszcze mozna byloby zamiast robic w Row dict [str, Any] to zrobic [Column, Any]
        for name in columns.keys():
            dpg.add_table_column(parent=self.columnsTable, label=name, tag=f"column_{name}")

        rowCounter = 0
        for row in data:
            with dpg.table_row(parent=self.columnsTable, tag=f"row_{rowCounter+1}"):
                dpg.add_text(str(rowCounter+1))
                for key, value in row.get().values:
                    dpg.add_text(str(value))
                rowCounter+=1

        dpg.configure_item(self.columnsTable, show=True)
