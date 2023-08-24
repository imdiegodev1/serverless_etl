import abc

class AbsFactory(abc.ABC):

    @abc.abstractmethod
    def extract_method(self):
        pass
    @abc.abstractmethod
    def transform_method(self):
        pass
    @abc.abstractmethod
    def load_method(self):
        pass