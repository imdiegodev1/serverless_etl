import abc
import numpy as np
import pandas as pd
import re

class AbsTransform(abc.ABC):

    @abc.abstractmethod
    def execute(self):
        pass
