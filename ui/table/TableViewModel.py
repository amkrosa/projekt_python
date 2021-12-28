from uuid import uuid4

from domain.Table import Table
from domain.column.IntegerColumn import IntegerColumn
from infrastructure.Repository import Repository
from lib.Observable import Observable
import dearpygui.dearpygui as dpg
from ui.table.TableView import TableView


class TableViewModel:
    def __init__(self, root):
        self.__root = root
        self.__repository = Repository()
        self.__tableView = TableView(root)
        self.__tableView.setRegistry(itemTag=self.__tableView.addTableButton, handlerTag="addButtonHandler",
                                     handler=self.handleAddTable)

    def handleAddTable(self):
        val: str = self.__tableView.addTableInputValue()
        if self.__repository.findByName(val) is not None:
            self.__tableView.errorPopup(text="Taki element juz istnieje")
            return
        if len(val.strip()) == 0:
            self.__tableView.errorPopup(text="Pole nie może być puste")
            return

        id, data = self.__tableView.addRow()
        self.__tableView.setRegistry(itemTag=id, handlerTag=f"table_{data}_handler", handler=self.handleSelectTable)
        table = Table(data, id)
        table.setNameCallback(self.handleTableNameChanged)
        self.__repository.add(table, id=id)

    def handleSelectTable(self, sender, app_data):
        tableId = app_data[1]
        tab = Table("tabela", uuid4().__str__())
        col = IntegerColumn("kolumna")
        col2 = IntegerColumn("druga")
        tab.addColumn(col)
        tab.addColumn(col2)
        tab.push({
            "kolumna": 1,
            "druga": 9
        })
        tab.push({
            "kolumna": 5,
            "druga": 6
        })
        self.__tableView.setColumns(columns=tab.columns, rows=tab.rowCount, data=tab.rows)
        print(tab.__str__())

    def handleTableNameChanged(self, data, uuid):
        self.__tableView.changeRow(tag=uuid, data=data)
