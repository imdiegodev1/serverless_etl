from etlfactory.factory.transform.abs_transform import AbsTransform
import pandas as pd

class ValidateTextColumns(AbsTransform):

    def execute(self, dfs: dict, table, parameters):

        #self.columns = config["columns"]
        df = dfs[table]
        '''
        Validate the text column from a dataframe, the column element become a string
        df = dataframe
        columns = list of columns name that need validation
        '''
        try:
            for column in parameters["columns"]:
                df[column] = df[column].astype("str")
        except Exception as e:
            raise Exception(f"An error occurred while trying to validate and set the text column {e}")

        return df
