from etlfactory.factory.transform.abs_transform import AbsTransform

class UppercaseStringColumns(AbsTransform):
    def __init__(self, config, data):
        super().__init__()
        self.columns = config["columns"]
        self.df = data

    def execute(self):
        """
        Removes leading and trailing spaces in the strings
        """
        try:
            for column in self.columns:
                self.df[column] = self.df[column].str.upper()
        except Exception as e:
            raise Exception(f"Unable to uppercase string {e}")

        return self.df

    def transfor_process(self, config, group_criteria):
        pass
