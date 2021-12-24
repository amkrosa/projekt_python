import abc

class Column(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'load_data_source') and
                callable(subclass.load_data_source) and
                hasattr(subclass, 'extract_text') and
                callable(subclass.extract_text) or
                NotImplemented)
    @classmethod
    @abc.abstractmethod
    def getData(cls):
        """Get dictionary containing data for specified column"""
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def writeData(cls, data):
        """Write dictionary containing data for specified column"""
        raise NotImplementedError

