from etlfactory.factory.transform.abs_transform import AbsTransform
import pandas as pd

class RemoveColumns(AbsTransform):
    def __init__(self, config, data):
        self.config = config['columns_to_delete']
        self.df = data

    def remove_columns(self):

        df = self.data
        df = df.drop(self.config, axis=1)

        return df