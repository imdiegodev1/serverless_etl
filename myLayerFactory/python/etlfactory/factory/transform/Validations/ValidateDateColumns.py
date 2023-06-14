from ..abs_transform import AbsTransform
import pandas as pd

class ValidateDateColumns(AbsTransform):

    def __init__(self, config, data):
        super().__init__()
        self.date_format = config["date_format"]
        self.columns = config["columns"]
        self.raise_flag = config["raise_flag"]
        self.errors = config["errors"]
        self.df = data

    def execute(self):
        '''
        Validate the date column from a dataframe, wrong values get deleted
        df= dataframe
        columns = list of columns name that need validation
        date_format = format date for to do validation
        '''
        try:
            for column in self.columns:
                self.df[column] = pd.to_datetime(self.df[column], exact = True, errors = self.errors, format = self.date_format)
                if self.raise_flag:
                    index = self.df[self.df[column].isna()].index
                    self.df.loc[index, 'flag'] = self.df.loc[index, 'flag'] + f'Wrong {column} format '
        except Exception as e:
            raise Exception(f"An error occurred while trying to validate and set the date column {e}")

        return self.df

    def transfor_process(self, config, group_criteria):
        pass
