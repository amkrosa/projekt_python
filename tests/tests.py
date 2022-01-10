import unittest
from uuid import uuid4

from application.TableService import TableService
from model.Repository import Repository


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
        """
        Creates a table named test1 with 4 columns. Realizes tests number 1 from project description.
        """

        expectedName_1 = "test1"
        expectedName_2 = "test2"
        service_1 = self.helper_createtest1()
        service_2 = self.helper_createtest2()
        self.assertEqual(expectedName_1, service_1.getTable("test1").name)
        self.assertEqual(expectedName_2, service_2.getTable("test2").name)


    def test_shouldAddValidRow(self):
        """
        Creates three rows and adds two of them to table test1 and one of them to table test2. Realizes tests number 2, 3 and 9 from project description.
        """
        #given
        service_1 = self.helper_createtest1()
        service_2 = self.helper_createtest2()
        input_row_1 = {"ID": "1", "imie": "Roch", "nazwisko": "Przylbipiet", "wzrost": "1.50"}
        input_row_2 = {"ID": "2", "imie": "Ziemniaczyslaw", "nazwisko": "Bulwiasty", "wzrost": "1.91"}
        input_row_3 = {"reserved": "", "kolor": "1337"}

        expected_row_1 = {"ID": 1, "imie": "Roch", "nazwisko": "Przylbipiet", "wzrost": 1.5}
        expected_row_2 = {"ID": 2, "imie": "Ziemniaczyslaw", "nazwisko": "Bulwiasty", "wzrost": 1.91}
        expected_row_3 = {"reserved": "", "kolor": 1337}

        tableName_1 = "test1"
        tableName_2 = "test2"

        #when
        service_1.push(tableName_1, input_row_1)
        service_1.push(tableName_1, input_row_2)
        service_2.push(tableName_2, input_row_3)

        #then
        result_1 = service_1.getTable(tableName_1).rows.get(1).get().values
        result_2 = service_1.getTable(tableName_1).rows.get(2).get().values
        result_3 = service_2.getTable(tableName_2).rows.get(1).get().values

        self.assertDictEqual(expected_row_1, result_1)
        self.assertDictEqual(expected_row_2, result_2)
        self.assertDictEqual(expected_row_3, result_3)

    def test_shouldNotAddInvalidRowWhenTypeIsIncorrect(self):
        """
        Tries to add invalid rows, expecting failure. Realizes tests number 4, 5 and 10 from project description.
        """
        #given
        service_1 = self.helper_createtest1()
        service_2 = self.helper_createtest2()
        row_1 = {"ID": "cztery", "imie": "bla", "nazwisko": "bla", "wzrost": "-90"}
        row_2 = {"ID": "3.14", "imie": "pi", "nazwisko": "ludolfina", "wzrost": "314e-2"}
        row_3 = {"reserved": "bla", "kolor": "1939b"}
        tableName_1 = "test1"
        tableName_2 = "test2"

        #when-then
        with self.assertRaises(TypeError):
            service_1.push(tableName_1, row_1)

        with self.assertRaises(TypeError):
            service_1.push(tableName_1, row_2)

        with self.assertRaises(TypeError):
            service_2.push(tableName_2, row_3)

    def test_shouldNotAddTableWithEmptyName(self):
        """
        Tries to create invalid tables, expecting failure. Realizes tests number 12 and 13 from project description.
        """
        #given
        service = TableService(Repository())
        tableId = str(uuid4())

        #when-then
        with self.assertRaises(ValueError):
            service.addTable(tableId=tableId, name="")
        with self.assertRaises(ValueError):
            service.addTable(tableId=tableId, name=" ")

    def test_shouldNotAddColumnWithEmptyField(self):
        """
        Creates two rows and adds them to table test1, expecting failure. Realizes tests number 14 and 15 from project description.
        """
        self.helper_query()
        #given
        service = TableService(Repository())
        tableId = str(uuid4())

        column_empty = {
            "": "int"
        }

        column_space = {
            "": "int"
        }

        #when-then
        with self.assertRaises(ValueError):
            service.addTable(tableId=tableId, name="tabela", columns=column_empty)
        with self.assertRaises(ValueError):
            service.addTable(tableId=tableId, name="tabela", columns=column_space)

    def test_shouldQueryRows(self):
        """
        Checks query functionality. Realizes partially test number 16 from project description.
        """
        #given
        service = self.helper_query()
        expectedRows = str({i: {"ID": i, "imie": f"Imie{i-1}", "nazwisko": f"Przylbipiet{i-1}", "wzrost": float(f"1.{i-1}")} for i in range(2, 12, 2)})


        #when
        result = str(service.query("test1", lambda row: row["ID"] % 2 == 0))

        #then
        self.assertEqual(result, expectedRows)


    def helper_createtest1(self):
        """
        Helper method for creating test1 table
        """
        columns = {
            "ID": "int",
            "imie": "str",
            "nazwisko": "str",
            "wzrost": "float"
        }
        service = TableService(Repository())
        tableId = str(uuid4())
        service.addTable(tableId, "test1", columns=columns)
        return service

    def helper_createtest2(self):
        """
        Helper method for creating test2 table
        """
        columns = {
            "reserved": "str",
            "kolor": "int"
        }
        service = TableService(Repository())
        tableId = str(uuid4())
        service.addTable(tableId, "test2", columns=columns)
        return service

    def helper_query(self):
        """
        Helper method for query test
        """
        service = self.helper_createtest1()
        rows = [{"ID": i+1, "imie": f"Imie{i}", "nazwisko": f"Przylbipiet{i}", "wzrost": f"1.{i}"} for i in range(10)]
        for row in rows:
            service.push("test1", row)
        return service



if __name__ == '__main__':
    unittest.main()
