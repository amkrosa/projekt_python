import abc

class Column(metaclass=abc.ABCMeta):
    """
    Metaclass for columns. Subclasses should implement method type(self) and cast(self, value) used for type checking
    and casting to column's type.
    """
    def __init__(self, name: str):
        self._row = 0
        if self._validateName(name):
            self.name = name.strip()

    @property
    @abc.abstractmethod
    def type(self):
        raise NotImplementedError

    @abc.abstractmethod
    def cast(self, value):
        raise NotImplementedError

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def _validateName(self, name: str) -> bool:
        """
        Validates if name is a string and does not consists only of whitespaces
        """
        if not isinstance(name, str):
            raise ValueError("Name must be a string")
        if len(name.strip()) == 0:
            raise ValueError("Name cannot consist only of whitespaces")
        return True