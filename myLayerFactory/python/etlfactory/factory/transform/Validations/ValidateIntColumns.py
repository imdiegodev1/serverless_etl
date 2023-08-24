from etlfactory.factory.transform.abs_transform import AbsTransform
import pandas as pd

class ValidateIntColumns(AbsTransform):
    def __init__(self, config, data):
        super().__init__()
        self.columns = config["columns"]
        self.errors = config["errors"]
        self.df = data

    def execute(self):
        '''
        Validate the text column from a dataframe, the column element become a string
        df = dataframe
        columns = list of columns name that need validation
        '''
        try:
            for column in self.columns:

                self.df[column] = pd.to_numeric(self.df[column], errors = self.errors)

        except Exception as e:
            raise Exception(f"An error occurred while trying to validate and set the integer column {e}")

        return self.df

    def transfor_process(self, config, group_criteria):
        pass
