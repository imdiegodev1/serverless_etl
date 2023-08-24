from etlfactory.factory.transform.abs_transform import AbsTransform

class RemoveNullsInColumns(AbsTransform):

    def execute(self, dfs: dict, table, parameters):

        df = dfs[table]

        df = df.dropna(subset = parameters['columns'], how = parameters['how'])

        return df