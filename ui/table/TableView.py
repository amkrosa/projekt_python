from typing import Any
from uuid import uuid4

from dearpygui.dearpygui import window
import dearpygui.dearpygui as dpg

from model.Table import Table
from model.column.Column import Column
from ui.root.RootView import RootView
from ui.widgets.AddTableModal import AddTableModal
from ui.widgets.ConfirmationModal import ConfirmationModal
from ui.widgets.ErrorPopup import ErrorPopup
from ui.widgets.TablesTable import TablesTable


class TableView:
    def __init__(self, root: RootView, addTableCallback, addColumnCallback, querySearchCallback, refreshCallback):
        self.__root = root
        self.__addTableButton = "addTableButton"
        self.__tablesTable = "tablesTable"
        self.__addTableInput = "addTableInput"
        self.__columnsTable = "columnsTable"
        self.__tablesTableRowCount = 0
        self.__columnTypes = ["str", "int", "float"]
        self.__tablesTable = TablesTable()
        self.__createAddTableButton(addTableCallback)
        dpg.add_spacer(width=50, parent="rootGroup")
        self.__createColumnsTable()
        self.__createAddColumn(addColumnCallback)
        self.__createQuerySearch(querySearchCallback, refreshCallback)

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

    def errorPopup(self, itemTag, text, modal=None):
        return ErrorPopup(itemTag, text, modal)

    def addTableModal(self, callback, afterCallback):
        AddTableModal(callback=callback, afterCallback=afterCallback,
                      width=250, height=270, center=self.__root.centerRelative(250, 270))

    def confirmationModal(self, text, callback, afterCallback, afterData):
        ConfirmationModal(text=text, afterData=afterData, callback=callback, afterCallback=afterCallback,
                          width=250, height=90, center=self.__root.centerRelative(250, 150))

    def __createAddTableInput(self, addTableCallback):
        dpg.add_input_text(tag="addTableInput", before=self.tablesTable.tag, label="Nazwa", parent="tablesTableGroup",
                           width=100, callback=addTableCallback, on_enter=True)

    def __createAddTableButton(self, handler):
        dpg.add_button(tag="addTableButton", before=self.tablesTable.tag, label="Dodaj tabele",
                       parent="tablesTableGroup", callback=handler)

    def __createAddColumn(self, handler):
        dpg.add_input_text(tag="addColumnInput", before=self.columnsTable, label="Nazwa", parent="columnsTableGroup",
                           width=100, callback=handler, on_enter=True)
        dpg.add_radio_button(tag="addColumnRadio", default_value="str", items=self.__columnTypes,
                             before=self.columnsTable,
                             horizontal=True)
        dpg.add_button(tag="addColumnButton", before=self.columnsTable, label="Dodaj kolumne",
                       parent="columnsTableGroup", callback=handler)

    def __createQuerySearch(self, handler, resetHandler):
        with dpg.group(parent="columnsTableGroup", tag="querySearchGroup", horizontal=True):
            dpg.add_input_text(tag="querySearchInput", hint="lambda row: row[\"id\"]>3", width=250)
            dpg.add_button(tag="querySearchButton", label="Szukaj", callback=handler,
                           user_data={"dataCallback": lambda tag: dpg.get_value(tag), "data": "querySearchInput"}, width=75)
            dpg.add_button(tag="querySearchResetButton", label="Reset", callback=resetHandler, width=75)

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

    def addTable(self, name, tableId):
        with dpg.table_row(parent="tablesTable"):
            dpg.add_text(name, tag=tableId)
            dpg.add_text("0", tag=f"count_{tableId}")

    def setRegistry(self, handlerTag, itemTag, handler, userData=None):
        if dpg.does_alias_exist(handlerTag):
            dpg.remove_alias(handlerTag)
        with dpg.item_handler_registry(tag=handlerTag):
            dpg.add_item_clicked_handler(callback=handler, user_data=userData)
        dpg.bind_item_handler_registry(itemTag, handlerTag)

    def setColumns(self, tab: Table, data: dict, addRowHandler, deleteRowHandler):
        self.__clearColumnsTable()
        dpg.add_text(tab.name, parent="columnsTableGroup", before=self.columnsTable, tag="tableNameText")
        dpg.add_table_column(parent=self.columnsTable, label="Wiersz", tag="rowCount")

        for name in tab.columns.keys():
            dpg.add_table_column(parent=self.columnsTable, label=name, tag=f"column_{name}")
        dpg.add_table_column(parent=self.columnsTable, label="Akcje", tag=f"inputColumn")

        self.__setColumnsData(tab.name, data, deleteRowHandler)
        self.__setColumnsInput(str(len(tab.rows) + 1), tab.columns, addRowHandler)

        dpg.configure_item("columnsTableGroup", show=True)

    def __setColumnsData(self, tableName, data: dict, deleteRowHandler):
        for i, row in data.items():
            with dpg.table_row(parent=self.columnsTable, tag=f"row_{i}"):
                dpg.add_text(str(i))
                for key, value in row.get().values.items():
                    dpg.add_text(str(value))
                dpg.add_button(label="Usun", tag=f"deleteRowButton_{i}", callback=deleteRowHandler,
                               user_data={"table": tableName, "row": i})

    def __setColumnsInput(self, rowsCount, columns, addRowHandler):
        with dpg.table_row(parent=self.columnsTable, tag=f"input_row"):
            dpg.add_text(rowsCount)
            for col in columns.values():
                dpg.add_input_text(hint=f"{self.__getTypeText(col.type)}", tag=f"input_row_col_{col.name}")
            dpg.add_button(label="Dodaj", tag="addRowButton", callback=addRowHandler, user_data=self.readRowInput)

    def hideColumns(self):
        dpg.configure_item("columnsTableGroup", show=False)
        self.__clearColumnsTable()

    def setTables(self, data, selectTableHandler, deleteTableHandler):
        self.__tablesTable.clear()
        self.__tablesTable = TablesTable()
        for tableId, value in data.items():
            with dpg.table_row(parent="tablesTable"):
                dpg.add_selectable(label=value.name, tag=f"table_{tableId.__str__()}", callback=selectTableHandler, user_data=self.__clearTableSelection)
                dpg.add_text(value.rowCount, tag=f"count_{tableId.__str__()}")
                dpg.add_button(label="Usun", tag=f"deleteTableButton_{tableId.__str__()}", callback=deleteTableHandler,
                               user_data={"id":tableId.__str__(), "currentTable": lambda: self.currentTableSelection})

    def __clearTableSelection(self, currentSelection=None):
        items = [item for item in dpg.get_aliases() if item.startswith("table_")]
        for item in items:
            if not item.split("_")[1] == currentSelection:
                dpg.set_value(item, False)
            else:
                dpg.set_value(item, True)

    def readRowInput(self):
        items = [item for item in dpg.get_aliases() if item.startswith("input_row_col_")]
        return {item.split("_")[3]: (dpg.get_value(item) if dpg.get_value(item) != "" else None) for item in items}

    def __getTypeText(self, type):
        if type == str:
            return "str"
        elif type == int:
            return "int"
        elif type == float:
            return "float"

    def __setitem__(self, key, value):
        dpg.set_value(key, value)

    def set(self, key, value):
        dpg.set_value(key, value)
