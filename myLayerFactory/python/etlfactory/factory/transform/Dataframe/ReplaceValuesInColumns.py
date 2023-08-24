import pandas as pd
import numpy as np
from etlfactory.factory.transform.abs_transform import AbsTransform

class ReplaceValuesInColumns(AbsTransform):

    def execute(self, dfs: dict, table, parameters):
        try:
            df = dfs[table]
            print(df.head(10))
            for replace in parameters:
                for cols in parameters[replace]['columns']:
                    df[cols] = df[cols].str.replace(parameters[replace]['replace_this'],
                                                    parameters[replace]['for_this'])
            print(df.head(10))
        except Exception as e:
            raise Exception(f"An error occurred while trying to replace values in columns. {e}")

        return df

    def transfor_process(self, config, group_criteria):
        pass
