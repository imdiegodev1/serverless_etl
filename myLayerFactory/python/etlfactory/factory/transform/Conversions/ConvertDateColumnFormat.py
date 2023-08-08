import pandas as pd

from etlfactory.factory.transform.abs_transform import AbsTransform


class ConvertDateColumnFormat(AbsTransform):

    def execute(self, dfs: dict, table, parameters):
        try:
            df = dfs[table]
            df['date'] = pd.to_datetime(df['date'])
            return df
        except Exception as e:
            print('Error from ConvertDateColumnFormat', e)