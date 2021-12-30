from typing import Any
from uuid import uuid4

from dearpygui.dearpygui import window
import dearpygui.dearpygui as dpg

from domain.Table import Table
from domain.column.Column import Column


class TableView:
    def __init__(self, root: window, addTableCallback, addColumnCallback):
        self.__root = root
        self.__addTableButton = "addTableButton"
        self.__tablesTable = "tablesTable"
        self.__addTableInput = "addTableInput"
        self.__columnsTable = "columnsTable"
        self.__tablesTableRowCount = 0
        self.__columnTypes = ["str", "int", "float"]
        self.__databaseTables()
        self.__createAddTableInput(addTableCallback)
        self.__createAddTableButton()
        self.__createColumnsTable()
        self.__createAddColumn(addColumnCallback)
        self.__createQuerySearch()

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

    @property
    def currentTableSelection(self):
        return dpg.get_value("tableNameText")

    @property
    def currentQuerySearch(self):
        return dpg.get_value("querySearchInput")

    def errorPopup(self, itemTag, text):
        self.clearErrorPopup(itemTag)
        buttonPos = dpg.get_item_pos(itemTag)
        buttonPos[0]+=110
        with dpg.window(tag=f"error_{itemTag}", popup=True, show=True, width=120, height=50,
                        min_size=(100,20), no_resize=True, no_move=True,
                        pos=buttonPos):
            dpg.add_text(text)

    def clearErrorPopup(self, itemTag):
        if dpg.does_item_exist(f"error_{itemTag}"):
            dpg.delete_item(f"error_{itemTag}")

    def __createAddTableInput(self, addTableCallback):
        dpg.add_input_text(tag="addTableInput", before=self.tablesTable, label="Nazwa", parent="tablesTableGroup",
                           width=100, callback=addTableCallback, on_enter=True)

    def __createAddTableButton(self):
        dpg.add_button(tag="addTableButton", before=self.tablesTable, label="Dodaj tabele", parent="tablesTableGroup")

    def __createAddColumn(self, addColumnCallback):
        dpg.add_input_text(tag="addColumnInput", before=self.columnsTable, label="Nazwa", parent="columnsTableGroup",
                           width=100, callback=addColumnCallback, on_enter=True)
        dpg.add_radio_button(tag="addColumnRadio", default_value="str", items=self.__columnTypes, before=self.columnsTable,
                             horizontal=True)
        dpg.add_button(tag="addColumnButton", before=self.columnsTable, label="Dodaj kolumne", parent="columnsTableGroup")

    def __createQuerySearch(self):
        with dpg.group(parent="columnsTableGroup", tag="querySearchGroup", horizontal=True, width=150):
            dpg.add_input_text(tag="querySearchInput", hint="lambda row: row[\"id\"]>3")
            dpg.add_button(tag="querySearchButton", label="Szukaj")

    def __databaseTables(self):
        with dpg.group(parent="rootGroup", tag="tablesTableGroup", horizontal=False):
            with dpg.table(tag="tablesTable", header_row=True, width=250):
                dpg.add_table_column(tag="tablesTableNameColumn", label="Name")
                dpg.add_table_column(tag="tablesTableRowsColumn", label="Rows")

    def __createColumnsTable(self):
        with dpg.group(parent="rootGroup", tag="columnsTableGroup", show=False):
            dpg.add_table(tag="columnsTable", header_row=True, width=400)

    def __clearColumnsTable(self):
        if dpg.does_item_exist("columnsTable") and dpg.does_item_exist("tableNameText"):
            dpg.delete_item("tableNameText")
            dpg.delete_item(self.columnsTable, children_only=True)

    def addColumn(self):
        name = dpg.get_value("addColumnInput")
        radio = dpg.get_value("addColumnRadio")
        return name, radio

    def addTable(self):
        self.clearErrorPopup(itemTag="addTableButton")
        id = uuid4()
        data = dpg.get_value(self.addTableInput)
        with dpg.table_row(parent=self.tablesTable):
            dpg.add_text(data, tag=id.__str__())
            dpg.add_text("0", tag=f"count_{id.__str__()}")
        return id.__str__(), data

    def changeRow(self, tag, data):
        dpg.set_value(tag, data)

    def setRegistry(self, handlerTag, itemTag, handler, userData = None):
        if dpg.does_alias_exist(handlerTag):
            dpg.remove_alias(handlerTag)
        with dpg.item_handler_registry(tag=handlerTag):
            dpg.add_item_clicked_handler(callback=handler)
        dpg.bind_item_handler_registry(itemTag, handlerTag)

    def setColumns(self, tab: Table, data: dict, addRowHandler, deleteRowHandler):
        self.__clearColumnsTable()
        dpg.add_text(tab.name, parent="columnsTableGroup", before=self.columnsTable, tag="tableNameText")
        dpg.add_table_column(parent=self.columnsTable, label="Wiersz", tag="rowCount")

        ##jeszcze mozna byloby zamiast robic w Row dict [str, Any] to zrobic [Column, Any]
        for name in tab.columns.keys():
            dpg.add_table_column(parent=self.columnsTable, label=name, tag=f"column_{name}")
        dpg.add_table_column(parent=self.columnsTable, tag=f"inputColumn")

        for i, row in data.items():
            with dpg.table_row(parent=self.columnsTable, tag=f"row_{i}"):
                dpg.add_text(str(i))
                for key, value in row.get().values:
                    dpg.add_text(str(value))
                dpg.add_button(label="Usun", tag=f"deleteRowButton_{i}")
                self.setRegistry(handlerTag=f"deleteRowButtonHandler_{i}",
                                 itemTag=f"deleteRowButton_{i}", handler=deleteRowHandler,
                                 userData={"table": tab.name, "row": i})

        with dpg.table_row(parent=self.columnsTable, tag=f"input_row"):
            dpg.add_text(str(len(tab.rows)+1))
            for col in tab.columns.values():
                dpg.add_input_text(hint=f"{self.__getTypeText(col.type)}", tag=f"input_row_col_{col.name}")
            dpg.add_button(label="Dodaj", tag="addRowButton")
            self.setRegistry(handlerTag="addRowButtonHandler", itemTag="addRowButton", handler=addRowHandler)

        dpg.configure_item("columnsTableGroup", show=True)

    def readRowInput(self):
        items = [item for item in dpg.get_aliases() if item.startswith("input_row_col_")]
        return {item.split("_")[3]: (dpg.get_value(item) if dpg.get_value(item)!="" else None) for item in items}

    def __getTypeText(self, type):
        if type == str:
            return "str"
        elif type == int:
            return "int"
        elif type == float:
            return "float"