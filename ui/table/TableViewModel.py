import json
import logging
import uuid
from json import JSONEncoder
from uuid import uuid4

from application.ColumnService import ColumnService
from application.TableService import TableService
from domain.Table import Table
from domain.column.Column import Column
from domain.column.FloatColumn import FloatColumn
from domain.column.IntegerColumn import IntegerColumn
from domain.column.TextColumn import TextColumn
from infrastructure.Repository import Repository
from infrastructure.json.Encoder import Encoder
from lib.Observable import Observable
import dearpygui.dearpygui as dpg

from ui.root.RootView import RootView
from ui.table.TableView import TableView

logger = logging.getLogger(__name__)


class TableViewModel:
    def __init__(self, root: RootView):
        self.__repository = Repository()
        self.__tableService = TableService(self.__repository.repository)
        self.__tableView = TableView(root, addTableCallback=self.handleOpenAddTable,
                                     addColumnCallback=self.handleAddColumn)
        self.__tableView.setRegistry(itemTag=self.__tableView.addTableButton, handlerTag="addButtonHandler",
                                     handler=self.handleOpenAddTable)
        self.__tableView.setRegistry(itemTag="addColumnButton", handlerTag="addColumnHandler",
                                     handler=self.handleAddColumn)
        self.__tableView.setRegistry(itemTag="querySearchButton", handlerTag="querySearchHandler",
                                     handler=self.handleQuerySearch)
        self.__tableView.setTables(self.__repository.repository, selectTableHandler=self.handleSelectTable)

    @property
    def currentTable(self):
        return self.__repository.findByName(self.__tableView.currentTableSelection)

    def handleOpenAddTable(self):
        # val: str = self.__tableView.addTableInputValue()
        # if self.__repository.findByName(val) is not None:
        #     self.__tableView.errorPopup(itemTag="addTableButton", text="Taki element juz istnieje")
        #     return
        # if len(val.strip()) == 0:
        #     self.__tableView.errorPopup(itemTag="addTableButton", text="Pole nie może być puste")
        #     return
        self.__tableView.addTableModal(callback=self.handleConfirmCreateTable, afterCallback=self.handleAddTable)

    def handleAddTable(self, data):
        tableId = uuid4()
        name = data["name"]
        table = Table(name, tableId)
        table.setNameCallback(self.handleTableNameChanged)
        table.setRowsCountCallback(self.handleRowsCountChanged)
        print([(columnName, columnType) for columnName, columnType in data["columns"].items()])
        [table.addColumn(ColumnService.createColumn(columnName, columnType)) for columnName, columnType in data["columns"].items()]
        self.__tableView.addTable(name, tableId.__str__())
        self.__repository.add(table, id=tableId.__str__())
        self.__tableView.setRegistry(itemTag=tableId.__str__(), handlerTag=f"table_{data['name']}_handler", handler=self.handleSelectTable)

    def handleSelectTable(self, sender, app_data):
        tableId = app_data[1]
        t = self.__repository[tableId]
        self.refreshTableRows(t)

    def handleAddColumn(self):
        columnName, columnType = self.__tableView.addColumn()
        col = ColumnService.createColumn(columnName, columnType)
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

    #klikam guzik usunięcia
    #wywoluje sie callback guziku usuniecia (handleDeleteRow)
    #klikam OK, wywoluje sie callback guziku OK (handleConfirmationModal)
    #chce przekazac dane do

    def handleConfirm(self, sender, app_data, user_data):
        self.__tableView.closeModal("confirmation_modal")
        if user_data["confirmation"]:
            user_data["after"](user_data["data"])
            self.refreshTableRows(self.currentTable)

    def handleConfirmCreateTable(self, sender, app_data, user_data):
        self.__tableView.closeModal("createTable_modal")
        if user_data["confirmation"]:
            user_data["after"](self.__tableView.addTableForm)
            self.refreshTables()

    def handleDeleteRow(self, sender, app_data, user_data):
        row = user_data["row"]-1
        tab = self.currentTable
        self.__tableView.confirmationModal("Czy aby napewno?", self.handleConfirm, tab.remove, row)

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
    def refreshTables(self):
        self.__tableView.setTables(self.__repository.repository, selectTableHandler=self.handleSelectTable)
