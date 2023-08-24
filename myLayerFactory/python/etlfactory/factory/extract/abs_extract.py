import abc

class AbsExtract(abc.ABC):

    @abc.abstractmethod
    def connect(self):
        pass

    @abc.abstractmethod
    def extract(self):
        pass