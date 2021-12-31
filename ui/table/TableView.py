from typing import Any
from uuid import uuid4

from dearpygui.dearpygui import window
import dearpygui.dearpygui as dpg

from domain.Table import Table
from domain.column.Column import Column
from ui.root.RootView import RootView


class TableView:
    def __init__(self, root: RootView, addTableCallback, addColumnCallback):
        self.__root = root
        self.__addTableButton = "addTableButton"
        self.__tablesTable = "tablesTable"
        self.__addTableInput = "addTableInput"
        self.__columnsTable = "columnsTable"
        self.__tablesTableRowCount = 0
        self.__columnTypes = ["str", "int", "float"]
        self.__databaseTables()
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

    def confirmationModal(self, text, callback, afterCallback, afterData):
        if dpg.does_item_exist("confirmation_modal"):
            dpg.delete_item("confirmation_modal")

        with dpg.window(modal=True, tag="confirmation_modal", pos=self.__root.centerRelative(200,100), width=200, height=100):
            dpg.add_text(text)
            with dpg.group(horizontal=True):
                dpg.add_button(label="OK", callback=callback, user_data={"confirmation": True, "after": afterCallback,
                                                                         "data": afterData})
                dpg.add_button(label="Wroc", callback=callback, user_data={"confirmation": False})

    def closeModal(self, itemTag):
        dpg.configure_item(itemTag, show=False)

    def clearErrorPopup(self, itemTag):
        if dpg.does_item_exist(f"error_{itemTag}"):
            dpg.delete_item(f"error_{itemTag}")

    def addColumnModal(self):
        with dpg.table_row(parent="addColumnTable"):
            count = len(dpg.get_item_children("addColumnTable", 1))
            dpg.add_text(dpg.get_value("addColumnInput_modal"), tag=f"addColumn_name_{count}")
            dpg.add_text(dpg.get_value("addColumnRadio_modal"), tag=f"addColumn_type_{count}")
            print(self.addTableForm)

    @property
    def addTableForm(self):
        names = [item for item in dpg.get_aliases() if item.startswith("addColumn_name_")]
        types = [item for item in dpg.get_aliases() if item.startswith("addColumn_type_")]
        return {
             "name": dpg.get_value("addTableInput_modal"),
             "columns": {dpg.get_value(names[index]): dpg.get_value(types[index]) for index in range(len(names))}
        }

    def addTableModal(self, callback, afterCallback):
        if dpg.does_item_exist("createTable_modal"):
            dpg.delete_item("createTable_modal")
        with dpg.window(tag="createTable_modal", label="Dodaj tabele", modal=True, pos=self.__root.centerRelative(itemWidth=270,itemHeight=250),
                        width=270, height=250):
            dpg.add_input_text(tag="addTableInput_modal", hint="nazwa", label="Tabela", width=100)
            dpg.add_input_text(tag="addColumnInput_modal", hint="nazwa", label="Kolumna", width=100)
            dpg.add_radio_button(tag="addColumnRadio_modal", default_value="str", items=self.__columnTypes,
                                 horizontal=True)
            dpg.add_button(tag="addColumnButton_modal", label="Dodaj kolumne",
                           callback=self.addColumnModal)
            with dpg.table(tag="addColumnTable", header_row=True):
                dpg.add_table_column(label="Kolumna")
                dpg.add_table_column(label="Typ")

            with dpg.group(horizontal=True):
                dpg.add_button(label="Stworz", callback=callback, user_data={"confirmation": True, "after": afterCallback})
                dpg.add_button(label="Wroc", callback=callback, user_data={"confirmation": False})


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
        if not dpg.does_item_exist("tablesTableGroup"):
            dpg.add_group(parent="rootGroup", tag="tablesTableGroup", horizontal=False)
        with dpg.table(tag="tablesTable", header_row=True, width=250, parent="tablesTableGroup"):
            dpg.add_table_column(tag="tablesTableNameColumn", label="Name")
            dpg.add_table_column(tag="tablesTableRowsColumn", label="Rows")

    def __clearDatabaseTables(self):
        if dpg.does_item_exist("tablesTable"):
            dpg.delete_item("tablesTable", children_only=False)

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
        # self.clearErrorPopup(itemTag="addTableButton")
        with dpg.table_row(parent="tablesTable"):
            dpg.add_text(name, tag=tableId)
            dpg.add_text("0", tag=f"count_{tableId}")

    def __setitem__(self, key, value):
        dpg.set_value(key, value)

    def setRegistry(self, handlerTag, itemTag, handler, userData = None):
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
        dpg.add_table_column(parent=self.columnsTable, tag=f"inputColumn")

        self.__setColumnsData(tab.name, data, deleteRowHandler)
        self.__setColumnsInput(str(len(tab.rows)+1), tab.columns, addRowHandler)

        dpg.configure_item("columnsTableGroup", show=True)

    def __setColumnsData(self, tableName, data: dict, deleteRowHandler):
        for i, row in data.items():
            with dpg.table_row(parent=self.columnsTable, tag=f"row_{i}"):
                dpg.add_text(str(i))
                for key, value in row.get().values.items():
                    dpg.add_text(str(value))
                dpg.add_button(label="Usun", tag=f"deleteRowButton_{i}")
                self.setRegistry(handlerTag=f"deleteRowButtonHandler_{i}",
                                 itemTag=f"deleteRowButton_{i}", handler=deleteRowHandler,
                                 userData={"table": tableName, "row": i})

    def __setColumnsInput(self, rowsCount, columns, addRowHandler):
        with dpg.table_row(parent=self.columnsTable, tag=f"input_row"):
            dpg.add_text(rowsCount)
            for col in columns.values():
                dpg.add_input_text(hint=f"{self.__getTypeText(col.type)}", tag=f"input_row_col_{col.name}")
            dpg.add_button(label="Dodaj", tag="addRowButton")
            self.setRegistry(handlerTag="addRowButtonHandler", itemTag="addRowButton", handler=addRowHandler)

    def setTables(self, data, selectTableHandler):
        self.__clearDatabaseTables()
        self.__databaseTables()
        for tableId, value in data.items():
            with dpg.table_row(parent="tablesTable"):
                dpg.add_text(value.name, tag=tableId.__str__())
                self.setRegistry(itemTag=tableId.__str__(), handlerTag=f"table_{value.name}_handler",
                                             handler=selectTableHandler)
                dpg.add_text(value.rowCount, tag=f"count_{tableId.__str__()}")

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