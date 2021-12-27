from domain.Table import Table
from infrastructure.Repository import Repository
from lib.Observable import Observable
import dearpygui.dearpygui as dpg
from ui.table.TableView import TableView


class TableViewModel:
    def __init__(self, root):
        self.__root = root
        self.__repository = Repository()
        self.__tableView = TableView(root)
        self.__tableView.setAddTableRegistry(handler=self.handleAddTable)

    def handleAddTable(self):
        print(self.__repository.findByName("tabela"))
        if self.__repository.findByName("tabela") is not None:
            self.__tableView.errorPopup(parent=self.__tableView.addTableButton,
                                        text="Taki element juz istnieje")
            return
        id = self.__tableView.addRow("tabela")
        table = Table("tabela", id)
        table.setNameCallback(self.handleTableNameChanged)
        self.__repository.add(table, id=id)

    def handleTableNameChanged(self, data, uuid):
        self.__tableView.changeRow(tag=uuid, data=data)
