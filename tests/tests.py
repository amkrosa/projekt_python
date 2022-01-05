import unittest
from uuid import uuid4

from application.TableService import TableService
from infrastructure.Repository import Repository


class MyTestCase(unittest.TestCase):
    """
    Tests are done only for "backend" part of the program. Code regarding UI and handling changes in the UI are untested be these test cases.
    """
    def tearDown(self) -> None:
        service = TableService(Repository())
        keys = service.getTables().copy()
        for tableId in keys:
            service.removeTable(tableId)

    def test_shouldAddValidTableAndColumn(self):
        expectedName = "test1"
        service = self.helper_createtest1()
        self.assertEqual(expectedName, service.getTable("test1").name)

    def test_shouldValidAddRow(self):
        row = {"ID": 1, "imie": "Roch", "nazwisko": "Przylbipiet", "wzrost": 1.50}
        tableName = "test1"

        service = self.helper_createtest1()
        service.push(tableName, row)

        result = service.getTable(tableName).rows.get(1).get().values

        self.assertDictEqual(row, result)

    def helper_createtest1(self):
        columns = {
            "ID": "int",
            "imie": "str",
            "nazwisko": "str",
            "wzrost": "float"
        }
        service = TableService(Repository())
        service.addTable(str(uuid4), "test1", columns=columns)
        return service

    def helper_createtest2(self):
        columns = {
            "reserved": "str",
            "kolor": "int"
        }
        service = TableService(Repository())
        service.addTable(str(uuid4), "test1", columns=columns)
        return service


if __name__ == '__main__':
    unittest.main()
