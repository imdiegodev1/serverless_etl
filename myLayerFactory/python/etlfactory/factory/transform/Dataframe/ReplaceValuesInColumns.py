from ..abs_transform import AbsTransform

class ReplaceValuesInColumns(AbsTransform):
    def __init__(self, config, data):
        super().__init__()
        self.replace_list = config["replace_list"]
        self.regex = config["regex"]
        self.df = data

    def execute(self):
        try:
            for replace in self.replace_list:
                for column in replace["columns"]:
                    self.df[column] = self.df[column] = self.df[column].str.replace(replace["replace_this"], replace["for_this"], regex=self.regex )
        except Exception as e:
            raise Exception(f"An error occurred while trying to replace values in columns. {e}")

        return self.df

    def transfor_process(self, config, group_criteria):
        pass
