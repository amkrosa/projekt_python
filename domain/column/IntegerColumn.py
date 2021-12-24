from domain.column.Column import Column


class IntegerColumn(Column):
    def __init__(self, name):
        super().__init__(name)
        self.__data: dict[int, int] = dict()

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, *data):
        for element in data:
            if isinstance(element, int):
                self.__data[super().nextRow()] = element
            else:
                raise TypeError("IntegerColumn may consists only of integers")