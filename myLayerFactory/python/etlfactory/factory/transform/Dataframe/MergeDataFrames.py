from etlfactory.factory.transform.abs_transform import AbsTransform
import pandas as pd

class MergeDataFrames(AbsTransform):
    def __init__(self, config, data1, data2):
        self.merge_type = config['merge_type']
        self.left_key = config['left_key']
        self.right_key = config['right_key']
        self.df_left = data1
        self.df_right = data2

    def merge_tables(self):

        df = self.df_left.merge(self.df_right, left_on=self.left_key, right_on=self.right_key, how=self.merge_type)

        return df