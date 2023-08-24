from etlfactory.factory.transform.abs_transform import AbsTransform
import numpy as np

class ValidateConvertDurationColumnsRegex(AbsTransform):
    def __init__(self, config, data):
        super().__init__()
        self.columns = config["columns"]
        self.regex = config["regex"]
        self.raise_flag = config["raise_flag"]
        self.df = data

    def validate_and_convert_duration_time_to_sec(x: str, regex: str = '(^\d+\.?\d*):(\d+\.?\d*):(\d+\.?\d*)'):
        if type(x) != str:
            return np.nan
        res = re.findall(regex, x)
        if  len(res) == 0:
            return np.nan

        res = res[0]
        res_len = len(res)
        match res_len:
            case 3:
                hour = float(res[0])
                minute = float(res[1])
                second = float(res[2])
                return hour*3600 + minute*60 + second
            case 2:
                minute = float(res[0])
                second = float(res[1])
                return minute*60 + second
            case 1:
                second = float(res[0])
                return second
            case _:
                return np.nan

    def execute(self):
        '''
        Validate the duration columns from a dataframe, wrong values get deleted
        df = dataframe
        column = column name that need validation [LIST]
        regex = string for search match patterns and get hours, minutes and seconds
        '''
        try:
            for column in self.columns:
                self.df[column] = self.df[column].apply(lambda x: self.validate_and_convert_duration_time_to_sec(x, regex = self.regex))
                if self.raise_flag:
                        index=self.df[self.df[column].isna()].index
                        self.df.loc[index, 'flag'] = self.df.loc[index, 'flag'] + f'Wrong {column} format '
        except Exception as e:
            raise Exception(f"An error occurred while trying to validate duration column {e}")

        return self.df

    def transfor_process(self, config, group_criteria):
        pass
