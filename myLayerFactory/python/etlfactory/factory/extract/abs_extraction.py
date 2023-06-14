from abc import ABC, abstractmethod

class AbsExtraction(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def extract(self):
        pass