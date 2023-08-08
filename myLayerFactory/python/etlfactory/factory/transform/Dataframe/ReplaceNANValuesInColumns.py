from etlfactory.factory.transform.abs_transform import AbsTransform

class ReplaceNANValuesInColumns(AbsTransform):

    def execute(self, dfs: dict, table, parameters):
        try:
            df = dfs[table]
            for replace in parameters:
                for cols in parameters[replace]['columns']:
                    df[cols] = df[cols].fillna(parameters[replace]['for_this'])
        except Exception as e:
            raise Exception(f"An error occurred while trying to replace values in columns. {e}")

        return df

    def transfor_process(self, config, group_criteria):
        pass