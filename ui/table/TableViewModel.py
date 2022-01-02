import json
import logging
import uuid
from json import JSONEncoder
from uuid import uuid4

from application.ColumnService import ColumnService
from application.TableService import TableService
from model.Table import Table
from model.column.Column import Column
from model.column.FloatColumn import FloatColumn
from model.column.IntegerColumn import IntegerColumn
from model.column.TextColumn import TextColumn
from infrastructure.Repository import Repository
from infrastructure.json.Encoder import Encoder
from lib.Observable import Observable
import dearpygui.dearpygui as dpg

from ui.root.RootView import RootView
from ui.table.TableView import TableView
from ui.widgets.AddTableModal import AddTableModal
from ui.widgets.ConfirmationModal import ConfirmationModal

logger = logging.getLogger(__name__)


class TableViewModel:
    def __init__(self, root: RootView):
        self.__repository = Repository()
        self.__tableService = TableService(self.__repository.repository)

        if len(self.__repository) != 0:
            for table in self.__repository.repository.values():
                table.setNameCallback(self.handleTableNameChanged)
                table.setRowsCountCallback(self.handleRowsCountChanged)

        self.__tableView = TableView(root, addTableCallback=self.handleOpenAddTable,
                                     addColumnCallback=self.handleAddColumn)
        self.__tableView.setRegistry(itemTag=self.__tableView.addTableButton, handlerTag="addButtonHandler",
                                     handler=self.handleOpenAddTable)
        self.__tableView.setRegistry(itemTag="addColumnButton", handlerTag="addColumnHandler",
                                     handler=self.handleAddColumn)
        self.__tableView.setRegistry(itemTag="querySearchButton", handlerTag="querySearchHandler",
                                     handler=self.handleQuerySearch)
        self.refreshTables()

    @property
    def view(self):
        return self.__tableView

    @property
    def currentTable(self):
        return self.__repository.findByName(self.__tableView.currentTableSelection)

    def handleOpenAddTable(self):
        self.__tableView.addTableModal(callback=self.handleConfirmCreateTable, afterCallback=self.handleAddTable)

    def handleAddTable(self, data):
        tableId = uuid4().__str__()
        name = data["name"]
        table = Table(name, tableId)
        table.setNameCallback(self.handleTableNameChanged)
        table.setRowsCountCallback(self.handleRowsCountChanged)
        [table.addColumn(ColumnService.createColumn(columnName, columnType)) for columnName, columnType in
         data["columns"].items()]
        self.__repository.add(table, id=tableId)
        self.refreshTables()
        self.__tableView.setRegistry(itemTag=tableId, handlerTag=f"table_{data['name']}_handler",
                                     handler=self.handleSelectTable)

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

    def handleAddRow(self, sender, app_data, user_data):
        """	Handles click on addRow button. Displays popup on error

        Args:
        	user_data (Callable): callback function that returns input row as dictionary
        Returns:
        	None
        """
        values = user_data()
        tab: Table = self.currentTable
        row = {}
        for index, col in enumerate(tab.columns.values()):
            try:
                row[col.name] = col.cast(values[col.name])
            except TypeError:
                self.__tableView.errorPopup(itemTag="addRowButton",
                                            text=f"Wartosc {values[col.name]} ma niepoprawny typ")
                return
        tab.push(row)
        self.refreshTableRows(tab)

    def handleConfirm(self, sender, app_data, user_data):
        """Handles click on button in ConfirmationModal. Clicking OK will send user_data["confirmation"]=True and execute callback contained in user_data.

        Args:
        	user_data (dict): dictionary with modal object, confirmation boolean, callback function if confimred and data if confirmed
        Returns:
        	None
        """
        modal: ConfirmationModal = user_data["modal"]
        modal.close()
        if user_data["confirmation"]:
            user_data["after"](user_data["data"])
            self.refreshTableRows(self.currentTable)

    def handleConfirmCreateTable(self, sender, app_data, user_data):
        """Handles click on button in AddTableModal. Clicking OK will send user_data["confirmation"]=True and execute callback contained in user_data.

        Args:
        	user_data (dict): dictionary with modal object, confirmation boolean, callback function if confirmed and data if confirmed
        Returns:
        	None
        """
        modal: AddTableModal = user_data["modal"]
        modal.close()
        if user_data["confirmation"]:
            user_data["after"](modal.form)
            self.refreshTables()

    def handleDeleteRow(self, sender, app_data, user_data):
        """Handles click on deleteRowButton, which displays ConfirmationModal.

        Args:
        	user_data (dict): dictionary with row number
        Returns:
        	None
        """
        row = user_data["row"] - 1
        tab = self.currentTable
        self.__tableView.confirmationModal("Czy aby napewno?", self.handleConfirm, tab.remove, row)

    def handleQuerySearch(self):
        """Handles click on querySearchButton, which filters data via TableService.query.

        Args:
        	user_data (str): current query search
        Returns:
        	None
        """
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
