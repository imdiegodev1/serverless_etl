import abc

class AbsValidation(abc.ABC):

    @abc.abstractmethod
    def execute(self):
        pass
