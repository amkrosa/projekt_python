import logging
from uuid import uuid4

from application.TableService import TableService
from domain.Table import Table
from domain.column.FloatColumn import FloatColumn
from domain.column.IntegerColumn import IntegerColumn
from domain.column.TextColumn import TextColumn
from infrastructure.Repository import Repository
from lib.Observable import Observable
import dearpygui.dearpygui as dpg
from ui.table.TableView import TableView

logger = logging.getLogger(__name__)


class TableViewModel:
    def __init__(self, root):
        self.__root = root
        self.__repository = Repository()
        self.__tableService = TableService(self.__repository)
        self.__tableView = TableView(root, addTableCallback=self.handleAddTable, addColumnCallback=self.handleAddColumn)
        self.__tableView.setRegistry(itemTag=self.__tableView.addTableButton, handlerTag="addButtonHandler",
                                     handler=self.handleAddTable)
        self.__tableView.setRegistry(itemTag="addColumnButton", handlerTag="addColumnHandler",
                                     handler=self.handleAddColumn)
        self.__tableView.setRegistry(itemTag="querySearchButton", handlerTag="querySearchHandler",
                                     handler=self.handleQuerySearch)

    @property
    def currentTable(self):
        return self.__repository.findByName(self.__tableView.currentTableSelection)

    def handleAddTable(self):
        val: str = self.__tableView.addTableInputValue()
        if self.__repository.findByName(val) is not None:
            self.__tableView.errorPopup(itemTag="addTableButton", text="Taki element juz istnieje")
            return
        if len(val.strip()) == 0:
            self.__tableView.errorPopup(itemTag="addTableButton", text="Pole nie może być puste")
            return

        id, data = self.__tableView.addTable()
        self.__tableView.setRegistry(itemTag=id, handlerTag=f"table_{data}_handler", handler=self.handleSelectTable)
        table = Table(data, id)
        table.setNameCallback(self.handleTableNameChanged)
        table.setRowsCountCallback(self.handleRowsCountChanged)
        self.__repository.add(table, id=id)

    def handleSelectTable(self, sender, app_data):
        tableId = app_data[1]
        t = self.__repository[tableId]
        self.refreshTableRows(t)

    def handleAddColumn(self):
        columnName, columnType = self.__tableView.addColumn()
        col = None

        if columnType == "str":
            col = TextColumn(columnName)
        elif columnType == "int":
            col = IntegerColumn(columnName)
        elif columnType == "float":
            col = FloatColumn(columnName)
        else:
            raise RuntimeError(f"Unexpected error has occured. Column type is: {columnType}")

        tab = self.currentTable
        tab.addColumn(col)
        self.refreshTableRows(tab)

    def handleAddRow(self):
        values = self.__tableView.readRowInput()
        tab = self.currentTable
        row = {}
        for index, col in enumerate(tab.columns.values()):
            try:
                row[col.name] = col.cast(values[col.name])
            except TypeError:
                self.__tableView.errorPopup(itemTag="addRowButton", text=f"Wartosc {values[col.name]} ma niepoprawny typ")
                return
        tab.push(row)
        self.refreshTableRows(tab)

    def handleDeleteRow(self, sender, app_data, user_data):
        row = user_data["row"]


    def handleQuerySearch(self):
        query = self.__tableView.currentQuerySearch
        tab = self.currentTable
        try:
            data = self.__tableService.query(tab.name, eval(query))
        except Exception as e:
             self.__tableView.errorPopup(itemTag="querySearchButton", text="Niepoprawne wyrazenie")
             logger.debug(f"{e.__str__()}")
             return

        self.refreshTableRows(tab, data)

    def handleTableNameChanged(self, data, uuid):
        self.__tableView[uuid] = data

    def handleRowsCountChanged(self, data, uuid):
        self.__tableView[f"count_{uuid}"] = data

    def refreshTableRows(self, tab: Table, data=None):
        self.__tableView.setColumns(tab, tab.rows if data is None else data,
                                    addRowHandler=self.handleAddRow, deleteRowHandler=self.handleDeleteRow)