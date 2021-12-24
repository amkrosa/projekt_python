import abc

class Column(metaclass=abc.ABCMeta):
    def __init__(self, name: str):
        if (self.validateName(name)):
            self.__name = name.strip()

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'load_data_source') and
                callable(subclass.load_data_source) and
                hasattr(subclass, 'extract_text') and
                callable(subclass.extract_text) or
                NotImplemented)

    @property
    @abc.abstractmethod
    def data(self):
        """Get dictionary containing data for specified column"""
        raise NotImplementedError

    @data.setter
    @abc.abstractmethod
    def data(self, *data):
        """Write dictionary containing data for specified column"""
        raise NotImplementedError

    def validateName(self, name: str) -> bool:
        if not isinstance(name, str):
            raise ValueError("Name must be a string")
        if len(name.strip()) == 0:
            raise ValueError("Name cannot consist only of whitespaces")

    def nextRow(self):
        row=0
        while True:
            yield row
            row+=1


