from etlfactory.factory.transform.abs_transform import AbsTransform
import pandas as pd
from datetime import datetime

class ExplodeDates (AbsTransform):

    def execute(self,  dfs: dict, table, parameters):

        df = dfs[table]

        '''
        Validate the text column from a dataframe, the column element become a string
        df = dataframe
        columns = list of columns name that need validation
        '''
        try:
            df[parameters["new_column"]] = df.apply(lambda row: pd.date_range(row[parameters["start_column"]], row[parameters["end_column"]], freq='D'), axis=1)
            df = df.explode(parameters["new_column"])
            startdate = pd.to_datetime("2022-01-01").date().strftime('%Y-%m-%d')
            today = datetime.today().strftime('%Y-%m-%d')
            df = df[df[parameters["new_column"]].between(startdate, today, inclusive=True)]

        except Exception as e:
            raise Exception(f"An error occurred while trying to validate and set the float column {e}")

        return df
