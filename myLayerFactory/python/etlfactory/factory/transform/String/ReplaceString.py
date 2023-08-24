from etlfactory.factory.transform.abs_transform import AbsTransform

class ReplaceString(AbsTransform):

    def execute(self, dfs: dict, table, parameters):

        df = dfs[table]
        columns_to_process = parameters['column_to_process']
        pattern_to_remove = parameters['pattern_to_remove']

        try:
            for column in columns_to_process:
                df[column] = df[column].str.replace(pattern_to_remove,"")

        except Exception as e:
            raise Exception(f"Unable to replace blank spaces {e}")

        return df