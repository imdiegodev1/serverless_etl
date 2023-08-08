import abc
import numpy as np
import pandas as pd
import re

class AbsTransform(abc.ABC):

    def __init__(self, log_group='DSI-Pipelines', log_stream='Transform') -> None:
        self.log_group = log_group
        self.log_stream = log_stream

    @abc.abstractmethod
    def execute(self):
        pass
