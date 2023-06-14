from ..abs_transform import AbsTransform

class ValidateBooleanColumns(AbsTransform):
    def __init__(self, config, data):
        super().__init__()
        self.columns = config["columns"]
        self.df = data

    def execute(self):
        '''
        Validate the text column from a dataframe, the column element become a string
        df = dataframe
        columns = list of columns name that need validation
        '''
        try:
            for column in self.columns:
                self.df[column] = self.df[column].astype("bool")
        except Exception as e:
            raise Exception(f"An error occurred while trying to validate and set the boolean column {e}")

        return self.df


    def transfor_process(self, config, group_criteria):
        pass
