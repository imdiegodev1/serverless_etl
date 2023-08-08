from abc import ABC, abstractmethod


class AbsLoad(ABC):

    @abstractmethod
    def load(self):
        pass