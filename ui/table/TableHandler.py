import logging
from uuid import uuid4

from application.TableService import TableService
from model.Table import Table
from model.Repository import Repository

from ui.root.RootView import RootView
from ui.table.TableView import TableView
from ui.widgets.AddTableModal import AddTableModal
from ui.widgets.ConfirmationModal import ConfirmationModal

logger = logging.getLogger(__name__)


class TableViewModel:
    def __init__(self, root: RootView):
        self.__repository = Repository()
        self.__tableService = TableService(self.__repository)

        #if repository is loaded from a file (so it's length is not 0) then add callbacks for Repository object
        #and Table objects
        if len(self.__repository) != 0:
            self.__repository.addCallback(self.refreshTables)
            for table in self.__repository.repository.values():
                table.addCallback(self.refreshTableRows)
                table.setNameCallback(self.handleTableNameChanged)
                table.setRowsCountCallback(self.handleRowsCountChanged)

        self.__tableView = TableView(root, addTableCallback=self.handleOpenAddTable,
                                     addColumnCallback=self.handleAddColumn, querySearchCallback=self.handleQuerySearch,
                                     refreshCallback=lambda sender, app_data, user_data: self.refreshTableRows())

        self.__tableView.setRegistry(itemTag=self.__tableView.addTableButton, handlerTag="addButtonHandler",
                                     handler=self.handleOpenAddTable)
        self.__tableView.setRegistry(itemTag="addColumnButton", handlerTag="addColumnHandler",
                                     handler=self.handleAddColumn)
        self.refreshTables()

    @property
    def view(self):
        return self.__tableView

    @property
    def currentTable(self):
        return self.__repository.findByName(self.__tableView.currentTableSelection)

    def handleOpenAddTable(self):
        """
        Opens add table modal
        """
        self.__tableView.addTableModal(callback=self.handleConfirmCreateTable, afterCallback=self.handleAddTable)

    def handleAddTable(self, data):
        """
        Handles click on addTableButton. Called from confirmation modal after clicking OK.
        """
        tableId = uuid4().__str__()
        name = data["name"]
        self.__tableService.addTable(tableId=tableId, name=name, nameCallback=self.handleTableNameChanged,
                                     rowsCallback=self.handleRowsCountChanged,
                                     refreshCallback=self.refreshTableRows, columns=data["columns"])

    def handleSelectTable(self, sender, app_data, user_data):
        """
        Selects clicked table.

        Args:
            sender (str): tag of the item that had callback
            user_data (Callable): TableView.__clearTableSelection, which clears table selection regarding Selectable element
        """
        tableId = sender.split("_")[1]
        tab = self.__tableService.getTableById(tableId=tableId)
        user_data(tableId)
        self.refreshTableRows(tab)

    def handleAddColumn(self):
        """
        Adds column after table creation
        """
        columnName, columnType = self.__tableView.addColumn()
        col = TableService.createColumn(columnName, columnType)
        tableName = self.currentTable.name
        self.__tableService.addColumn(tableName=tableName, column=col)

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
        for col in self.__tableService.getColumns(tab.name).values():
            try:
                row[col.name] = col.cast(values[col.name])
            except TypeError:
                self.__tableView.errorPopup(itemTag="addRowButton",
                                            text=f"Wartosc {values[col.name]} ma niepoprawny typ")
                return
        self.__tableService.push(tab.name, row)

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
            user_data["after"](user_data["data"]["tableName"], user_data["data"]["row"])

    def handleConfirmDeleteTable(self, sender, app_data, user_data):
        """Handles click on button in ConfirmationModal regarding table deletion. Clicking OK will send
        user_data["confirmation"]=True and execute callback contained in user_data. Checks also if deleted table is the
        current one, if True then it also hides displayed table rows.

        Args:
        	user_data (dict): dictionary with modal object, confirmation boolean, callback function if confimred and data if confirmed
        Returns:
        	None
        """
        modal: ConfirmationModal = user_data["modal"]
        modal.close()
        if user_data["confirmation"]:
            if user_data["data"]["currentTable"] == self.__repository[user_data["data"]["id"]].name:
                self.refreshTableRows(hide=True)
            user_data["after"](user_data["data"]["id"])

    def handleConfirmCreateTable(self, sender, app_data, user_data):
        """Handles click on button in AddTableModal. Clicking OK will send user_data["confirmation"]=True and execute callback contained in user_data.

        Args:
        	user_data (dict): dictionary with modal object, confirmation boolean, callback function if confirmed and data if confirmed
        Returns:
        	None
        """
        modal: AddTableModal = user_data["modal"]

        if user_data["confirmation"]:
            try:
                Table(modal.form["name"], None)
            except ValueError:
                self.__tableView.errorPopup(itemTag="createTableButton_modal",
                                            text=f"Nazwa tabeli jest niepoprawna", modal="createTable_modal")
                return
            user_data["after"](modal.form)
        modal.close()

    def handleDeleteRow(self, sender, app_data, user_data):
        """Handles click on deleteRowButton, which displays ConfirmationModal.

        Args:
        	user_data (dict): dictionary with row number
        Returns:
        	None
        """
        row = user_data["row"] - 1
        tab = self.currentTable
        self.__tableView.confirmationModal("Czy aby napewno?", self.handleConfirm, self.__tableService.pop,
                                           {"row": row, "tableName": tab.name})

    def handleQuerySearch(self, sender, app_data, user_data):
        """Handles click on querySearchButton, which filters data via TableService.query.

        Args:
        	user_data (dict): dictionary with keys dataCallback (function to get data with) and data (tag of element)
        Returns:
        	None
        """
        query = user_data["dataCallback"](user_data["data"])
        logger.debug(f"Executing: {query}...")
        tab = self.currentTable
        try:
            data = self.__tableService.query(tab.name, eval(query))
        except Exception as e:
            self.__tableView.errorPopup(itemTag="querySearchButton", text="Niepoprawne wyrazenie")
            logger.debug(f"{e.__str__()}")
            return

        self.refreshTableRows(data=data)

    def handleTableNameChanged(self, data, uuid):
        self.__tableView[uuid] = data

    def handleRowsCountChanged(self, data, uuid):
        self.__tableView[f"count_{uuid}"] = data

    def handleDeleteTable(self, sender, app_data, user_data):
        """Handles click on deleteTableButton, which displays ConfirmationModal.

        Args:
        	user_data (dict): dictionary with table id and currently selected table
        Returns:
        	None
        """
        id = user_data["id"]
        tab = user_data["currentTable"]
        self.__tableView.confirmationModal("Czy aby napewno?", self.handleConfirmDeleteTable,
                                           self.__tableService.removeTable,
                                           {"id": id, "currentTable": tab()})

    def refreshTableRows(self, table=None, data=None, hide=False):
        """
        Calls setColumns method from view with current or specified rows data

        Args:
        	table (Table): table object, defaults to current table
        	data (dict): dictionary containing row data
        	hide (bool): specifies if method should hide row section of application
        """
        logging.debug("refreshTableRows called")
        if hide:
            self.__tableView.hideColumns()
            return
        tab = self.currentTable if table is None else table
        self.__tableView.setRows(tab, tab.rows if data is None else data,
                                 addRowHandler=self.handleAddRow, deleteRowHandler=self.handleDeleteRow)

    def refreshTables(self):
        """
        Calls setTables method from view with current Table data
        """
        logging.debug("refreshTables called")
        self.__tableView.setTables(self.__tableService.getTables(), selectTableHandler=self.handleSelectTable,
                                   deleteTableHandler=self.handleDeleteTable)
