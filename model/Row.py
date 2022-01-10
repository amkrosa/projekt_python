class Row:
    """
    Row class holding dictionary with row data
    """
    def __init__(self, data):
        self.__data: dict = data

    def __iter__(self):
        return iter(self.__data)

    @property
    def values(self):
        return self.__data

    def addValue(self, column, value):
        """
        Adds specified value to a column in the row
        """
        self.__data[column] = value

    def __getitem__(self, columnName: str):
        return self.__data[columnName]

    def __repr__(self):
        return str(self.__data)