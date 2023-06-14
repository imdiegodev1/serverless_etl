from ..abs_transform import AbsTransform
import pandas as pd

class ValidateDurationColumns(AbsTransform):
    def __init__(self, config, data):
        super().__init__()
        self.columns = config["columns"]
        self.hour_format = config["hour_format"]
        self.raise_flag = config["raise_flag"]
        self.errors = config["errors"]
        self.df = data

    def execute(self):
        '''
        Validate the duration columns from a dataframe, wrong values get deleted
        df = dataframe
        column = column name that need validation [LIST]
        hour_format = format time duration for to do validation
        '''
        try:
            for column in self.columns:
                self.df[column] = pd.to_datetime(self.df[column], exact=False, errors = self.errors, format = self.hour_format)
                if self.raise_flag:
                        index=self.df[self.df[column].isna()].index
                        self.df.loc[index, 'flag'] = self.df.loc[index, 'flag'] + f'Wrong {column} format '
        except Exception as e:
            raise Exception(f"An error occurred while trying to validate duration column {e}")

        return self.df

    def transfor_process(self, config, group_criteria):
        pass
