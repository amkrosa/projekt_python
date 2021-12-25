import unittest

from domain.Table import Table
from domain.column.IntegerColumn import IntegerColumn
from domain.column.TextColumn import TextColumn


class MyTestCase(unittest.TestCase):
    def test_something(self):
        tab = Table("nazwa")
        tab.addColumn(IntegerColumn("cena"))
        tab["cena"].data = [1,4,5,7,2]
        result = tab["cena"].executeQuery(lambda x: x<3)
        print(result.__str__())
        self.assertEqual(len(result), 2)


if __name__ == '__main__':
    unittest.main()
