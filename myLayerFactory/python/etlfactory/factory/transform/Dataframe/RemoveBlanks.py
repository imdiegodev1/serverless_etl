from etlfactory.factory.transform.abs_transform import AbsTransform
import pandas as pd

class RemoveBlanks(AbsTransform):
    def __init__(self, config, data):
        self.removing_type = config['removing_type']
        self.df = data

    def execute(self):

        df = self.df

        if self.removing_type == 'all':

            df = df.dropna()
            return df

        else:
            df = df.dropna(subset=self.removing_type)